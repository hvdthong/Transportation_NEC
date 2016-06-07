__author__ = 'vdthoang'
from main.loadFile import load_file
from CRF_labeling.CRF_POS import create_part_of_speech, intersection_POS_CRF
from CRF_labeling.filterText_CRF import filterTxt_CRF
from CRF_running import folder_files, featuers_CRF, construct_ftr_CRF, load_target_label, n_cross_valid_crf
import numpy as np


if __name__ == '__main__':
    # TWITTER
    # get the text for part-of-speech and our lablled data
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    name_POS = 'labeling_text_POS.txt'
    name_CRF = 'labeling_all.txt'

    list_ = load_file(path, name_POS)
    list_all = create_part_of_speech(list_)
    list_POS = filterTxt_CRF(list_all, command='removeLink', command_data='twitter')
    list_CRF = filterTxt_CRF(load_file(path, name_CRF), command='removeLink', command_data='twitter')

    list_new = intersection_POS_CRF(list_POS, list_CRF)
    list_new_POS, list_new_CRF = list_new[0], list_new[1]  # note that part-of-speech will have same length now
    list_line_ = list_new_CRF

    # loading CRF features
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_POS'
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_POS_withoutREG'
    path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_without_POS_RE'
    files_ = folder_files(path_ftr)
    features = featuers_CRF(files_, path_ftr)
    X = np.array(construct_ftr_CRF(features))  # construct the features for CRF
    print X.shape
    print 'Finish loading features for CRF'

    # loading target labels
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    name_ = 'labeling_all.txt'
    Y = np.array(load_target_label(list_line_))
    print Y.shape
    print 'Finish loading target label'

    # n_cross_valid_crf(X, Y, K=5, command='metrics_F1')  # use to calculate the F1 for classification
    n_cross_valid_crf(X, Y, K=5, command='confusion_matrix')  # use to calculate the confusion matrix of CRFs
