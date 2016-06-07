__author__ = 'vdthoang'
from main.loadFile import load_file
from main.writeFile import write_file
from clf_event.CLF_one_vs_one import events_none, convert_list_
from sklearn.cross_validation import KFold
from clf_event.CLF_event import load_event_x_y
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix


def event_listIndex(event, indexs):
    list_value = list()
    for index in indexs:
        list_value.append(event[index])
    return list_value


def write_file_training(totalFold, numFold, training, path, events):
    for i in range(0, len(training)):
        j = i + 1
        for k in range(j, len(training)):
            first, second = training[i], training[k]
            second = convert_list_(second, events[k])
            new_list = first + second
            print events[i], events[k]
            write_file(path, str(totalFold) + 'Folds_' + events[i] + '_' + events[k] + '_training_' + str(numFold), new_list)


def write_file_testing(totalFold, numFold, testing, path, events):
    for i in range(0, len(testing)):
        write_file(path, str(totalFold) + 'Folds_' + events[i] + '_testing_' + str(numFold), testing[i])


def each_event_list(path, events, numFolds):
    list_events, list_nones = list(), list()
    for event in events:
        list__ = load_file(path, event + '.csv')
        list_event, list_none = events_none(list__)
        list_events.append(list_event), list_nones.append(list_none)
        # print len(list_event)

    for i in range(0, len(list_nones)):
        if i == 0:
            first = list(set(list_nones[i]).intersection(list_nones[i + 1]))
        elif i == len(list_nones) - 1:
            break
        else:
            first = list(set(first).intersection(list_nones[i + 1]))

    list_none = first
    list_events.append(list_none)
    events.append('none')

    event_cross_valid = list()
    for event in list_events:
        train_test, training, testing = list(), list(), list()
        kfold = KFold(len(event), n_folds=numFolds)
        for train_index, test_index in kfold:
            print len(train_index), len(test_index)
            training.append(train_index), testing.append(test_index)
        train_test.append(training), train_test.append(testing)
        event_cross_valid.append(train_test)

    print len(event_cross_valid)
    print events, len(list_events)

    for i in range(0, numFolds):
        training_event, testing_event = list(), list()
        for j in range(0, len(events)):
            event_fold = event_cross_valid[j]
            training_fold, testing_fold = event_fold[0], event_fold[1]
            training, testing = training_fold[i], testing_fold[i]
            value_training, value_testing = event_listIndex(list_events[j], training), event_listIndex(list_events[j], testing)
            print len(value_training), len(value_testing)

            training_event.append(value_training), testing_event.append(value_testing)
        write_file_training(numFolds, i, training_event, path, events)
        write_file_testing(numFolds, i, testing_event, path, events)


def testing_data(path, events, indexFold, numFold):
    labels, sents = list(), list()
    for i in range(0, len(events)):
        list_event = load_file(path, str(numFold) + 'Folds_' + events[i] + '_testing_' + str(indexFold) + '.csv')
        for line in list_event:
            split_line = line.split('\t')
            labels.append(str(i)), sents.append(split_line[2])
    return labels, sents


def convert_test_pred(y_pred, first, second):
    new_pred = list()
    for pred in y_pred:
        if pred == '1':
            new_pred.append(first)
        else:
            new_pred.append(second)
    return new_pred


def clf_event_one_one(clf, X_train, Y_train, X_test, first_index, second_index):
    vec = CountVectorizer(lowercase=True, min_df=2)
    vec = vec.fit(X_train)

    X_train_trans = vec.transform(X_train)
    X_test_trans = vec.transform(X_test)

    # transformer = TfidfTransformer()
    # X_train_trans, X_test_trans = transformer.fit_transform(X_train_trans), transformer.fit_transform(X_test_trans)

    clf.fit(X_train_trans, Y_train)  # training model
    y_test_pred = convert_test_pred(clf.predict(X_test_trans), first_index, second_index)
    return y_test_pred


def find_max_label(list_, events):
    labels = list()
    for i in range(0, len(events)):
        labels.append(i)

    list_new = list()
    for line in list_:
        list_count = list()
        for label in labels:
            list_count.append(line.count(str(label)))

        # Sgforums
        if max(list_count) == 1:  # the labels are equally divided
            list_new.append('2')
        else:
            list_new.append(str(list_count.index(max(list_count))))
    return list_new


def clf_one_one(path, events, numFold):
    events.append('none')

    for i in range(0, numFold):
        label_test, sent_test = testing_data(path, events, i, numFold)
        print len(label_test), len(sent_test)
        list_pred, list_join = list(), list()
        for j in range(0, len(events)):
            k = j + 1
            for k in range(k, len(events)):
                # print events[j] + '_' + events[k]
                sent_train = load_file(path_, str(numFold) + 'Folds_' + events_[j] + '_' + events_[k]
                                       + '_training_' + str(i) + '.csv')
                print 'Running event: ', events[j] + '_' + events[k] + ':Fold_index_' + str(i)
                list_all = load_event_x_y(events_[j] + '_' + events_[k], sent_train, command='')
                X, Y = np.array(list_all[0]), np.array(list_all[1])
                # clf = MultinomialNB()
                # clf = LinearSVC(C=1.0, random_state=0, class_weight='auto', max_iter=100000)
                clf = LogisticRegression(max_iter=50000, solver='liblinear', tol=0.000001, class_weight='auto')
                list_pred.append(clf_event_one_one(clf, X, Y, sent_test, j, k))

        for m in range(0, len(list_pred)):
            if m == 0:
                list_join = list_pred[m]
            else:
                list_join = [str(x) + str(y) for x, y in zip(list_join, list_pred[m])]
        pred_label = find_max_label(list_join, events)
        list_matrix = confusion_matrix(pred_label, label_test)
        for row in list_matrix:
            line = ''
            for value in row:
                line = line + '\t' + str(value)
            print line.strip()


if __name__ == '__main__':
    # Sgforums
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_classification_events/detectAllEvents_ver2'
    # events_ = ['bunch', 'crowd']
    # numFold = 5
    # each_event_list(path_, events_, numFold)  # using to create files for cross validation one by one
    # # clf_one_one(path_, events_, numFold)


    # Facebook
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event/detectAllEvents_ver2'
    # events_ = ['complaint', 'compliment', 'skip', 'suggestion', 'wait']
    # numFold = 5
    # # each_event_list(path_, events_, numFold)  # using to create files for cross validation one by one
    # clf_one_one(path_, events_, numFold)


    # Twitter
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver3'
    events_ = ['wait', 'missing', 'skip', 'slow', 'accident', 'crowd']
    numFold = 5
    # each_event_list(path_, events_, numFold)  # using to create files for cross validation one by one
    clf_one_one(path_, events_, numFold)