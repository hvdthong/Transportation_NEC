__author__ = 'vdthoang'
from main.loadFile import load_file
from main.writeFile import write_file
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def retrieve_sents(path, name):
    sents_only = list()
    sents = load_file(path, '/allTweets_ver3/' + name)
    for sent in sents:
        split_sent = sent.split('\t')
        sents_only.append(split_sent[2])
    print len(sents)
    return sents_only


def ftr_sentiment(path, name):
    ftr = list()
    sents = load_file(path, name)
    for sent in sents:
        split_sent = sent.split('\t')
        sentiment, sentence = split_sent[0], split_sent[1]
        new_sent = sentence.strip() + ' sentiment_' + str(sentiment)
        ftr.append(new_sent)
    # for value in ftr:
    #     print value
    # print len(ftr)
    return ftr


def event_sentiment(path, event, ftr_list):
    path_event = path + '/allTweets_ver3'
    list_ = load_file(path_event,  event + '.csv')
    new_list = list()
    for i in range(0, len(list_)):
        split_value = list_[i].split('\t')
        new_list.append(split_value[0] + '\t' + split_value[1] + '\t' + ftr_list[i])

    write_file(path_event, event + '_sentiment', new_list)

if __name__ == '__main__':
    # getting the sentences of events, then run the sentiment analysis to do the events detection (using PeiHua work)
    # After that, creating the features for events detection

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents'
    # name = 'accident.csv'
    # sents = retrieve_sents(path, name)
    # write_file(path, 'allTweets_ver3', sents)

    # After running the four commands above, applying sentiment analysis for events detection in folder
    # D:\Project\Transportation_SMU-NEC_collaboration\SentimentAnalysis\TransportSentiment (1)\TransportSentiment
    # After that, we will have the sentiment scores for each sents
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents'
    name = 'allTweets_ver3_sentiment.txt'
    events = ['wait', 'missing', 'skip', 'slow', 'accident', 'crowd']
    ftr_list = ftr_sentiment(path, name)
    for event in events:
        event_sentiment(path, event, ftr_list)
