__author__ = 'vdthoang'
from main.loadFile import load_file
from nltk import FreqDist
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from classification_busService.ftr_bussvc_extraction import is_int
from CRF_labeling.feature_token_crf import token_isAllCharacter
from CRF_labeling.filterText_CRF import filterTxt_CRF
import sys
from main.writeFile import write_file

# make the default is 'utf-8'
reload(sys)
sys.setdefaultencoding('utf8')


def check_label_crf(list_line):
    # check if we label correct or not.
    # In particular, we check if the length of text and label are equal or not
    # if not, print line: 'wrong at index'
    list_wrong = []
    for i in range(0, len(list_line), 3):
        first = 0
        second = 0
        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
            first = len(split_first)
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')
            second = len(split_second)

        if first == second:
            print i, first, second
        else:
            list_wrong.append('Wrong at index:' + str(i))
            print 'Wrong at index:', i
    print ('There are %d wrong lines' % len(list_wrong))


def check_label_crf_lblText(list_line):
    # we check if user annotate label which appear in the label list or not
    # print the list of label that user annotated
    # for CRF, we have four labels: 0:None, 1: Bus service, 2: Road, 3: Bus stop
    list_label = list()
    for i in range(0, len(list_line), 3):
        first = 0
        second = 0
        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')

        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        for each in split_second:
            if each not in list_label:
                list_label.append(each)
    print sorted(list_label)
    return None


def check_svc_bef_aft(list_line, command):
    # check the freq of words before and after bus service
    # check the freq of words before and after of word (number) which is non bus svc
    text = ''
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        for k in range(0, len(split_second)):
            if command == 'before_svc':
                if int(split_second[k]) == 1:  # mean bus svc
                    if command == 'before_svc':
                        if k > 0:  # bus svc doesn't appear at the first position of sentences
                            text = text + split_first[k - 1].lower() + ' '  # take the word before
                print i, k, split_first[k]

            if command == 'after_svc':
                if int(split_second[k]) == 1:  # mean bus svc
                    if command == 'after_svc':
                        if k < len(split_second) - 1:
                            text = text + split_first[k + 1].lower() + ' '  # take the word after

            if command == 'before_notsvc':
                if RepresentsInt(split_first[k]) is True and int(split_second[k]) != 1:  # text is a number and not a bus svc
                    if k > 0:  # bus svc doesn't appear at the last position of sentences
                        text = text + split_first[k - 1].lower() + ' '

            if command == 'after_notsvc':
                if RepresentsInt(split_first[k]) is True and int(split_second[k]) != 1:  # text is a number and not a bus svc
                    if k < len(split_second) - 1:  # bus svc doesn't appear at the last position of sentences
                        text = text + split_first[k + 1].lower() + ' '

    fdist = FreqDist()
    tokens = word_tokenize(str(text))
    fdist.update(tokens)
    for value in fdist.most_common(len(fdist)):
        print value[0], '\t', value[1]

    print text

    # wordcloud = WordCloud(background_color='black', max_words=100, margin=10, random_state=False).generate(text)
    # plt.title(command, fontsize=30)
    # plt.imshow(wordcloud.recolor())
    # plt.axis("off")
    # plt.show()


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


#################################################################################################
#################################################################################################
def connect_token(string):
    split_str = string.split()
    if len(split_str) > 1:
        text = ''
        for token in split_str:
            text = text + '_' + token
        return text[1:]
    else:
        return string


def check_bef_aft_roadBusStop(list_line, command):
    text = ''
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        k = 0
        while True:
            if k >= len(split_second):
                break

            if command == 'bef_road':
                try:
                    if int(split_second[k]) == 2:  # take road
                        if k > 0:
                            text = text + connect_token(split_first[k - 1].lower()) + ' '  # take the word before

                        while True:
                            k += 1
                            if k == len(split_second):
                                break
                            else:
                                if int(split_second[k]) != 2:
                                    break
                    else:
                        k += 1
                except ValueError:
                    k += 1

            if command == 'aft_road':
                try:
                    if int(split_second[k]) == 2:  # take road
                        while True:
                            k += 1
                            if k == len(split_second):
                                break
                            else:
                                if int(split_second[k]) != 2:
                                    break
                        if k < len(split_second) - 1:
                            if is_int(split_first[k]) is False:
                                text = text + connect_token(split_first[k].lower()) + ' '  # take the token after the label
                    else:
                        k += 1

                except ValueError:
                    k += 1

            if command == 'bef_busstop':
                try:
                    if int(split_second[k]) == 3:  # take busstop
                        if k > 0:
                            text = text + connect_token(split_first[k - 1].lower()) + ' '  # take the word before

                        while True:
                            k += 1
                            if k == len(split_second):
                                break
                            else:
                                if int(split_second[k]) != 3:
                                    break
                    else:
                        k += 1
                except ValueError:
                    k += 1

            if command == 'aft_busstop':
                try:
                    if int(split_second[k]) == 3:  # take road
                        while True:
                            k += 1
                            if k == len(split_second):
                                break
                            else:
                                if int(split_second[k]) != 3:
                                    break
                        if k < len(split_second) - 1:
                            if is_int(split_first[k]) is False:
                                text = text + connect_token(split_first[k].lower()) + ' '  # take the token after the label
                    else:
                        k += 1

                except ValueError:
                    k += 1

    fdist = FreqDist()
    tokens = word_tokenize(str(text))
    fdist.update(tokens)
    for value in fdist.most_common(len(fdist)):
        print value[0], '\t', value[1]

    print text

    # wordcloud = WordCloud(background_color='black', max_words=100, margin=10, random_state=False).generate(text)
    # plt.title(command, fontsize=30)
    # plt.imshow(wordcloud.recolor())
    # plt.axis("off")
    # plt.show()


def take_road_busstop(list_line, command):
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        list_ = []
        k = 0
        while True:
            if k >= len(split_second):
                break

            if command == 'road':
                text = ''
                if int(split_second[k]) == 2:  # take road
                    text = text + split_first[k] + ' '
                    while True:
                        k += 1
                        if k == len(split_second):
                            break
                        else:
                            if int(split_second[k]) == 2:
                                text = text + split_first[k] + ' '
                            else:
                                break
                    list_.append(text)
                else:
                    k += 1

        for value in list_:
            print i, value


######################################################################################################
######################################################################################################
def load_all_dic_token_bef_road_busstop(list_line, command):
    # load all the word of token before and after labeling, note that we do not consider if this token is a
    # number. In fact, we only consider if token contain all characters
    # Using only for "road" and "busstop"

    text = ''
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        k = 0
        while True:
            if k >= len(split_second):
                break

            if command == 'road':  # get the token before labeling for road
                try:
                    if int(split_second[k]) == 2:  # detect this is a road => get the token before it
                        if k > 0:
                            token_bef = split_first[k - 1].lower()
                            if token_isAllCharacter(token_bef) is True:
                                text = text + connect_token(token_bef) + ' '  # take the word before

                        while True:
                            k += 1
                            if k == len(split_second):
                                break
                            else:
                                if int(split_second[k]) != 2:
                                    break
                    else:
                        k += 1
                except ValueError:
                    k += 1

            if command == 'busstop':  # get the token before labeling for road
                try:
                    if int(split_second[k]) == 3:  # detect this is a road => get the token before it
                        if k > 0:
                            token_bef = split_first[k - 1].lower()
                            if token_isAllCharacter(token_bef) is True:
                                text = text + connect_token(token_bef) + ' '  # take the word before

                        while True:
                            k += 1
                            if k == len(split_second):
                                break
                            else:
                                if int(split_second[k]) != 3:
                                    break
                    else:
                        k += 1
                except ValueError:
                    k += 1

    fdist = FreqDist()
    tokens = word_tokenize(str(text))
    fdist.update(tokens)
    for value in fdist.most_common(len(fdist)):
        print value[0], '\t', value[1]

    list_return = list()
    for value in fdist.most_common(len(fdist)):
        list_return.append(value[0])
        print value[0]
    print len(fdist)
    return list_return


def load_all_dic_token_bef_aft_svc(list_line, command):
    # loading all token before and after for bus service
    # Using only for bus service, because for bus service we not only focus on the token before, but also the token
    # after labeling
    text = ''
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        k = 0
        while True:
            if k >= len(split_second):
                break

            if command == 'bef_svc':  # get the token before labeling for bus svc
                try:
                    if int(split_second[k]) == 1:  # detect this is a svc => get the token before it
                        if k > 0:
                            token_bef = split_first[k - 1].lower()
                            if token_isAllCharacter(token_bef) is True:
                                text = text + connect_token(token_bef) + ' '  # take the word before

                        while True:
                            k += 1
                            if k == len(split_second):
                                break
                            else:
                                if int(split_second[k]) != 1:
                                    break
                    else:
                        k += 1
                except ValueError:
                    k += 1

            if command == 'aft_svc':
                try:
                    if int(split_second[k]) == 1:  # take bus svc
                        while True:
                            k += 1
                            if k == len(split_second):
                                break
                            else:
                                if int(split_second[k]) != 1:
                                    break
                        if k < len(split_second) - 1:
                            # take the token after the label
                            token_aft = split_first[k].lower()
                            if token_isAllCharacter(token_aft) is True:
                                text = text + connect_token(token_aft) + ' '
                    else:
                        k += 1

                except ValueError:
                    k += 1

    fdist = FreqDist()
    tokens = word_tokenize(str(text))
    fdist.update(tokens)
    for value in fdist.most_common(len(fdist)):
        print value[0], '\t', value[1]

    list_return = list()
    for value in fdist.most_common(len(fdist)):
        list_return.append(value[0])
        print value[0]
    print len(fdist)
    return list_return


######################################################################################################
######################################################################################################
if __name__ == '__main__':
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    # name_T = 'Label_Thong_crf.txt'  # good
    # file_line_T = load_file(path, name_T)
    # check_label_crf(file_line_T)

    # name_H = 'Label_PeiHua_crf.txt'  # good
    # file_line_H = load_file(path, name_H)
    # check_label_crf(file_line_H)
    # check_svc_bef_aft(file_line_H, 'before_svc')

    # name_P = 'Label_Philips_crf.txt'  # good
    # file_line_P = load_file(path, name_P)
    # check_label_crf(file_line_P)
    # check_svc_bef_aft(file_line_P, 'before_svc')

    # name_all = 'Label_all_crf.txt'  # good
    # file_line_all = load_file(path, name_all)
    # check_label_crf(file_line_all)
    # check_svc_bef_aft(file_line_all, 'before_svc')
    # check_svc_bef_aft(file_line_all, 'after_svc')
    # check_svc_bef_aft(file_line_all, 'before_notsvc')
    # check_svc_bef_aft(file_line_all, 'after_notsvc')

    # take_road_busstop(file_line, 'road')
    # check_bef_aft_roadBusStop(file_line_all, 'bef_road')
    # check_bef_aft_roadBusStop(file_line_all, 'aft_road')
    # check_bef_aft_roadBusStop(file_line_all, 'bef_busstop')
    # check_bef_aft_roadBusStop(file_line_all, 'aft_busstop')

    ######################################################################################################
    ######################################################################################################
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    # name_all = 'Label_all_crf.txt'  # good
    # file_line_all = load_file(path, name_all)
    # load_all_dic_token_bef_road_busstop(file_line_all, command='road')
    # load_all_dic_token_bef_road_busstop(file_line_all, command='busstop')

    # load_all_dic_token_bef_aft_svc(file_line_all, command='bef_svc')
    # load_all_dic_token_bef_aft_svc(file_line_all, command='aft_svc')

    ######################################################################################################
    ######################################################################################################
    # USING FOR TWITTER DATASET
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    name = 'labeling_all.txt'
    list_line = filterTxt_CRF(load_file(path, name))
    # check_label_crf(list_line)
    # check_label_crf_lblText(list_line)
    # check_label_crf(filterTxt_CRF(list_line))

    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features'
    # name_tok_bef_road = 'all_token_bef_road'
    # list_tok_bef_road = load_all_dic_token_bef_road_busstop(list_line, command='road')
    # write_file(path_write, name_tok_bef_road, list_tok_bef_road)

    # name_tok_bef_busstop = 'all_token_bef_busstop'
    # list_tok_bef_busstop = load_all_dic_token_bef_road_busstop(list_line, command='busstop')
    # write_file(path_write, name_tok_bef_busstop, list_tok_bef_busstop)

    # name_tok_bef_bussvc = 'all_token_bef_bussvc'
    # list_tok_bef_bussvc = load_all_dic_token_bef_aft_svc(list_line, command='bef_svc')
    # write_file(path_write, name_tok_bef_bussvc, list_tok_bef_bussvc)

    # name_tok_aft_bussvc = 'all_token_aft_bussvc'
    # list_tok_aft_bussvc = load_all_dic_token_bef_aft_svc(list_line, command='aft_svc')
    # write_file(path_write, name_tok_aft_bussvc, list_tok_aft_bussvc)
