__author__ = 'vdthoang'
from CRF_labeling.feature_crf_all import folder_files
from CRF_clf import featuers_CRF
from main.loadFile import load_file
from feature_crf import construct_ftr_CRF, load_target_label, n_cross_valid_crf
import numpy as np
import timeit
from CRF_labeling.filterText_CRF import filterTxt_CRF


if __name__ == '__main__':
    ############################################################################
    ############################################################################
    # USING FOR SGFORUMS DATASET
    # start = timeit.default_timer()  # get the start time
    #
    # # loading CRF features
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features/features'
    # files_ = folder_files(path_ftr)
    # features = featuers_CRF(files_, path_ftr)
    # X = np.array(construct_ftr_CRF(features))  # construct the features for CRF
    # print 'Finish loading features for CRF'
    #
    # # loading target labels
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    # name_ = 'Label_all_crf.txt'
    # list_line_ = load_file(path_, name_)
    # Y = np.array(load_target_label(list_line_))
    # print 'Finish loading target label'
    #
    # # running CRF models
    # n_cross_valid_crf(X, Y, K=2)
    # stop = timeit.default_timer()
    # print 'Finish running CRF model %.3f sec' % (stop - start)

    ############################################################################
    ############################################################################
    # USING FOR TWITTER DATASET

    ############################################################################
    # start = timeit.default_timer()  # get the start time
    #
    # # loading CRF features
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features'
    # files_ = folder_files(path_ftr)
    # features = featuers_CRF(files_, path_ftr)
    # X = np.array(construct_ftr_CRF(features))  # construct the features for CRF
    # print 'Finish loading features for CRF'
    #
    # # loading target labels
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    # name_ = 'labeling_all.txt'
    # list_line_ = filterTxt_CRF(load_file(path_, name_))
    # Y = np.array(load_target_label(list_line_))
    # print 'Finish loading target label'
    #
    # # running CRF models
    # # n_cross_valid_crf(X, Y, K=2, command='metrics_F1')  # use to calculate the F1 for classification
    # # n_cross_valid_crf(X, Y, K=2, command='confusion_matrix')  # use to calculate the F1 for classification
    # n_cross_valid_crf(X, Y, K=2, command='write_results')  # use to calculate the confusion matrix
    #
    # stop = timeit.default_timer()
    # print 'Finish running CRF model %.3f sec' % (stop - start)

    ############################################################################
    # start = timeit.default_timer()  # get the start time
    #
    # # loading CRF features
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLink'
    # files_ = folder_files(path_ftr)
    # features = featuers_CRF(files_, path_ftr)
    # X = np.array(construct_ftr_CRF(features))  # construct the features for CRF
    # print 'Finish loading features for CRF'
    #
    # # loading target labels
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    # name_ = 'labeling_all.txt'
    # list_line_ = filterTxt_CRF(load_file(path_, name_), command='removeLink')
    # Y = np.array(load_target_label(list_line_))
    # print 'Finish loading target label'
    #
    # # running CRF models
    # # n_cross_valid_crf(X, Y, K=5, command='metrics_F1')  # use to calculate the F1 for classification
    # # n_cross_valid_crf(X, Y, K=5, command='confusion_matrix')  # use to calculate the F1 for classification
    # n_cross_valid_crf(X, Y, K=5, command='write_results')  # use to calculate the confusion matrix
    #
    # stop = timeit.default_timer()
    # print 'Finish running CRF model %.3f sec' % (stop - start)

    ############################################################################
    ############################################################################
    # USING FOR FACEBOOK DATASET

    ############################################################################
    start = timeit.default_timer()  # get the start time

    # loading CRF features
    path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF/crf_features/features'
    files_ = folder_files(path_ftr)
    features = featuers_CRF(files_, path_ftr)
    X = np.array(construct_ftr_CRF(features))  # construct the features for CRF
    print 'Finish loading features for CRF'

    # loading target labels
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF'
    name_ = 'label.txt'
    list_line_ = filterTxt_CRF(load_file(path_, name_), command='removePunc')
    Y = np.array(load_target_label(list_line_))
    print 'Finish loading target label'

    # running CRF models
    # n_cross_valid_crf(X, Y, K=5, command='metrics_F1')  # use to calculate the F1 for classification
    # n_cross_valid_crf(X, Y, K=5, command='confusion_matrix')  # use to calculate the F1 for classification
    n_cross_valid_crf(X, Y, K=5, command='write_results')  # use to calculate the confusion matrix

    stop = timeit.default_timer()
    print 'Finish running CRF model %.3f sec' % (stop - start)
