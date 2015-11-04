__author__ = 'vdthoang'
from main.loadFile import load_file
from sklearn.cross_validation import KFold, StratifiedKFold
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfTransformer
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
import sys
from CRF_labeling.filterText_CRF import filterTxt_CRF
import numpy as np
from main.filter_text import filter_token
import chardet
from operator import itemgetter
from main.writeFile import write_file


# make the default is 'utf-8'
reload(sys)
sys.setdefaultencoding('utf8')


def load_event_x_y(sentences):
    all, X, Y = list(), list(), list()
    for sent in sentences:
        split_sent = sent.strip().split('\t')
        label = split_sent[1]  # load label
        text = split_sent[2]  # load text
        X.append(text), Y.append(label)
        # X.append(filter_token(text)), Y.append(label)
    # decoded = [x.decode(chardet.detect(x)['encoding']) for x in X]
    # all.append(decoded), all.append(Y)

    all.append(X), all.append(Y)
    return all


def clf_event_running(path, event, name_clf, X, Y, clf, K, command, call):
    if command == 'KFold':
        cv = KFold(len(X), K, shuffle=True, random_state=0)
    elif command == 'StratifiedKFold':
        cv = StratifiedKFold(Y, 4)
    else:
        print 'Need a correct command'
        quit()
    # print cv.n_folds

    list_print = list()

    for traincv, testcv in cv:
        X_train = X[traincv]
        X_test = X[testcv]
        y_train, y_test = Y[traincv], Y[testcv]

        MIN_DF = 2
        vec = CountVectorizer(lowercase=True, min_df=MIN_DF)
        vec = vec.fit(X)

        X_train_trans = vec.transform(X_train)
        X_test_trans = vec.transform(X_test)

        # transformer = TfidfTransformer()
        # X_train_trans, X_test_trans = transformer.fit_transform(X_train_trans), transformer.fit_transform(X_test_trans)

        clf.fit(X_train_trans, y_train)  # training model
        y_test_pred = clf.predict(X_test_trans)

        matrix = confusion_matrix(y_test_pred, y_test)
        for value in matrix:
            line = ''
            for each in value:
                line = line + str(each) + '\t'
            print line.strip()
        print '----------------'

        # cnt = 0
        # for index in testcv:
        #     pred, truth = y_test_pred[cnt], y_test[cnt]
        #
        #     # if pred != truth:
        #     print index, str(pred), str(truth), X[index]
        #     cnt += 1

        if call == 'PrintPredicted':
            cnt = 0
            for index in testcv:
                tweet, pred, truth = X[index], y_test_pred[cnt], y_test[cnt]
                list_ = list()
                list_.append(index), list_.append(pred), list_.append(truth), list_.append(tweet)
                list_print.append(list_)
                cnt += 1

    if call == 'PrintPredicted':
        list_print = sorted(list_print, key=itemgetter(0))  # sorted list based on index
        list_write = list()
        for value in list_print:
            print str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2]) + '\t' + str(value[3])
            list_write.append(str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2]) + '\t' + str(value[3]))
        write_file(path, event + '_' + name_clf, list_write)

################################################################################################
################################################################################################
if __name__ == '__main__':
    # TWITTER
    # events = ['missing', 'delay']
    # events = ['delay']
    # events = ['wait', 'slow', 'missing']
    # events = ['missing', 'slow']
    events = ['wait']
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents'
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets'
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver2'

    for event in events:
        list_sentences = load_file(path, event + '.csv')
        print 'Running event: ', event
        list_all = load_event_x_y(list_sentences)
        X, Y = np.array(list_all[0]), np.array(list_all[1])
        # clf = MultinomialNB()
        # clf = LinearSVC(C=1.0, random_state=0, class_weight='auto', max_iter=5000)
        clf = LogisticRegression(max_iter=10000, solver='liblinear', tol=0.000001, penalty='l1', class_weight='auto')
        # clf_event_running(X, Y, clf, K=5, command='KFold')
        clf_event_running(path, event, 'LR', X, Y, clf, K=5, command='StratifiedKFold', call='PrintPredicted')
