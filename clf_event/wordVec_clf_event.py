__author__ = 'vdthoang'
from main.loadFile import load_file
from CRF_labeling.filterText_CRF import filter_eachTok_rmLinks
from CRF_labeling.CRF_wordVector import wordVector_storage
import numpy as np
from scipy.sparse import *
from CLF_event import load_event_x_y
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import hstack
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
from sklearn.svm import LinearSVC


def load_tweets(texts):
    tweets = list()
    for t in texts:
        split_t = t.split('\t')
        tweet = ''
        for w in split_t[2].split():
            tweet += filter_eachTok_rmLinks(w, 'twitter') + ' '
        tweets.append(tweet.strip().lower())
    return tweets


def load_facebook(texts):
    posts = list()
    for t in texts:
        split_t = t.split('\t')
        post = ''
        for w in split_t[2].split():
            post += filter_eachTok_rmLinks(w, 'model') + ' '
        posts.append(post.strip().lower())
    return posts


def tweetVec(texts, dict_w, vec_w):
    X_vec = list()
    for i in xrange(0, len(texts)):
        split_i = texts[i].split()
        j = 0
        sum_vec = np.zeros(len(vec_w[0]))
        for w in split_i:
            if w in dict_w:
                vec = vec_w[dict_w.index(w)]
                vec_convert = np.array(vec, dtype=np.float)
                sum_vec += vec_convert

        X_vec.append(sum_vec)
    return csr_matrix(np.array(X_vec))


def clf_event_running_wordVec(path, event, name_clf, X, X_vec, Y, clf, K, command, call):
    if command == 'StratifiedKFold':
        cv = StratifiedKFold(Y, K)
    else:
        print 'Need a correct command'
        quit()

    X_vec_norm = preprocessing.normalize(X_vec, norm='l2')
    for traincv, testcv in cv:
        X_train, X_test = X[traincv], X[testcv]
        X_vec_train, X_vec_test = X_vec_norm[traincv], X_vec_norm[testcv]
        y_train, y_test = Y[traincv], Y[testcv]

        MIN_DF = 2
        vec = CountVectorizer(lowercase=True, min_df=2)
        vec = vec.fit(X_train)

        X_train_trans, X_test_trans = vec.transform(X_train), vec.transform(X_test)
        X_train_trans_all, X_test_trans_all = hstack([X_train_trans, X_vec_train]), hstack([X_test_trans, X_vec_test])

        # print X_vec_train.shape, X_vec_test.shape
        # print X_train_trans.shape, X_test_trans.shape
        # print X_train_trans_all.shape, X_test_trans_all.shape

        clf.fit(X_train_trans_all, y_train)  # training model
        y_test_pred = clf.predict(X_test_trans_all)

        matrix = confusion_matrix(y_test_pred, y_test)
        for value in matrix:
            line = ''
            for each in value:
                line = line + str(each) + '\t'
            print line.strip()
        print '----------------'


if __name__ == '__main__':
    # path_w = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/WordVector'
    # # name_w = 'word_vec_30.csv'
    # # name_w = 'word_vec_70.csv'
    # # name_w = 'word_vec_100.csv'
    # # name_w = 'word_vec_150.csv'
    # name_w = 'word_vec_200.csv'
    # vec = load_file(path_w, name_w)
    # dict_w, vec_w = wordVector_storage(vec)
    #
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver3'
    # events = ['accident', 'crowd', 'missing', 'skip', 'slow', 'wait']
    #
    # texts = load_tweets(load_file(path, events[0] + '.csv'))

    path_w = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/WordVector'
    # name_w = 'word_vec_30.csv'
    # name_w = 'word_vec_70.csv'
    # name_w = 'word_vec_100.csv'
    # name_w = 'word_vec_150.csv'
    name_w = 'word_vec_200.csv'
    vec = load_file(path_w, name_w)
    dict_w, vec_w = wordVector_storage(vec)

    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event/detectAllEvents_ver2'
    events = ['complaint', 'compliment', 'skip', 'suggestion', 'wait']
    texts = load_facebook(load_file(path, events[0] + '.csv'))

    tweetsVec = tweetVec(texts, dict_w, vec_w)
    print tweetsVec.shape
    print type(tweetsVec)

    path_write = ''
    name_write = ''

    for event in events:
        list_sentences = load_file(path, event + '.csv')
        print 'Running event: ', event

        list_all = load_event_x_y(event, list_sentences, command='')
        X, Y = np.array(list_all[0]), np.array(list_all[1])
        # clf = LinearSVC(C=1.0, random_state=0, class_weight='auto', max_iter=500000)
        clf = LogisticRegression(max_iter=100000, solver='liblinear', tol=0.000001, class_weight='auto')
        clf_event_running_wordVec(path_write, event, 'LR', X, tweetsVec, Y, clf, K=5, command='StratifiedKFold', call='')

