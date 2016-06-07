__author__ = 'vdthoang'


from main.loadFile import load_file
import sys

# make the default is 'utf-8'
reload(sys)
sys.setdefaultencoding('utf8')


def load_eventResult(results):
    all, preds, truths, texts = list(), list(), list(), list()
    for value in results:
        split_value = value.split('\t')
        preds.append(split_value[1].strip()), truths.append(split_value[2].strip()), texts.append(split_value[3].strip())

    all.append(preds), all.append(truths), all.append(texts)
    return all


def get_CLFWrong_MatchRight(list_clf, list_matching, list_truth, list_text):
    # print len(list_crf), len(list_clf), len(list_truth), len(list_text)
    for i in range(0, len(list_clf)):
        clf, matching, truth = int(list_clf[i]), int(list_matching[i]), int(list_truth[i])
        if (clf != truth) and (matching == truth) and ((truth == 1) or (clf != 0)):
            print clf, matching, truth, list_text[i]
    return None


def get_CLFRigtht_MatchWrong(list_clf, list_matching, list_truth, list_text):
    for i in range(0, len(list_clf)):
        clf, matching, truth = int(list_clf[i]), int(list_matching[i]), int(list_truth[i])
        if (clf == truth) and (matching != truth) and ((clf == 0) or (clf == 1)):
            print clf, matching, truth, list_text[i]


if __name__ == '__main__':
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver2'

    # name_clf = 'missing_SVM.csv'
    # name_matching = 'missing_match.csv'
    # name_clf = 'slow_SVM.csv'
    # name_matching = 'slow_match.csv'
    name_clf = 'wait_LR.csv'
    name_matching = 'wait_match.csv'

    list_clf = load_file(path_, name_clf)
    clf_results = load_eventResult(list_clf)
    list_matching = load_file(path_, name_matching)
    matching_results = load_eventResult(list_matching)
    get_CLFWrong_MatchRight(clf_results[0], matching_results[0], clf_results[1], clf_results[2])
    # get_CLFRigtht_MatchWrong(clf_results[0], matching_results[0], clf_results[1], clf_results[2])

