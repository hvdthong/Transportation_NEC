__author__ = 'vdthoang'
from main.loadFile import load_file
from load_crf import connect_token  # use to connect token, ex: 'Web 04' => 'Web_04'
from nltk import FreqDist
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from classification_busService.ftr_bussvc_extraction import is_int
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def token_bef(list_line, command):
    # check the token before label, note that belongs to the command ('svc', 'road', 'busstop')
    port = PorterStemmer()
    text = ''
    list_length = []
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')  # list of sentences
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')  # list of label for each word
        list_length.append(len(split_first))

        if command == 'svc':
            for k in range(0, len(split_second)):
                # check the frequency of token before bus service
                if int(split_second[k]) == 1:  # mean bus svc
                    if k > 0:  # bus svc doesn't appear at the first position of sentences
                        # try:  # don't use stemming here
                        #     stem_word = port.stem(connect_token(split_first[k - 1].lower()))  # take the token before
                        # except UnicodeDecodeError:
                        #     stem_word = connect_token(split_first[k - 1].lower())
                        stem_word = connect_token(split_first[k - 1].lower())
                        if is_int(stem_word) is False:
                            text = text + stem_word + ' '

        elif command == 'road':
            k = 0
            while True:
                if k >= len(split_second):
                    break
                else:
                    try:
                        if int(split_second[k]) == 2:  # mean road
                            if k > 0:
                                stem_word = connect_token(split_first[k - 1].lower())
                                if is_int(stem_word) is False:
                                    text = text + stem_word + ' '  # take the word before

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

        elif command == 'busstop':
            k = 0
            while True:
                if k >= len(split_second):
                    break
                else:
                    try:
                        if int(split_second[k]) == 3:  # mean bus stop
                            if k > 0:
                                stem_word = connect_token(split_first[k - 1].lower())
                                if is_int(stem_word) is False:
                                    text = text + stem_word + ' '  # take the word before

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
        # print value[0]

    print text


def token_aft(list_line, command):
    # check the token after label, note that belongs to the command ('svc', 'road', 'busstop')
    text = ''
    list_length = []

    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')  # list of sentences
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')  # list of label for each word
        list_length.append(len(split_first))

        if command == 'svc':
            for k in range(0, len(split_second)):
                # check the frequency of token before bus service
                if int(split_second[k]) == 1:  # mean bus svc
                    if k < len(split_second) - 1:  # bus svc doesn't appear at the first position of sentences
                        # try:  # don't use stemming here
                        #     stem_word = port.stem(connect_token(split_first[k - 1].lower()))  # take the token before
                        # except UnicodeDecodeError:
                        #     stem_word = connect_token(split_first[k - 1].lower())
                        stem_word = connect_token(split_first[k + 1].lower())  # take the token after label
                        if is_int(stem_word) is False:
                            text = text + stem_word + ' '

                        # if stem_word == 'sd' or stem_word == 'dd':
                        #     print list_line[i]

    fdist = FreqDist()
    tokens = word_tokenize(str(text))
    fdist.update(tokens)
    for value in fdist.most_common(len(fdist)):
        # print value[0], '\t', value[1]
        print value[0]

    print text


if __name__ == '__main__':
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    name_all = 'Label_all_crf.txt'  # good
    file_line_all = load_file(path, name_all)
    command = 'svc'
    # command = 'road'
    # command = 'busstop'
    # token_bef(file_line_all, command)
    token_aft(file_line_all, command)
