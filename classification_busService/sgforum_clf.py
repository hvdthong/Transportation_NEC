__author__ = 'vdthoang'
from sklearn.cross_validation import cross_val_score, KFold
from main.loadFile import load_file
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split
import numpy as np
from scipy.stats import sem
from sklearn import metrics
from sklearn.metrics import f1_score
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegressionCV
from sklearn.linear_model import LogisticRegression
from classification_busService.ftr_bussvc_extraction import load_bus_svc
from main.pattern_busService import pattern_bus_service_ver2, pattern_bus_service


def ftr_sgforum(texts):
    list_target = []
    list_ftr = []
    for text in texts:
        split_text = text.split('\t')

        target = split_text[1]  # mean label
        list_target.append(target)

        # ftr = split_text[3].encode('utf-8')
        ftr = split_text[3]  # mean target
        # print ftr
        list_ftr.append(ftr)

    list_all = []
    list_all.append(list_ftr)  # add feature
    list_all.append(list_target)  # add target
    return list_all


def ftr_sgforum_svc(texts):  # doing like ftr_sgforum, but we add list of bus service
    list_target = []
    list_ftr = []
    list_svc = []

    for text in texts:
        split_text = text.split('\t')

        target = split_text[1]  # get label
        list_target.append(target)
        svc = split_text[2].strip()  # get bus service
        list_svc.append(svc)
        # ftr = split_text[3].encode('utf-8')
        ftr = split_text[3]  # get target
        list_ftr.append(ftr)

    list_all = []
    list_all.append(list_ftr)  # add feature
    list_all.append(list_target)  # add target
    list_all.append(list_svc)  # add bus service
    return list_all


def evaluate_cross_validation(clf, X, y, K):
    # create a k-fold croos validation iterator of k=5 folds
    cv = KFold(len(y), K, shuffle=True, random_state=0)
    # by default the score used is the one returned by score method of the estimator (accuracy)

    # scores_prc = cross_val_score(clf, X, y, cv=cv, scoring='precision')
    # print scores_prc
    # print ("Mean score precision: {0:.3f} (+/-{1:.3f})").format(np.mean(scores_prc), sem(scores_prc))
    # scores_rcl = cross_val_score(clf, X, y, cv=cv, scoring='recall')
    # print scores_rcl
    # print ("Mean score recall: {0:.3f} (+/-{1:.3f})").format(np.mean(scores_rcl), sem(scores_rcl))
    scores_f1 = cross_val_score(clf, X, y, cv=cv, scoring='f1_weighted')
    print scores_f1
    print ("Mean score f1: {0:.3f} (+/-{1:.3f})").format(np.mean(scores_f1), sem(scores_f1))
    scores_acc = cross_val_score(clf, X, y, cv=cv)
    print scores_acc
    print ("Mean score accuracy: {0:.3f} (+/-{1:.3f})").format(np.mean(scores_acc), sem(scores_acc))


def clf_sgforum(texts):
    list_ftr = ftr_sgforum(texts)
    clf = Pipeline([('vect', CountVectorizer()), ('clf', MultinomialNB())])
    # clf = Pipeline([('vect', CountVectorizer()), ('clf', svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,gamma=0.0, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False))])
    # clf = Pipeline([('vect', CountVectorizer()), ('clf', SGDClassifier())])
    # clf = Pipeline([('vect', TfidfVectorizer()), ('clf', SGDClassifier())])
    # clf = Pipeline([('vect', CountVectorizer()), ('clf', LogisticRegression())])
    clf = Pipeline([('vect', CountVectorizer()), ('clf', svm.LinearSVC(C=1.0, random_state=0, class_weight='auto'))])
    evaluate_cross_validation(clf, list_ftr[0], list_ftr[1], 5)


def n_fold_cross_valid(texts, clf, K):
    list_ftr = ftr_sgforum(texts)
    X = np.array(list_ftr[0])
    y = np.array(list_ftr[1])

    cv = KFold(len(X), K, shuffle=True, random_state=0)
    print cv.n_folds
    for traincv, testcv in cv:

        X_train, X_test = X[traincv], X[testcv]
        y_train, y_test = y[traincv], y[testcv]

        MIN_DF = 2
        vec = CountVectorizer(token_pattern='[A-Za-z0-9]*', lowercase=True, min_df=MIN_DF)
        vec = vec.fit(X)
        X_train_trans = vec.transform(X_train)
        X_test_trans = vec.transform(X_test)

        clf.fit(X_train_trans, y_train)  # training model
        y_test_pred = clf.predict(X_test_trans)

        print metrics.accuracy_score(y_test, y_test_pred)
        print metrics.classification_report(y_test, y_test_pred)
        print metrics.confusion_matrix(y_test, y_test_pred)


def n_fold_cross_valid_label(texts, clf, K):
    # doing like function n_fold_cross_valid but we will check the non-correct label
    list_ftr = ftr_sgforum_svc(texts)
    X = np.array(list_ftr[0])
    y = np.array(list_ftr[1])
    word = np.array(list_ftr[2])

    cv = KFold(len(X), K, shuffle=True, random_state=0)
    print cv.n_folds
    for traincv, testcv in cv:

        X_train, X_test = X[traincv], X[testcv]
        y_train, y_test = y[traincv], y[testcv]
        word_train, word_test = word[traincv], word[testcv]

        MIN_DF = 2
        vec = CountVectorizer(token_pattern='[A-Za-z0-9]*', lowercase=True, min_df=MIN_DF)
        vec = vec.fit(X)
        X_train_trans = vec.transform(X_train)
        X_test_trans = vec.transform(X_test)

        clf.fit(X_train_trans, y_train)  # training model
        y_test_pred = clf.predict(X_test_trans)

        for i in range(0, len(y_test_pred)):
            if y_test[i] != y_test_pred[i]:
                print word_test[i]


#############################################################################################
#############################################################################################
def check_reg(svc, text, list_sv):
    # if the text contain correct bus service which appear in text, add word "feature_reg"
    list_pattern_services = pattern_bus_service_ver2(text, list_sv)
    list_match_services = pattern_bus_service(text, list_sv)

    list_total = list(set(list_pattern_services) | set(list_match_services))

    if svc in list_total:
        return text + ' feature_reg'
    else:
        return text


def extend_clf_with_reg(list_text, list_sv, clf, K):
    list_new_text = list()
    for element in list_text:
        split_element = element.split('\t')
        index = split_element[0]
        label = split_element[1]
        svc = split_element[2].strip()
        text = split_element[3]

        new_text = check_reg(svc, text, list_sv)
        string = index + '\t' + label + '\t' + svc + '\t' + new_text
        list_new_text.append(string)

    print '------ Finish to add the regular expression features ------'
    # for value in list_new_text:
    #     print value
    # n_fold_cross_valid(list_new_text, clf, K)
    n_fold_cross_valid_label(list_new_text, clf, K)

if __name__ == '__main__':
    #############################################################################################
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling'
    # name = 'sgforum_label.csv'
    # clf_sgforum(list_text) # old file, can't use in general case
    #############################################################################################

    #############################################################################################
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    # name = 'feature_svc_n10.txt'
    # list_text = load_file(path, name)
    # clf = MultinomialNB()
    # clf = svm.LinearSVC(C=1.0, random_state=0, class_weight='auto')
    # clf = LogisticRegression()
    # K = 5  # number of cross-validation
    # n_fold_cross_valid(list_text, clf, K)  # running K cross validation for clf, where each K: print coefficient matrix
    #############################################################################################


    #############################################################################################
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    name = 'feature_svc_n10.txt'
    list_text = load_file(path, name)

    path_sv = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name_sv = 'bus_services.csv'
    load_sv = load_bus_svc(load_file(path_sv, name_sv))
    list_sv = [item.lower() for item in load_sv]
    # clf = MultinomialNB()
    # clf = svm.LinearSVC(C=1.0, random_state=0, class_weight='auto')
    clf = LogisticRegression()
    K = 5  # number of cross-validation
    extend_clf_with_reg(list_text, list_sv, clf, K)
    #############################################################################################

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    # name = 'feature_svc_n10.txt'
    # list_text = load_file(path, name)
    # clf = LogisticRegression()
    # K = 5  # number of cross-validation
    # n_fold_cross_valid_label(list_text, clf, K)
