__author__ = 'vdthoang'
import json
import gensim
from CRF_labeling.filterText_CRF import filter_eachTok_rmLinks
from main.writeFile import write_file


def load_FBText(path, name):
    with open(path + '/' + name) as data_file:
        data = json.load(data_file)
    print len(data)
    texts = list()
    for element in data:
        if element['message'] is not None:
            message = element['message'].encode('utf-8').replace('\n', ' ').replace('\r', ' ') \
                .replace('\t', ' ').strip()
        else:
            if element['description'] is not None:
                message = element['description'].encode('utf-8').replace('\n', ' ').replace('\r', ' ') \
                    .replace('\t', ' ').strip()
            else:
                message = 'None'
        # print message
        if message is not 'None':
            texts.append(message)
    return texts


def wordVec_facebook(sents, path_w, name_w, win_size):
    list_all = list()
    for i in range(0, len(sents)):
        split_sent = sents[i].split()
        tokens = list()
        for token in split_sent:
            token_filter = filter_eachTok_rmLinks(token, 'model')
            if len(token_filter) > 0:
                tokens.append(token_filter.lower())
        print i
        list_all.append(tokens)

    model = gensim.models.Word2Vec(list_all, size=win_size, window=5, min_count=1, workers=5)
    print model.most_similar(['bus'])

    list_write = list()
    for i in range(0, len(model.index2word)):
        # print model.index2word[i], model.syn0norm[i]
        line = model.index2word[i]
        for value in model.syn0norm[i]:
            line += '\t' + str(value)
        line = line.strip()
        list_write.append(line)
        print line
    write_file(path_w, name_w + '_%i' % win_size, list_write)


if __name__ == '__main__':
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/WordVector'
    name = 'sg_fb_feed_2015_BusNews.json'
    sents = load_FBText(path, name)
    print len(sents)

    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/WordVector'
    name_write = 'word_vec'
    # win_size = 30
    # win_size = 70
    # win_size = 100
    # win_size = 150
    win_size = 200
    wordVec_facebook(sents, path_write, name_write, win_size)