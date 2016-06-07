__author__ = 'vdthoang'

from main.loadFile import load_file
from ICWSM_2016.hourly_dist import extract_tweet


def find_event(list_id, list_event):
    id_all = extract_tweet(list_id)
    id_event = extract_tweet(list_event)

    for i in range(0, len(list_id)):
        id_ = list_id[i].split('\t')
        event_ = list_event[i].split('\t')

        if int(event_[1]) == 1:
            print id_[0], id_[2], id_[3]


def event_entity_corr(list_event, list_entity, event, type):
    list_cnt = list()
    for tweet in list_event:
        split_ = tweet.split('\t')
        if int(split_[1]) == 1:
            id = split_[0]
            for tweet_e in list_entity:
                split_entity = tweet_e.split('\t')
                id_entity = split_entity[0]
                if id == id_entity:
                    if type == 'busstop':
                        if split_entity[1] not in list_cnt:
                            list_cnt.append(split_entity[1])
                    else:
                        if split_entity[3] not in list_cnt:
                            list_cnt.append(split_entity[3])
    # print list_cnt
    print event + '\t' + type + '\t' + str(len(list_cnt))

if __name__ == '__main__':
    # path = 'd:/'
    # name = 'twitter.csv'
    # load_id = load_file(path, name)
    #
    # path_event = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data'
    # name_event = 'twitter_event_accident.csv'
    # load_event = load_file(path_event, name_event)
    #
    # find_event(load_id, load_event)

    events = ['accident', 'crowd', 'missing', 'skip', 'slow', 'wait']
    types = ['bussvc', 'road', 'busstop']
    for event in events:
        path_event = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data'
        name_event = 'twitter_event_' + event + '.csv'
        load_event = load_file(path_event, name_event)

        for type in types:
            path_type = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data'
            name_type = 'twitter_' + type + '.csv'
            load_type = load_file(path_type, name_type)
            event_entity_corr(load_event, load_type, event, type)
            # break
        # print path_event, name_event
        # break