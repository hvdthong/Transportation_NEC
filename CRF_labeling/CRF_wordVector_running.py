__author__ = 'vdthoang'
import timeit
import numpy as np
from CRF_labeling.feature_crf_all import folder_files
from CRF_clf import featuers_CRF
from feature_crf import n_cross_valid_crf, load_target_label
from main.loadFile import load_file
from CRF_labeling.filterText_CRF import filterTxt_CRF


def construct_ftr_CRF_wordVector(list_all):
    # construct the features for running CRF

    # nsents, nftrs = len(list_all[0]), len(list_all)
    # print nsents, nftrs

    i = 0
    list_combine = []
    while i <= len(list_all) - 1:
        if i == 0:
            list_first = list_all[i]
            list_second = list_all[i + 1]

            for j in range(0, len(list_first)):
                first = list_first[j].split('\t')
                second = list_second[j].split('\t')
                combine = map('\t'.join, zip(first, second))
                list_combine.append(combine)
            i += 2
        else:
            list_ = list_all[i]
            for j in range(0, len(list_)):
                first = list_combine[j]
                second = list_[j].split('\t')
                combine = map('\t'.join, zip(first, second))
                list_combine[j] = combine
            i += 1

    list_all_sentences = []
    for i in range(0, len(list_combine)):
        sentence = list_combine[i]
        # print sentence
        list_ftr_sentence = []
        for word in sentence:
            ftr_word = []
            for ftr in word.split('\t'):
                ftr_word.append(float(ftr))
            list_ftr_sentence.append(ftr_word)

        num_list_sentence = np.array(list_ftr_sentence)  # IMPORTANT. We need to convert to array before adding to list
        list_all_sentences.append(num_list_sentence)
    return list_all_sentences


if __name__ == '__main__':
    start = timeit.default_timer()  # get the start time

    # loading CRF features
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLinkWordVector/wordVec_30'
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLinkWordVector/wordVec_70'
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLinkWordVector/wordVec_100'
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLinkWordVector/wordVec_150'
    path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLinkWordVector/wordVec_200'
    files_ = folder_files(path_ftr)
    features = featuers_CRF(files_, path_ftr)
    # construct_ftr_CRF_wordVector(features)
    X = np.array(construct_ftr_CRF_wordVector(features))  # construct the features for CRF
    print X.shape
    print 'Finish loading features for CRF'
    #
    # # loading target labels
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    name_ = 'labeling_all.txt'
    list_line_ = filterTxt_CRF(load_file(path_, name_), 'removeLink', 'model')
    Y = np.array(load_target_label(list_line_))
    print Y.shape
    print 'Finish loading target label'
    #
    # # for index in range(0, len(X)):
    # #     print len(X[index]), len(Y[index])
    #
    # # running CRF models
    # n_cross_valid_crf(X, Y, K=5, command='metrics_F1')  # use to calculate the F1 for classification
    n_cross_valid_crf(X, Y, K=5, command='confusion_matrix')  # use to calculate the F1 for classification
    # # n_cross_valid_crf(X, Y, K=5, command='write_results')  # use to calculate the confusion matrix
    #
    # stop = timeit.default_timer()
    # print 'Finish running CRF model %.3f sec' % (stop - start)