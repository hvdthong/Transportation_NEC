__author__ = 'vdthoang'
from main.loadFile import load_file


def sent_dist(list_sent, list_event):
    positive, negative, neutral = 0, 0, 0


if __name__ == '__main__':
    path = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data'
    name_sent = 'sentiment_Twitter_predcited_analysis.txt'
    list_sent = load_file(path, name_sent)

    events = ['accident', 'crowd', 'missing', 'skip', 'slow', 'wait']
    for event in events:
        list_event = load_file(path, 'twitter_event_' + event + '.csv')
