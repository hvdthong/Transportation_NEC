__author__ = 'vdthoang'
from CRF_labeling.feature_crf_all import folder_files
from main.loadFile import load_file
from CRF_labeling.feature_crf import load_target_label, construct_ftr_CRF, metrics_crf
import numpy as np
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn import metrics, svm
from sklearn.cross_validation import KFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from operator import itemgetter
from CRF_labeling.filterText_CRF import filterTxt_CRF
from CRF_labeling.feature_crf import label_distribution


def featuers_CRF(files, path):
    # reading all CRF features and add them to list
    list_all = []
    for f in files:
        list_f = load_file(path, f)
        list_all.append(list_f)
    return list_all


def convert_ftr_x_clf(list_all):  # convert features list
    list_convert = construct_ftr_CRF(list_all)
    list_ftr_token = []

    for sentence in list_convert:
        for word in sentence:
            list_ftr_token.append(word)
    return list_ftr_token


def convert_frt_y_clf(list_target):  # convert target label
    list_convert = load_target_label(list_target)
    list_target = []

    for sentence in list_convert:
        for label in sentence:
            list_target.append(label)
    return list_target


#################################################################################################
#################################################################################################
def metrics_clf_ftrCRF(y_test, y_pred):  # we know that we have 4 labels
    num_label = []
    for label in y_test:
        if label not in num_label:
            num_label.append(label)
    labels = sorted(num_label)
    for label in labels:
        TT, TF, FT, FF = 0, 0, 0, 0
        for i in range(0, len(y_test)):
            pred = y_pred[i]
            test = y_test[i]

            if (pred == test) and (test == label) and (pred == label):
                TT += 1
            elif (pred != test) and (test != label) and (pred == label):
                TF += 1
            elif (pred != test) and (test == label) and (pred != label):
                FT += 1
            elif (test != pred) and (test != label) and (pred != label):
                FF += 1

            # print 'Finish %i' % i

        print 'Confusion matrix of label ' + str(label) + '\t' + str(TT) + '\t' + str(TF) + '\t' + str(FT) + '\t' + str(FF)
        prc = TT / float(TT + TF)
        rcl = TT / float(TT + FT)
        try:
            f1 = 2 * prc * rcl / (prc + rcl)
        except ZeroDivisionError:
            f1 = 0

        prc_false = FF / float(FF + FT)
        rcl_false = FF / float(FF + TF)
        try:
            f1_false = 2 * prc_false * rcl_false / (prc_false + rcl_false)
        except ZeroDivisionError:
            f1_false = 0

        print 'Accuracy: %f' % ((TT + FF) / float(TT + FF + TF + FT))
        print 'F1 of True: %f' % f1
        print 'F1 of False: %f' % f1_false


def confusion_matrix_clf_CRF(y_test, y_pred):
    matrix = confusion_matrix(y_pred, y_test)
    for value in matrix:
        text = ''
        for each in value:
            text += str(each) + '\t'
        print text.strip()


def write_results_clf(list_index, y_test, y_pred):
    list_write = list()
    for i in range(0, len(list_index)):
        list_ = list()
        index, pred, test = list_index[i], y_pred[i], y_test[i]
        list_.append(index)
        list_.append(pred)
        list_.append(test)
        list_write.append(list_)
    return list_write


def n_cross_valid_clf_CRF(X, Y, clf, K, command):
    cv = KFold(len(X), K, shuffle=True, random_state=0)
    if command == 'write_results':
        list_write = list()
    for traincv, testcv in cv:
        x_train, x_test = X[traincv], X[testcv]
        y_train, y_test = Y[traincv], Y[testcv]

        clf.fit(x_train, y_train)
        y_pred = clf.predict(x_test)
        print 'Accuracy of linear-crf %f:' % clf.score(x_test, y_test)

        if command == 'metrics_F1':
            metrics_clf_ftrCRF(y_test, y_pred)
        elif command == 'confusion_matrix':
            confusion_matrix_clf_CRF(y_test, y_pred)
        elif command == 'write_results':
            list_write += write_results_clf(testcv, y_test, y_pred)
        else:
            print 'You need to give correct command'
            quit()

        print '------------------------------------------------------'
        print '------------------------------------------------------'

    if command == 'write_results':
        list_write = sorted(list_write, key=itemgetter(0))  # sorted list based on index
        for value in list_write:
            print str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2])


if __name__ == '__main__':
    # loading features from CRF, and construct the features for classification
    # running classification

    # # loading CRF features
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features/features'
    # files_ = folder_files(path_ftr)
    # features = featuers_CRF(files_, path_ftr)
    # X = np.array(convert_ftr_x_clf(features))
    # print len(X)
    #
    # # loading target labels
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    # name_ = 'Label_all_crf.txt'
    # list_line_ = load_file(path_, name_)
    # Y = np.array(convert_frt_y_clf(list_line_))
    # print len(Y)
    # print 'Loading the target labels ------------------------------------'
    #
    # # clf = MultinomialNB()
    # # clf = svm.LinearSVC(C=1.0, random_state=0, class_weight='auto')
    # clf = LogisticRegression()
    # n_cross_valid_clf_CRF(X, Y, clf, K=5)

    #################################################################################################
    #################################################################################################
    # RUNNING FOR TWITTER DATASET

    #################################################################################################
    # # loading CRF features, remember that we only remove all punctuation
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features'
    # files_ = folder_files(path_ftr)
    # features = featuers_CRF(files_, path_ftr)
    # X = np.array(convert_ftr_x_clf(features))
    # print len(X)
    #
    # # loading target labels
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    # name_ = 'labeling_all.txt'
    # list_line_ = filterTxt_CRF(load_file(path_, name_), 'removePunc')  # remove all punctuations
    # label_distribution(list_line_)  # get the distribution of labeling in Twitter
    # Y = np.array(convert_frt_y_clf(list_line_))
    # print len(Y)
    # print 'Loading the target labels ------------------------------------'
    #
    # clf = MultinomialNB()
    # # clf = svm.LinearSVC(C=1.0, random_state=0, class_weight='auto')
    # # clf = LogisticRegression()
    # n_cross_valid_clf_CRF(X, Y, clf, K=5, command='metrics_F1')  # use to calculate the F1 for classification
    # # n_cross_valid_clf_CRF(X, Y, clf, K=5, command='confusion_matrix')  # use to calculate the confusion matrix
    # # n_cross_valid_clf_CRF(X, Y, clf, K=5, command='write_results')  # use to calculate the confusion matrix

    #################################################################################################
    # TWITTER
    # loading CRF features, remember that we only remove all punctuation and links in Twitter
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLink'
    # files_ = folder_files(path_ftr)
    # features = featuers_CRF(files_, path_ftr)
    # X = np.array(convert_ftr_x_clf(features))
    # print len(X)
    #
    # # loading target labels
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    # name_ = 'labeling_all.txt'
    # list_line_ = filterTxt_CRF(load_file(path_, name_), 'removeLink')  # remove all punctuations
    # label_distribution(list_line_)  # get the distribution of labeling in Twitter
    # Y = np.array(convert_frt_y_clf(list_line_))
    # print len(Y)
    # print 'Loading the target labels ------------------------------------'
    #
    # # clf = MultinomialNB()
    # # clf = svm.LinearSVC(C=1.0, random_state=0, class_weight='auto')
    # clf = LogisticRegression()
    # # n_cross_valid_clf_CRF(X, Y, clf, K=5, command='metrics_F1')  # use to calculate the F1 for classification
    # # n_cross_valid_clf_CRF(X, Y, clf, K=5, command='confusion_matrix')  # use to calculate the confusion matrix
    # n_cross_valid_clf_CRF(X, Y, clf, K=5, command='write_results')  # use to calculate the confusion matrix

    #################################################################################################
    # FACEBOOK
    # loading CRF features, remember that we only remove all punctuation and links in Facebook
    path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF/crf_features/features'
    files_ = folder_files(path_ftr)
    features = featuers_CRF(files_, path_ftr)
    X = np.array(convert_ftr_x_clf(features))
    print len(X)

    # loading target labels
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF'
    name_ = 'label.txt'
    list_line_ = filterTxt_CRF(load_file(path_, name_), 'removePunc')  # remove all punctuations
    label_distribution(list_line_)  # get the distribution of labeling in Facebook
    Y = np.array(convert_frt_y_clf(list_line_))
    print len(Y)
    print 'Loading the target labels ------------------------------------'

    # clf = MultinomialNB()
    # clf = svm.LinearSVC(C=1.0, random_state=2500, class_weight='auto')
    clf = LogisticRegression()
    # n_cross_valid_clf_CRF(X, Y, clf, K=5, command='metrics_F1')  # use to calculate the F1 for classification
    # n_cross_valid_clf_CRF(X, Y, clf, K=5, command='confusion_matrix')  # use to calculate the confusion matrix
    n_cross_valid_clf_CRF(X, Y, clf, K=5, command='write_results')  # use to calculate the confusion matrix