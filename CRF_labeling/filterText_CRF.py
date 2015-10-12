__author__ = 'vdthoang'
import sys
from main.loadFile import load_file
from string import punctuation

# make the default is 'utf-8'
reload(sys)
sys.setdefaultencoding('utf8')


def filter_eachToken(text):  # use for each token string
    # clean if the first character of string contains punctuation
    while True:
        if text[0] in punctuation:
            text = text[1:]

            if len(text) == 0:
                break
        else:
            break

    # clean if the final character of string contains the punctuation
    while True:
        if len(text) == 0:
                break

        if text[-1] in punctuation:
            text = text[:-1]
        else:
            break
    return text.strip()


def filter_eachTok_rmLinks(text):
    text = filter_eachToken(text)  # remove all punctuations
    if ('https://' in text) or ('http://' in text):
        return ''
    else:
        return text.strip()


def filterTxt_CRF(list_line, command):
    # remove all the punctuation for each token in the text
    list_convert = []
    for i in range(0, len(list_line), 3):
        text = ''
        label = ''

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')

        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        for k in range(0, len(split_first)):
            token_ = split_first[k].strip()

            if command == 'removePunc':  # remove all punctuations
                token_filter = filter_eachToken(token_)
            elif command == 'removeLink':  # remove all punctuations and links in token
                token_filter = filter_eachTok_rmLinks(token_)
            else:
                print 'You need to give the correct command'
                quit()

            if len(token_filter) != 0:
                text += token_filter + '\t'
                label += split_second[k] + '\t'

        list_convert.append(text.strip())
        list_convert.append(label.strip())
        list_convert.append('\n')

    del list_convert[-1]
    return list_convert


if __name__ == '__main__':
    # use to filter Twitter data set. In particular, we remove all punctuations in the Twitter dataset
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    name = 'labeling_all.txt'
    list_line_ = load_file(path, name)
    list_convert = filterTxt_CRF(list_line_, command='removePunc')  # remove all punctuation for each token
    list_convert = filterTxt_CRF(list_line_, command='removeLink')

    print 'Length of orignial list %i ' % len(list_line_)
    print 'Length of converted list %i ' % len(list_convert)

    for value in list_convert:
        print value
