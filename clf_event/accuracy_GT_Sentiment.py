__author__ = 'vdthoang'
from main.loadFile import load_file
from main.writeFile import write_file
import sys
from skll import kappa
from scipy import spatial

# make the default is 'utf-8'
reload(sys)
sys.setdefaultencoding('utf8')


def load_sentiment(path, name, sentiment_label):
    list_ = load_file(path, name)
    list_write = list()

    for value in list_:
        split_value = value.split('\t')
        sentiment, sentence = split_value[0], split_value[1]
        if sentiment_label == 'veryNeg':
            if int(sentiment) == 0:
                new_sent = '1' + '\t' + sentence
            else:
                new_sent = '0' + '\t' + sentence

        elif sentiment_label == 'Neg':
            if int(sentiment) == 1:
                new_sent = '1' + '\t' + sentence
            else:
                new_sent = '0' + '\t' + sentence

        elif sentiment_label == 'Neutral':
            if int(sentiment) == 2:
                new_sent = '1' + '\t' + sentence
            else:
                new_sent = '0' + '\t' + sentence

        elif sentiment_label == 'Pos':
            if int(sentiment) == 3:
                new_sent = '1' + '\t' + sentence
            else:
                new_sent = '0' + '\t' + sentence

        elif sentiment_label == 'veryPos':
            if int(sentiment) == 4:
                new_sent = '1' + '\t' + sentence
            else:
                new_sent = '0' + '\t' + sentence

        elif sentiment_label == 'veryNeg_Neg':
            if int(sentiment) == 0 or int(sentiment) == 1:
                new_sent = '1' + '\t' + sentence
            else:
                new_sent = '0' + '\t' + sentence

        elif sentiment_label == 'Pos_veryPos':
            if int(sentiment) == 3 or int(sentiment) == 4:
                new_sent = '1' + '\t' + sentence
            else:
                new_sent = '0' + '\t' + sentence

        list_write.append(new_sent)
    print len(list_write)
    write_file(path, 'allTweets_ver3_sentLabel_' + sentiment_label, list_write)


def kapp_sentiment_event(path_sent, path_event, sentiment, event):
    load_sent, load_event = load_file(path_sent, 'allTweets_ver3_sentLabel_' + sentiment + '.csv')\
        , load_file(path_event, event + '.csv')
    list_sent, list_gt = list(), list()
    for i in range(0, len(load_sent)):
        split_sent, split_gt = load_sent[i].split('\t'), load_event[i].split('\t')
        label, gt = int(split_sent[0]), int(split_gt[1])
        list_sent.append(label), list_gt.append(gt)
    print 'Kappa score of ' + sentiment + ' and ' + event + ':' + '\t' + str(kappa(list_gt, list_sent))
    # print 'Kappa score of ' + sentiment + ' and ' + event + ': ' + str(1 - spatial.distance.cosine(list_gt, list_sent))


########################################################################################################################
########################################################################################################################
def count_sentiment_event(path_sent, path_event, sentiment, event):
    load_sent, load_event = load_file(path_sent, 'allTweets_ver3_sentLabel_' + sentiment + '.csv')\
        , load_file(path_event, event + '.csv')
    list_sent, list_gt = list(), list()
    for i in range(0, len(load_sent)):
        split_sent, split_gt = load_sent[i].split('\t'), load_event[i].split('\t')
        label, gt = int(split_sent[0]), int(split_gt[1])
        list_sent.append(label), list_gt.append(gt)

    count = 0
    for i in range(0, len(list_gt)):
        if (list_gt[i] == 1) and (list_sent[i] == 1):
            count += 1
    print 'Count of ' + sentiment + ' and ' + event + ':' + '\t' + str(count)

if __name__ == '__main__':
    # Running this to get the labelled of sentiment for each 'Neg', 'Pos' or 'Neutral'
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents'
    # name = 'allTweets_ver3_sentiment.txt'
    # # sentiments = ['veryNeg', 'Neg', 'Neutral', 'Pos', 'veryPos']
    # sentiments = ['veryNeg_Neg', 'Neutral', 'Pos_veryPos']
    # for label in sentiments:
    #     load_sentiment(path, name, label)

    # After that, running this to get the Kappa score of each 'Neg', 'Pos' or 'Neutral' vs. ground truth
    path_sent = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents'
    path_event = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver3'

    sentiments = ['veryNeg_Neg', 'Neutral', 'Pos_veryPos']
    events = ['wait', 'missing', 'skip', 'slow', 'accident', 'crowd']
    for event in events:
        for sent in sentiments:
            # kapp_sentiment_event(path_sent, path_event, sent, event)
            count_sentiment_event(path_sent, path_event, sent, event)
