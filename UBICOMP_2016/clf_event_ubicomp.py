__author__ = 'vdthoang'
import MySQLdb
from clf_event.CLF_one_vs_one import events_all
from main.loadFile import load_file
from clf_event.preprocessText import clean_url
from clf_event.CLF_event import load_event_x_y, clf_event_running
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
import numpy as np
from ICWSM_2016.CLF_event_predicted import clf_event_predicted
from main.writeFile import write_file


def load_data_ubicomp():
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                      passwd="ducthong",  # your password
                      db="2015_allschemas")  # name of the data base

    cur = db.cursor()

    # Use all the SQL you like
    cur.execute("select tweetID, tweetText from twitter_icwsm_correct")
    data_id, data_text = list(), list()

    for row in cur.fetchall():
        data_id.append(row[0])
        data_text.append(clean_url(row[1]))
    return data_id, data_text


def write_pred_event(path, id_, text_, pred, event_1, event_2):
    list_write = list()
    for i in range(0, len(id_)):
        line = ''
        if int(pred[i]) == 0:
            line = id_[i] + '\t' + text_[i] + '\t' + event_2
        else:
            line = id_[i] + '\t' + text_[i] + '\t' + event_1
        list_write.append(line)
    write_file(path, 'pred_' + event_1 + '_' + event_2, list_write)


def pred_label(pred, event_1, event_2):
    pred_event = list()
    for i in range(0, len(pred)):
        if int(pred[i]) == 0:
            line = event_2
        else:
            line = event_1
        pred_event.append(line)
    return pred_event


def restruct_pred(pred_all):
    length = len(pred_all[0])
    list_new = list()
    for i in range(0, length):
        event = list()
        for j in range(0, len(pred_all)):
            index = pred_all[j]
            event.append(index[i])

        d = {x: event.count(x) for x in event}
        list_new.append(d)
    print len(list_new)
    return list_new


if __name__ == '__main__':
    id_, text_ = load_data_ubicomp()
    print len(id_), len(text_)

    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver3'
    events_ = ['accident', 'crowd', 'missing', 'skip', 'slow', 'wait']
    # events_all(path_, events_)
    events_.append('none')
    list_pred = list()
    for i in range(0, len(events_)):
        j = i + 1
        for k in range(j, len(events_)):
            print events_[i], events_[k]
            list_sentences = load_file(path_, events_[i] + '_' + events_[k] + '.csv')
            print 'Running event: ', events_[i] + '_' + events_[k]
            list_all = load_event_x_y(events_[i] + '_' + events_[k], list_sentences, command='')
            X, Y = np.array(list_all[0]), np.array(list_all[1])
            # clf = LinearSVC(C=1.0, random_state=0, class_weight='auto', max_iter=100000)
            clf = LogisticRegression(max_iter=50000, solver='liblinear', tol=0.000001, class_weight='auto')
            pred = clf_event_predicted(text_, X, Y, clf)
            list_pred.append(pred_label(pred, events_[i], events_[k]))

    print len(list_pred)
    new_struct = restruct_pred(list_pred)
    for i in range(0, len(new_struct)):
        index = new_struct[i]
        print str(index.keys()[0]) + ' ' + str(index.values()[0])

        if index.keys()[0] != 'none':
            print index
            break





