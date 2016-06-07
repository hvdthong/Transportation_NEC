__author__ = 'vdthoang'
from main.loadFile import load_file
from main.writeFile import write_file
from clf_event.CLF_event import load_event_x_y, clf_event_running
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC


def events_none(list_):
    list_event, list_none = list(), list()
    for line in list_:
        split_line = line.split('\t')
        if int(split_line[1]) == 1:
            list_event.append(line)
        else:
            list_none.append('none' + '\t' + '0' + '\t' + split_line[2])
    return list_event, list_none


def convert_list_(list_, event):
    new_list = list()
    for line in list_:
        split_line = line.split('\t')
        try:
            new_list.append(event + '\t' + '0' + '\t' + split_line[2])
        except IndexError:
            print 'catching error'
    return new_list


def events_all(path, events):
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

    for event in list_events:
        print len(event)

    for i in range(0, len(list_events)):
        j = i + 1
        for k in range(j, len(list_events)):
            first, second = list_events[i], list_events[k]
            second = convert_list_(second, events[k])
            new_list = first + second
            print events[i], events[k]
            write_file(path, events[i] + '_' + events[k], new_list)


if __name__ == '__main__':
    # Sgforums
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_classification_events/detectAllEvents_ver2'
    # events_ = ['bunch', 'crowd']
    # events_all(path_, events_)

    # Facebook
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event/detectAllEvents_ver2'
    # events_ = ['complaint', 'compliment', 'skip', 'suggestion', 'wait']
    # events_all(path_, events_)

    # running classification for event
    # Sgforums
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_classification_events/detectAllEvents_ver2'
    # events_ = ['bunch', 'crowd']

    # Facebook
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event/detectAllEvents_ver2'
    events_ = ['complaint', 'compliment', 'skip', 'suggestion', 'wait']
    events_.append('none')
    for i in range(0, len(events_)):
        j = i + 1
        for k in range(j, len(events_)):
            print events_[i], events_[k]
            list_sentences = load_file(path_, events_[i] + '_' + events_[k] + '.csv')
            print 'Running event: ', events_[i] + '_' + events_[k]
            list_all = load_event_x_y(events_[i] + '_' + events_[k], list_sentences, command='')
            X, Y = np.array(list_all[0]), np.array(list_all[1])
            # clf = MultinomialNB()
            # clf = LinearSVC(C=1.0, random_state=0, class_weight='auto', max_iter=100000)
            clf = LogisticRegression(max_iter=50000, solver='liblinear', tol=0.000001, class_weight='auto')

            # clf_event_running(X, Y, clf, K=5, command='KFold')
            # clf_event_running(path, event, 'LR', X, Y, clf, K=5, command='StratifiedKFold', call='PrintPredicted')
            # clf_event_running(path, event, 'LR', X, Y, clf, K=5, command='StratifiedKFold', call='ProbScore')
            clf_event_running(path_, events_[i] + '_' + events_[k], 'LR', X, Y, clf, K=5, command='StratifiedKFold', call='')