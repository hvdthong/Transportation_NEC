__author__ = 'vdthoang'
from main.loadFile import load_file
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from classification_busService.sgforum_clf import n_fold_cross_valid


def extend_clf_road_busstop_with_reg(list_text, list_reg, clf, K):
    list_new_text = []
    for i in range(0, len(list_text)):
        reg = list_reg[i]
        if 'TRUE' in reg:
            new_text = list_text[i] + ' feature_reg'
            list_new_text.append(new_text)
        else:
            list_new_text.append(list_text[i])

    n_fold_cross_valid(list_new_text, clf, K)

if __name__ == '__main__':
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    # # name = 'feature_road_n5.txt'
    # name = 'feature_busstop_n5.txt'
    # list_text = load_file(path, name)
    # # clf = MultinomialNB()
    # # clf = svm.LinearSVC(C=1.0, random_state=0, class_weight='auto')
    # clf = LogisticRegression()
    # K = 5  # number of cross-validation
    # n_fold_cross_valid(list_text, clf, K)  # running K cross validation for clf, where each K: print coefficient matrix

    ###################################################################################################################
    ###################################################################################################################
    # adding features used regular expression to build classification model
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    # name = 'feature_road_n5.txt'
    # name_reg = 'feature_road_n5_re.txt'
    name = 'feature_busstop_n5.txt'
    name_reg = 'feature_busstop_n5_re.txt'
    list_text = load_file(path, name)
    list_reg = load_file(path, name_reg)

    # clf = MultinomialNB()
    # clf = svm.LinearSVC(C=1.0, random_state=0, class_weight='auto')
    clf = LogisticRegression()
    extend_clf_road_busstop_with_reg(list_text, list_reg, clf, K=5)
