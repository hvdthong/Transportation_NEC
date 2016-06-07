__author__ = 'vdthoang'
from main.loadFile import load_file
from clf_event.CLF_event import load_event_x_y
import numpy as np
from sklearn.svm import LinearSVC
from clf_event.preprocessText import clean_url
from sklearn.feature_extraction.text import CountVectorizer
from main.writeFile import write_file
import MySQLdb
from sklearn.linear_model import LogisticRegression


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


def load_data(path, name, command):
    list_ = load_file(path, name)
    X = list()
    for line in list_:
        split_line = line.split('\t')
        text = split_line[3]

        if command == 'preprocessText':
            text = clean_url(text)

        X.append(text)
    return X


def load_data_ID(path, name):
    list_ = load_file(path, name)
    X_id = list()
    for line in list_:
        split_line = line.split('\t')
        id = split_line[0]
        X_id.append(id)
    return X_id


def clf_event_predicted(X, X_train, Y_train, clf):
    MIN_DF = 2
    vec = CountVectorizer(lowercase=True, min_df=MIN_DF)
    vec = vec.fit(X)

    X_train_trans = vec.transform(X_train)
    X_trans = vec.transform(X)

    clf.fit(X_train_trans, Y_train)
    pred = clf.predict(X_trans)

    # for i in range(0, len(pred)):
    #     print pred[i], X[i]
    return pred


def writing_pred(path, event, X_id, X, X_pred):
    list_write = list()
    for i in range(0, len(X_id)):
        line = X_id[i] + '\t' + X_pred[i] + '\t' + X[i]
        list_write.append(line)

    write_file(path, 'twitter_event_' + event, list_write)

if __name__ == '__main__':
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver3'
    events = ['wait', 'missing', 'skip', 'slow', 'accident', 'crowd']

    path_load = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data'
    # name_load = 'twitter.csv'
    # X_ = load_data(path_load, name_load, 'preprocessText')
    # X_id = load_data_ID(path_load, name_load)

    X_id, X_ = load_data_ubicomp()

    # print len(X_)

    for event in events:
        list_sentences = load_file(path, event + '.csv')
        print 'Running event: ', event
        list_all = load_event_x_y(event, list_sentences, command='preprocessText')

        X_train, Y_train = np.array(list_all[0]), np.array(list_all[1])
        # clf = LinearSVC(C=1.0, random_state=0, class_weight='auto', max_iter=100000)
        clf = LogisticRegression(max_iter=50000, solver='liblinear', tol=0.000001, class_weight='auto')
        X_pred = clf_event_predicted(X_, X_train, Y_train, clf)
        writing_pred(path_load, event, X_id, X_, X_pred)



