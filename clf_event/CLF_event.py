__author__ = 'vdthoang'
from main.loadFile import load_file
from sklearn.cross_validation import KFold
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
import sys
from CRF_labeling.filterText_CRF import filterTxt_CRF
import numpy as np
from main.filter_text import filter_token


# make the default is 'utf-8'
reload(sys)
sys.setdefaultencoding('utf8')


def load_event_x_y(sentences):
    all, X, Y = list(), list(), list()
    for sent in sentences:
        split_sent = sent.strip().split('\t')
        label = split_sent[1]  # load label
        text = split_sent[2]  # load text
        # X.append(text), Y.append(label)
        X.append(filter_token(text)), Y.append(label)

    all.append(X), all.append(Y)
    return all


def clf_event_running(X, Y, clf, K):
    cv = KFold(len(X), K, shuffle=True, random_state=0)
    # print cv.n_folds
    for traincv, testcv in cv:

        X_train = X[traincv]
        X_test = X[testcv]
        y_train, y_test = Y[traincv], Y[testcv]

        MIN_DF = 2
        vec = CountVectorizer(lowercase=True, min_df=MIN_DF)
        # vec = HashingVectorizer()
        vec = vec.fit(X)

        X_train_trans = vec.transform(X_train)
        X_test_trans = vec.transform(X_test)

        clf.fit(X_train_trans, y_train)  # training model
        y_test_pred = clf.predict(X_test_trans)

        matrix = confusion_matrix(y_test_pred, y_test)
        for value in matrix:
            line = ''
            for each in value:
                line = line + str(each) + '\t'
            print line.strip()
        print '----------------'


if __name__ == '__main__':
    # TWITTER
    events = ['missing', 'delay']
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents'

    for event in events:
        list_sentences = load_file(path, event + '.csv')
        print 'Running event: ', event
        list_all = load_event_x_y(list_sentences)
        X, Y = np.array(list_all[0]), np.array(list_all[1])
        clf = MultinomialNB()
        # clf = LinearSVC(C=1.0, random_state=0, class_weight='auto', max_iter=5000)
        # clf = LogisticRegression(max_iter=10000, solver='liblinear', tol=0.000001, penalty='l1')
        clf_event_running(X, Y, clf, K=4)


