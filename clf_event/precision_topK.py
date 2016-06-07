__author__ = 'vdthoang'
from main.loadFile import load_file


def pre_at_topK(list_, list_topK):
    for K in list_topK:
        list_top = list_[:K]
        count = 0
        for line in list_top:
            split_line = line.split('\t')
            if int(split_line[2]) == int(split_line[3]):
                count += 1

        print str(K) + '\t' + str(count / float(K))

if __name__ == '__main__':
    # SGFORUMS
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_classification_events/detectAllEvents_ver2'
    # name = 'bunch_ftrMatch_LR_probScore.csv'
    name = 'crowd_ftrMatch_LR_probScore.csv'

    # FACEBOOK
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event/detectAllEvents_ver2'
    # name = 'complaint_LR_probScore.csv'
    # name = 'compliment_LR_probScore.csv'
    # name = 'skip_LR_probScore.csv'
    # name = 'suggestion_LR_probScore.csv'
    # name = 'wait_LR_probScore.csv'

    list_topK = list()
    for value in range(0, 20):
        list_topK.append((value + 1) * 5)

    list_ = load_file(path, name)
    print len(list_)

    pre_at_topK(list_, list_topK)
