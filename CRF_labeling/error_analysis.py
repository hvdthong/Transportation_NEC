__author__ = 'vdthoang'
from main.loadFile import load_file
import sys
from CRF_labeling.filterText_CRF import filterTxt_CRF


# make the default is 'utf-8'
reload(sys)
sys.setdefaultencoding('utf8')


def load_results_clf(list_clf):
    list_pred = list()
    list_truth = list()
    for index in range(1, len(list_clf)):
        split_index = list_clf[index].split('\t')
        pred, truth = split_index[1], split_index[2]

        list_pred.append(pred)
        list_truth.append(truth)

    list_return = list()
    list_return.append(list_pred)
    list_return.append(list_truth)
    return list_return


def load_results_CRF(list_crf):
    list_pred = list()
    list_truth = list()
    for index in range(1, len(list_crf)):
        split_index = list_crf[index].split('\t')
        pred, truth = split_index[0], split_index[1]

        list_pred.append(pred)
        list_truth.append(truth)

    list_return = list()
    list_return.append(list_pred)
    list_return.append(list_truth)
    return list_return


def load_text(list_line):
    list_word = []
    cnt = 0
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')  # get the sentences
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        index = cnt
        for word in split_first:
            list_ = list()
            list_.append(index)
            list_.append(word)
            list_word.append(list_)
        cnt += 1
    return list_word


def get_CRFwrong_CLFright(list_crf, list_clf, list_truth, list_text):
    # print len(list_crf), len(list_clf), len(list_truth), len(list_text)
    for i in range(0, len(list_crf)):
        crf, clf, truth = int(list_crf[i]), int(list_clf[i]), int(list_truth[i])
        if (crf != truth) and (clf == truth) and (crf != 0):
            print crf, clf, truth, list_text[i]
    return None


def get_CRFright_CLFwrong(list_crf, list_clf, list_truth, list_text):
    for i in range(0, len(list_crf)):
        crf, clf, truth = int(list_crf[i]), int(list_clf[i]), int(list_truth[i])
        if (crf == truth) and (clf != truth) and (crf != 0):
            print crf, clf, truth, list_text[i]


if __name__ == '__main__':
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    # name_clf = 'result_LogReg.txt'
    # name_crf = 'result_CRF.txt'
    # name_file = 'Label_all_crf.txt'
    #
    # list_clf = load_results_clf(load_file(path_, name_clf))
    # list_crf = load_results_CRF(load_file(path_, name_crf))
    # list_word = load_text(load_file(path_, name_file))
    #
    # # get_CRFwrong_CLFright(list_crf[0], list_clf[0], list_crf[1], list_word)
    # get_CRFright_CLFwrong(list_crf[0], list_clf[0], list_crf[1], list_word)

    ############################################################################
    ############################################################################
    # USING FOR TWITTER DATASET
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    name_clf = 'results_LR_twitter.txt'
    name_crf = 'results_CRF_twitter.txt'
    name_file = 'labeling_all.txt'

    list_clf = load_results_clf(load_file(path_, name_clf))
    list_crf = load_results_CRF(load_file(path_, name_crf))
    list_word = load_text(filterTxt_CRF(load_file(path_, name_file)))

    # get_CRFwrong_CLFright(list_crf[0], list_clf[0], list_crf[1], list_word)
    get_CRFright_CLFwrong(list_crf[0], list_clf[0], list_crf[1], list_word)

