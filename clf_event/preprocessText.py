__author__ = 'vdthoang'

from main.loadFile import load_file
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS


def clean_url(sentence):
    tokens = sentence.split()
    new_sentence = ''

    for token in tokens:
        if token.startswith('http'):
            token = 'url_link'
        new_sentence = new_sentence.strip() + ' ' + token
    # print new_sentence
    return new_sentence.strip()


def clean_number(sentence):
    tokens = sentence.split()
    new_sentence = ''

    for token in tokens:
        if token.isdigit():
           flag = True
        else:
            flag = False

        if flag is False:
            new_sentence = new_sentence.strip() + ' ' + token
    return new_sentence.strip()


def remove_stopwords(sentence):
    tokens = sentence.split()
    new_sentence = ''

    for token in tokens:
        if token.lower() in ENGLISH_STOP_WORDS:
            token = ''
        new_sentence = new_sentence.strip() + ' ' + token
    # print new_sentence
    return new_sentence.strip()


if __name__ == '__main__':
    # # using to create a label for running classification
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event'
    name_ = 'Philips_twitter_labeledComplete_ver2.txt'
    list_lbl = load_file(path_, name_)

    for sent in list_lbl:
        split_sent = sent.split('\t')
        # clean_url(sent)
        remove_stopwords(sent)
