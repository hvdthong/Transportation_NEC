__author__ = 'vdthoang'
from main.loadFile import load_file


def load_sentiment(list_):
    id_, label_ = list(), list()
    for value in list_:
        split_value = value.split('\t')
        id_.append(split_value[0]), label_.append(split_value[1])
    return id_, label_


if __name__ == '__main__':
    path = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/ubicomp2016_paper/data'
    name = 'sentiment_Twitter_predcited_analysis.txt'

    list_load = load_file(path, name)
    for value in list_load:
        print value
    print len(list_load)

    id_, label_ = load_sentiment(list_load)
    print len(id_), len(label_)

