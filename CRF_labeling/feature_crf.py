__author__ = 'vdthoang'
from main.loadFile import load_file
import sys
import re
from classification_busService.ftr_bussvc_extraction import range_text_index
from main.pattern_busService import pattern_bus_service_ver2
from crawl.abbreviation import pattern_match
import numpy as np
from pystruct.models import ChainCRF
from pystruct.learners import FrankWolfeSSVM
from sklearn.cross_validation import KFold
from sklearn import metrics
import timeit
from main.writeFile import write_file
from sklearn.metrics import confusion_matrix
from operator import itemgetter



# make the default is 'utf-8'
reload(sys)
sys.setdefaultencoding('utf8')


#########################################################################
#########################################################################
# load dictionary of different feature types: 'service', 'road', 'bus stop'
def load_dict(command):
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features'
    if command == 'svc':
        name = 'dict_bussvc.txt'
        list_svc = load_file(path, name)
        return list_svc
    elif command == 'road':
        name = 'dict_road.txt'
        list_road = load_file(path, name)
        return list_road
    elif command == 'busstop':
        name = 'dict_busstop.txt'
        list_stop = load_file(path, name)
        return list_stop

    return 'You need to give correct command'


def match_dict(list_line, command):
    # matching the dictionary for type: 'service', 'road', 'bus stop'
    list_ftr = []
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        feature = ''
        if command == 'svc':
            list_svc = load_dict('svc')
            for value in split_first:
                if value.strip() in list_svc:
                    feature += '1'
                else:
                    feature += '0'
            # print len(split_first), split_first
            # print len(feature), feature
            list_ftr.append(feature)
        elif command == 'road':
            list_road = load_dict(command)
            for value in split_first:
                if value.strip().lower() in list_road:
                    feature += '1'
                else:
                    feature += '0'
            # print len(split_first), split_first
            # print len(feature), feature
            list_ftr.append(feature)
        elif command == 'busstop':
            list_busstop = load_dict(command)
            for value in split_first:
                if value.strip().lower() in list_busstop:
                    feature += '1'
                else:
                    feature += '0'
            # print len(split_first), split_first
            # print len(feature), feature
            list_ftr.append(feature)
    # print len(list_ftr)
    return list_ftr


def isCapitalize(list_line):
    # check if the token begin with the capitalize letter or not
    list_ftr = []
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        feature = ''
        for value in split_first:
            if value[0].isupper() is True:
                feature += '1'
            else:
                feature += '0'
        # print len(split_first), split_first
        # print len(feature), feature
        list_ftr.append(feature)
    return list_ftr


#######################################################################################
#######################################################################################
# check regular expression for bus service
def pattern_token_bussvc(token):  # use for each token
    pattern_1 = r'[s][v][0-9]+\b'
    pattern_2 = r'[s][v][0-9]+[A-z]{1}\b'
    pattern_3 = r'[s][v][c][0-9]+[A-z]{1}\b'

    list_svc = load_dict('svc')

    if (re.match(pattern_1, token)) or (re.match(pattern_2, token)):
        token = token[2:]
        if token.lower() in list_svc:
            return True
    elif re.match(pattern_3, token):
        token = token[3:]
        if token.lower() in list_svc:
            return True

    elif (len(token) >= 3) and (token.lower() in list_svc):
        return True

    else:
        return False


def pattern_tokenText_bussvc(token, text):
    list_svc = load_dict('svc')
    list_patt = pattern_bus_service_ver2(text, list_svc)
    if token in list_patt:
        return True
    else:
        return False


def reg_bussvc(list_line, n_token):
    # check if the token match the regular expression for bus service or not
    list_ftr = []
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        ftr = ''
        for k in range(0, len(split_first)):
            token = split_first[k].strip()
            if pattern_token_bussvc(token) is True:
                ftr += '1'
            else:
                range_k = range_text_index(k, len(split_second), n_token)
                token_text = ''
                for m in range(range_k[1], range_k[2] + 1):
                    token_text = token_text + ' ' + split_first[m]

                token_text = token_text.strip()

                if pattern_tokenText_bussvc(token, token_text):
                    ftr += '1'
                else:
                    ftr += '0'
        # print len(split_first), split_first
        # print len(ftr), ftr
        list_ftr.append(ftr)
    return list_ftr


#######################################################################################
#######################################################################################
def matching(text, command):
    list_ = []  # list can be road or bus stop belong to the command
    if command == 'road':
        path_road = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
        name_road = 'road_abbrevation_all.csv'
        list_ = load_file(path_road, name_road)
    elif command == 'busstop':
        path_stop = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
        name_busstop = 'bus_stop_crf.csv'  # delete the header of file bus stop
        list_ = load_file(path_stop, name_busstop)

    list_element = []
    for index in range(0, len(list_)):
        ele = list_[index].lower()
        split_road = ele.split(';')

        for road in split_road:
            if pattern_match(road, text) is True:
                list_element.append(road)
                break

    list_token_element = []
    for element in list_element:
        split_ = element.split()
        for value in split_:
            list_token_element.append(value)
    return list_token_element


def match_road_busstop(list_line, command):
    # match with road and bus stop name
    list_ftr = []
    # start = timeit.default_timer()
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        ftr = ''
        text = ''
        for k in range(0, len(split_first)):
            text = text + ' ' + split_first[k]
        text = text.strip()
        list_token_road = matching(text.lower(), command)

        for k in range(0, len(split_first)):
            token = split_first[k].lower().strip()
            if token in list_token_road:
                ftr += '1'
            else:
                ftr += '0'
        # print len(split_first), split_first
        # print len(ftr), ftr
        list_ftr.append(ftr)
    # stop = timeit.default_timer()
    # print 'Time for running is: %.3f sec' % (stop - start)
    return list_ftr


##################################################################################
##################################################################################
def load_dic_token_bef(command):
    list_token_bef = []
    if command == 'svc':
        path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features'
        name = 'tok_bef_bussvc.txt'
        list_token_bef = load_file(path, name)
    elif command == 'road':
        path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features'
        name = 'tok_bef_road.txt'
        list_token_bef = load_file(path, name)
    elif command == 'busstop':
        path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features'
        name = 'tok_bef_busstop.txt'
        list_token_bef = load_file(path, name)
    return list_token_bef


def matching_token_bef(list_line, command):
    # check the token before the label
    list_ftr = []
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        ftr = ''
        for k in range(0, len(split_first)):
            if k == 0:
                ftr += '0'
            else:
                if command == 'svc':
                    list_svc_token_bef = load_dic_token_bef(command)
                    token_bef = split_first[k - 1].strip().lower()
                    if token_bef in list_svc_token_bef:
                        ftr += '1'
                    else:
                        pattern_busplate = r'\b[A-z]{3}[0-9]+[A-z]{1}\b'
                        if re.match(pattern_busplate, token_bef):
                            ftr += '1'
                        else:
                            ftr += '0'
                elif command == 'road':
                    list_road_token_bef = load_dic_token_bef(command)
                    list_road_dict = load_dict(command)
                    token_bef = split_first[k - 1].strip().lower()

                    if (token_bef in list_road_token_bef) or (token_bef in list_road_dict):
                        ftr += '1'
                    else:
                        ftr += '0'
                elif command == 'busstop':
                    list_stop_token_bef = load_dic_token_bef(command)
                    list_stop_dict = load_dict(command)
                    token_bef = split_first[k - 1].strip().lower()

                    if (token_bef in list_stop_token_bef) or (token_bef in list_stop_dict):
                        ftr += '1'
                    else:
                        ftr += '0'

        # print len(split_first), split_first
        # print len(ftr), ftr
        list_ftr.append(ftr)
    return list_ftr


##################################################################################
##################################################################################
def load_dic_token_aft(command):
    list_token_aft = []
    if command == 'svc':
        path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features'
        name = 'tok_aft_bussvc.txt'
        list_token_aft = load_file(path, name)
    return list_token_aft


def matching_token_aft(list_line, command):
    # check the token before the label
    list_ftr = []
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        ftr = ''
        for k in range(0, len(split_first)):
            if k == len(split_first) - 1:
                ftr += '0'
            else:
                if command == 'svc':
                    list_token_aft = load_dic_token_aft(command)
                    token_aft = split_first[k + 1].strip().lower()
                    if token_aft in list_token_aft:
                        ftr += '1'
                    else:
                        ftr += '0'
        # print len(split_first), split_first
        # print len(ftr), ftr
        list_ftr.append(ftr)
    return list_ftr


##################################################################################
##################################################################################
def construct_ftr_CRF(list_all):
    # construct the features for running CRF
    i = 0
    list_combine = []
    while i <= len(list_all) - 1:
        if i == 0:
            list_first = list_all[i]
            list_second = list_all[i + 1]

            for j in range(0, len(list_first)):
                first = list_first[j]
                second = list_second[j]
                combine = map(''.join, zip(first, second))
                list_combine.append(combine)
            i += 2
        else:
            list_ = list_all[i]
            for j in range(0, len(list_)):
                first = list_combine[j]
                second = list_[j]
                combine = map(''.join, zip(first, second))
                list_combine[j] = combine
            i += 1

    list_all_sentences = []
    for i in range(0, len(list_combine)):
        sentence = list_combine[i]
        list_ftr_sentence = []
        for word in sentence:
            ftr_word = []
            for ftr in word:
                ftr_word.append(int(ftr))
            list_ftr_sentence.append(ftr_word)

        num_list_sentence = np.array(list_ftr_sentence)  # IMPORTANT. We need to convert to array before adding to list
        list_all_sentences.append(num_list_sentence)

    return list_all_sentences


def load_target_label(list_line):
    # load target label for CRF
    list_all_label = []
    for i in range(0, len(list_line), 3):
        list_label = []
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        for label in split_second:
            list_label.append(int(label.strip()))

        num_list_label = np.array(list_label)  # IMPORTANT. We need to convert to array before adding to list
        list_all_label.append(num_list_label)
    return list_all_label


##################################################################################
##################################################################################
def metrics_crf(y_test, y_pred):  # we know that we have 4 labels
    num_label = []
    for line in y_test:
        for label in line:
            if label not in num_label:
                num_label.append(label)
    labels = sorted(num_label)
    for label in labels:
        TT, TF, FT, FF = 0, 0, 0, 0
        for i in range(0, len(y_test)):
            pred = y_pred[i]
            test = y_test[i]

            for j in range(0, len(test)):
                if (pred[j] == test[j]) and (test[j] == label) and (pred[j] == label):
                    TT += 1
                elif (pred[j] != test[j]) and (test[j] != label) and (pred[j] == label):
                    TF += 1
                elif (pred[j] != test[j]) and (test[j] == label) and (pred[j] != label):
                    FT += 1
                elif (test[j] != pred[j]) and (test[j] != label) and (pred[j] != label):
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


def n_cross_valid_crf(X, Y, K):
    # cross validation for crf
    # list_write = []
    cv = KFold(len(X), K, shuffle=True, random_state=0)
    for traincv, testcv in cv:
        x_train, x_test = X[traincv], X[testcv]
        y_train, y_test = Y[traincv], Y[testcv]

        crf = ChainCRF(inference_method='max-product', directed=True, class_weight=None)
        ssvm = FrankWolfeSSVM(model=crf, C=1.0, max_iter=100)
        ssvm.fit(x_train, y_train)
        y_pred = ssvm.predict(x_test)

        print 'Accuracy of linear-crf %f:' % ssvm.score(x_test, y_test)
        metrics_crf(y_test, y_pred)
        # confusion_matrix_CRF(y_test, y_pred)
        # list_write += write_results_CRF(testcv, y_test, y_pred)

        print '------------------------------------------------------'
        print '------------------------------------------------------'

    # list_write = sorted(list_write, key=itemgetter(0))  # sorted list based on index
    # for value in list_write:
    #     pred_list = value[1]
    #     test_list = value[2]
    #
    #     for i in range(0, len(pred_list)):
    #         print str(pred_list[i]) + '\t' + str(test_list[i])


##################################################################################
##################################################################################
def convert_list_CRF(list_label):
    list_ = []
    for sentence in list_label:
        for word in sentence:
            list_.append(word)
    return list_


def confusion_matrix_CRF(y_test, y_pred):
    print len(y_test), len(y_pred)
    list_test = convert_list_CRF(y_test)
    list_pred = convert_list_CRF(y_pred)
    matrix = confusion_matrix(list_pred, list_test)
    for value in matrix:
        text = ''
        for each in value:
            text += str(each) + '\t'
        print text.strip()


##################################################################################
##################################################################################
def write_results_CRF(list_index, y_test, y_pred):  # remember the index is the index of sentence
    list_write = []
    for i in range(0, len(list_index)):
        list_ = []
        index, pred, test = list_index[i], y_pred[i], y_test[i]
        list_.append(index)
        list_.append(pred)
        list_.append(test)
        list_write.append(list_)
    return list_write


##################################################################################
##################################################################################
def metrics_crf_candidate(sentences, y_test, y_pred):
    list_label = ['svc', 'road', 'busstop']
    list_wrong_svc = []
    list_wrong_road = []
    list_wrong_busstop = []

    list_good_svc = []
    list_good_road = []
    list_good_busstop = []
    for label in list_label:
        list_dict = load_dict(label)
        TT, TF, FT, FF = 0, 0, 0, 0
        for i in range(0, len(sentences)):
            sentence = sentences[i]
            pred = y_pred[i]
            truth = y_test[i]

            if label == 'svc':
                for j in range(0, len(sentence)):
                    word = sentence[j]
                    if word in list_dict:  # this word in list of candidate
                        value_pred = pred[j]
                        value_truth = truth[j]

                        if value_pred == value_truth and value_pred == 1:
                            TT += 1
                            string = ' '.join(sentence)
                            # print word + '\t' + string
                            list_good_svc.append(word + '\t' + string)
                        elif value_pred != value_truth and value_pred == 1:
                            TF += 1
                            string = ' '.join(sentence)
                            # print word + '\t' + string
                            list_wrong_svc.append(word + '\t' + string)
                        elif value_pred != value_truth and value_truth == 1:
                            FT += 1
                            string = ' '.join(sentence)
                            # print word + '\t' + string
                            list_wrong_svc.append(word + '\t' + string)
                        elif value_pred != 1 and value_truth != 1:
                            FF += 1
            elif label == 'road':
                for j in range(0, len(sentence)):
                    word = sentence[j].strip().lower()
                    if (int(pred[j] == 2)) or (word.strip().lower() in list_dict):
                        value_pred = pred[j]
                        value_truth = truth[j]

                        if value_pred == value_truth and value_pred == 2:
                            TT += 1
                            string = ' '.join(sentence)
                            # print word + '\t' + string
                            list_good_road.append(word + '\t' + string)
                        elif value_pred != value_truth and value_pred == 2:
                            TF += 1
                            string = ' '.join(sentence)
                            # print word + '\t' + string
                            list_wrong_road.append(word + '\t' + string)
                        elif value_pred != value_truth and value_truth == 2:
                            FT += 1
                            string = ' '.join(sentence)
                            # print word + '\t' + string
                            list_wrong_road.append(word + '\t' + string)
                        elif value_pred != 2 and value_truth != 2:
                            FF += 1
            elif label == 'busstop':
                for j in range(0, len(sentence)):
                    word = sentence[j]
                    if (int(pred[j] == 2)) or (word.strip().lower() in list_dict):
                        value_pred = pred[j]
                        value_truth = truth[j]

                        if value_pred == value_truth and value_pred == 3:
                            TT += 1
                            string = ' '.join(sentence)
                            # print word + '\t' + string
                            list_good_busstop.append(word + '\t' + string)
                        elif value_pred != value_truth and value_pred == 3:
                            TF += 1
                            string = ' '.join(sentence)
                            # print word + '\t' + string
                            list_wrong_busstop.append(word + '\t' + string)
                        elif value_pred != value_truth and value_truth == 3:
                            FT += 1
                            string = ' '.join(sentence)
                            # print word + '\t' + string
                            list_wrong_busstop.append(word + '\t' + string)
                        elif value_pred != 3 and value_truth != 3:
                            FF += 1

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

    list_write_wrong = []
    list_write_wrong.append(list_wrong_svc)
    list_write_wrong.append(list_wrong_road)
    list_write_wrong.append(list_wrong_busstop)

    list_good = []
    list_good.append(list_good_svc)
    list_good.append(list_good_road)
    list_good.append(list_good_busstop)

    # return list_write_wrong
    return list_good


def n_cross_valid_crf_candidate(list_line, X, Y, K):
    list_text = []
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        list_text.append(split_first)

    list_text = np.array(list_text)

    cv = KFold(len(X), K, shuffle=True, random_state=0)
    list_write = []
    for traincv, testcv in cv:
        x_train, x_test = X[traincv], X[testcv]
        y_train, y_test = Y[traincv], Y[testcv]
        list_text_train, list_text_test = list_text[traincv], list_text[testcv]

        crf = ChainCRF(inference_method='max-product', directed=False, class_weight=None)
        ssvm = FrankWolfeSSVM(model=crf, C=1.0, max_iter=10)
        ssvm.fit(x_train, y_train)
        y_pred = ssvm.predict(x_test)
        list_wrong = metrics_crf_candidate(list_text_test, y_test, y_pred)
        if len(list_write) == 0:
            list_write = list_wrong
        else:
            for i in range(0, len(list_wrong)):
                svc = list_wrong[0]
                road = list_wrong[1]
                busstop = list_wrong[2]

                list_write[0] = list_write[0] + svc
                list_write[1] = list_write[1] + road
                list_write[2] = list_write[2] + busstop

    # write_file('d:/', 'wrong_svc', list_write[0])
    # write_file('d:/', 'wrong_road', list_write[1])
    # write_file('d:/', 'wrong_busstop', list_write[2])

    write_file('d:/', 'good_svc', list_write[0])
    write_file('d:/', 'good_road', list_write[1])
    write_file('d:/', 'good_busstop', list_write[2])


##################################################################################
##################################################################################
def label_distribution(list_line):
    # check the distribution of labels:
    list_all = list()
    total = 0
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')
        list_all.append(split_second)  # get all the labels
        total += len(split_second)

    labels = []
    for line in list_all:
        for label in line:
            if label not in labels:
                labels.append(label)

    labels = sorted(labels)
    for label in labels:
        cnt_label = 0
        for line in list_all:
            for value in line:
                if value.strip() == label:
                    cnt_label += 1
        print 'Counting number of label %i: \t %i \t %.2f' % (int(label), cnt_label, (cnt_label / float(total) * 100))
    print 'Total labels: \t %i' % total
    return None


##################################################################################
##################################################################################
if __name__ == '__main__':
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    name_ = 'Label_all_crf.txt'
    list_line_ = load_file(path_, name_)

    # label_distribution(list_line_)
    # command_ = 'svc'  # call for each type: 'svc', 'road', 'busstop'
    # command_ = 'road'  # call for each type: 'svc', 'road', 'busstop'
    # command_ = 'busstop'  # call for each type: 'svc', 'road', 'busstop'
    # match_dict(list_line_, command_)
    # isCapitalize(list_line_)
    # reg_bussvc(list_line_, n_token=10)
    # match_road_busstop(list_line_, 'road')
    # match_road_busstop(list_line_, 'busstop')
    # command_ = 'svc'
    # command_ = 'road'
    # command_ = 'busstop'
    # machting_token_bef(list_line_, command_)
    # command_ = 'svc'
    # matching_token_aft(list_line_, command_)

    print 'Loading features ------------------------------------'
    list_all = []
    start = timeit.default_timer()

    ftr_match_dict_svc = match_dict(list_line_, command='svc')
    ftr_match_dict_road = match_dict(list_line_, command='road')
    ftr_match_dict_busstop = match_dict(list_line_, command='busstop')
    print 'Finished loading match dictionary ------------------------------------'
    ftr_isCapitalize = isCapitalize(list_line_)
    ftr_reg_svc = reg_bussvc(list_line_, n_token=10)
    ftr_match_road = match_road_busstop(list_line_, command='road')
    ftr_match_busstop = match_road_busstop(list_line_, command='busstop')
    print 'Finished loading regular expression and matching for road and bus stop ------------------------------------'
    ftr_match_token_bef_svc = matching_token_bef(list_line_, command='svc')
    ftr_match_token_bef_road = matching_token_bef(list_line_, command='road')
    ftr_match_token_bef_busstop = matching_token_bef(list_line_, command='busstop')
    ftr_match_token_aft_svc = matching_token_aft(list_line_, command='svc')
    print 'Finished loading for token before and after the label ------------------------------------'

    list_all.append(ftr_match_dict_svc)
    list_all.append(ftr_match_dict_road)
    list_all.append(ftr_match_dict_busstop)
    list_all.append(ftr_isCapitalize)
    list_all.append(ftr_reg_svc)
    list_all.append(ftr_match_road)
    list_all.append(ftr_match_busstop)
    list_all.append(ftr_match_token_bef_svc)
    list_all.append(ftr_match_token_bef_road)
    list_all.append(ftr_match_token_bef_busstop)
    list_all.append(ftr_match_token_aft_svc)

    X = np.array(construct_ftr_CRF(list_all))  # construct the features for CRF
    print 'Constructing features for CRF ------------------------------------'
    Y = np.array(load_target_label(list_line_))
    print 'Loading the target labels ------------------------------------'

    stop = timeit.default_timer()
    print 'Loading features needs %.3f sec' % (stop - start)

    # # crf = ChainCRF(inference_method='max-product', directed=False, class_weight=None)
    # # ssvm = FrankWolfeSSVM(model=crf, C=1.0, max_iter=10)
    # # ssvm.fit(X, Y)
    # # print 'Accuracy of linear-crf %f:' % ssvm.score(X, Y)

    # n_cross_valid_crf(X, Y, K=2)
    n_cross_valid_crf_candidate(list_line_, X, Y, K=2)
