__author__ = 'vdthoang'
from main.loadFile import load_file
from CRF_labeling.feature_crf import load_target_label, convert_list_CRF
from sklearn.metrics import confusion_matrix
from CRF_labeling.filterText_CRF import filterTxt_CRF


def convert_label_CRF(list_, command):
    list_convert = list()
    if command == 'svc':
        for value in list_:
            if int(value) == 0:
                list_convert.append(int(value))
            elif int(value) == 1:
                list_convert.append(1)
            else:
                print 'Something wrong with your file'
                quit()
    elif command == 'road':
        for value in list_:
            if int(value) == 0:
                list_convert.append(int(value))
            elif int(value) == 1:
                list_convert.append(2)
            else:
                print 'Something wrong with your file'
                quit()
    elif command == 'busstop':
        for value in list_:
            if int(value) == 0:
                list_convert.append(int(value))
            elif int(value) == 1:
                list_convert.append(3)
            else:
                print 'Something wrong with your file'
                quit()
    else:
        print 'Please give a correct command'
        quit()

    return list_convert


def CRF_F1_reg(list_line, list_svc, list_road, list_busstop):
    num_label = list()
    for label in list_line:
        if label not in num_label:
            num_label.append(label)
    labels = sorted(num_label)  # we collect all the labels

    list_merge = list()
    for i in range(0, len(list_svc)):
        list_max = list()
        svc, road, busstop = list_svc[i], list_road[i], list_busstop[i]
        list_max.append(svc)
        list_max.append(road)
        list_max.append(busstop)

        max_value = max(list_max)
        list_merge.append(max_value)

    matrix = confusion_matrix(list_merge, list_line)
    for value in matrix:
        text = ''
        for each in value:
            text += str(each) + '\t'
        print text.strip()


def loading_reg_ftr(list_line_, command):
    if command == 'sgforums':
        path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features/features'
    elif command == 'twitter':
        path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLink'
    elif command == 'facebook':
        path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF/crf_features/features'
    else:
        print 'You need to give the correct command'
        quit()

    name_svc = 'ftr_reg_svc.csv'
    name_road = 'ftr_reg_match_road.csv'
    name_busstop = 'ftr_reg_match_busstop.csv'

    list_svc = convert_label_CRF(convert_list_CRF(load_file(path_, name_svc)), 'svc')
    list_road = convert_label_CRF(convert_list_CRF(load_file(path_, name_road)), 'road')
    list_busstop = convert_label_CRF(convert_list_CRF(load_file(path_, name_busstop)), 'busstop')
    CRF_F1_reg(list_line_, list_svc, list_road, list_busstop)


if __name__ == '__main__':
    # Calculate the F1 of regular expression
    # SGFORUMS
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    # name_ = 'Label_all_crf.txt'
    # list_line = convert_list_CRF(load_target_label(load_file(path, name_)))
    # loading_reg_ftr(list_line, command='sgforums')

    # TWITTER
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    # name_ = 'labeling_all.txt'
    # list_line = convert_list_CRF(load_target_label(filterTxt_CRF(load_file(path_, name_), command='removeLink')))
    # loading_reg_ftr(list_line, command='twitter')

    # FACEBOOK
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF'
    name_ = 'label.txt'
    list_line = convert_list_CRF(load_target_label(filterTxt_CRF(load_file(path_, name_), command='removePunc')))
    loading_reg_ftr(list_line, command='facebook')
