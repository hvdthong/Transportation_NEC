__author__ = 'vdthoang'
from main.loadFile import load_file
from CRF_labeling.filterText_CRF import filterTxt_CRF
from CRF_labeling.feature_crf_all import folder_files
from CRF_labeling.CRF_clf import featuers_CRF, convert_ftr_x_clf
import numpy as np
from main.writeFile import write_file


def checking_line(lines):
    for i in xrange(0, len(lines), 3):
        split_line = lines[i].split()
        split_label = lines[i + 1].split()
        print str(len(split_line)) + '\t' + str(len(split_label))


def all_word(lines):
    words = list()
    for i in xrange(0, len(lines), 3):
        split_line = lines[i].split()
        for w in split_line:
            if w.lower() not in words:
                words.append(w.lower())
    return words


def wordVector_storage(vec):
    dict_word, vec_word = list(), list()
    for i in xrange(0, len(vec)):
        split_v = vec[i].split()
        dict_word.append(split_v[0])
        vec_word.append(split_v[1:])
    return dict_word, vec_word


def construct_ftr_wordVector(dict_w, vec_w, lines, path_write, name_write):
    word_lines = list()
    for i in xrange(0, len(lines), 3):
        split_line = lines[i].lower().split('\t')
        word_lines.append(split_line)

    nftr_wordVec = len(vec_w[0])  # number of features in word vector
    for nfr in xrange(nftr_wordVec):
        frt_wordVec = list()
        for i in xrange(0, len(word_lines)):
            wordvec_score = ''
            w_line = word_lines[i]
            for j in xrange(0, len(w_line)):
                word = w_line[j]
                if word in dict_w:
                    index_ = dict_w.index(word)
                    scores_ = vec_w[index_]
                    ftr_score = scores_[nfr]
                    # print index_, word, ftr_score
                    wordvec_score += ftr_score + '\t'
                else:
                    word = '@' + word
                    if word in dict_w:
                        index_ = dict_w.index(word)
                        scores_ = vec_w[index_]
                        ftr_score = scores_[nfr]
                        # print index_, word, ftr_score
                        wordvec_score += ftr_score + '\t'
                    else:
                        # print word, '0'
                        wordvec_score += '0' + '\t'
            frt_wordVec.append(wordvec_score)
        # print len(frt_wordVec)
        # all_ftrWordVec.append(frt_wordVec)
        write_file(path_write, name_write + '_%i' % nfr, frt_wordVec)


def construct_oldfeatures(path, files, path_write):
    for f in files:
        list_ = load_file(path, f)
        list_convert = list()

        for line in list_:
            string = ''
            for c in line:
                string += c + '\t'
            list_convert.append(string.strip())
        print f
        write_file(path_write, f.replace('.csv', ''), list_convert)


if __name__ == '__main__':
    ####################################################################################################################
    ## create word vector
    # path_wordVec = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/WordVector'
    # name_wordVec = 'word_vec.csv'

    path_wordVec = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/WordVector'
    # name_wordVec = 'word_vec_70.csv'
    # name_wordVec = 'word_vec_100.csv'
    # name_wordVec = 'word_vec_150.csv'
    name_wordVec = 'word_vec_200.csv'
    vec = load_file(path_wordVec, name_wordVec)
    dict_w, vec_w = wordVector_storage(vec)
    # # print len(dict_w), len(vec_w)
    # #
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    name_ = 'labeling_all.txt'
    list_line_ = filterTxt_CRF(load_file(path_, name_), 'removeLink', 'model')  # remove all punctuations & links
    words = all_word(list_line_)
    # # print len(words)
    #
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLinkWordVector'
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLinkWordVector/wordVec_100'
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLinkWordVector/wordVec_150'
    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLinkWordVector/wordVec_200'
    name_write = 'ftr_wordVec'
    construct_ftr_wordVector(dict_w, vec_w, list_line_, path_write, name_write)

    ## set up format of old features so they have to be similar with word vector features
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLink'
    # path_w = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLinkWordVector'
    # files_ = folder_files(path_ftr)
    # construct_oldfeatures(path_ftr, files_, path_w)


    ####################################################################################################################
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLink'
    # name_ftr = 'ftr_isBusPlate.csv'
    # list_ = load_file(path_ftr, name_ftr)
    # leng_ = [len(list_[i].strip()) for i in xrange(0, len(list_))]
    # for value in leng_:
    #     print value

    # # loading CRF features, remember that we only remove all punctuation and links in Twitter
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLink'
    # files_ = folder_files(path_ftr)
    # features = featuers_CRF(files_, path_ftr)
    # X = np.array(convert_ftr_x_clf(features))
    # print len(X)
    #

    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    # name_ = 'labeling_all.txt'
    # list_line_ = filterTxt_CRF(load_file(path_, name_), 'removeLink', 'model')  # remove all punctuations & links
    # checking_line(list_line_)