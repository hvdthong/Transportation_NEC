__author__ = 'vdthoang'
import json
import pandas as pd
import time
from main.writeFile import write_file
from main.loadFile import load_file


def add_hour_dof():
    file = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data/tweet_short_event_tagged_for_icwsm2016.json'

    start = time.time()
    df = pd.read_json(file)
    end = time.time()
    print end - start

    df['hour'] = df['createAtMilis'].map(lambda x: (pd.to_datetime(x, unit='ms').hour + 8) % 24)
    df['dow'] = df['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').dayofweek)
    # df['woy'] = df['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').weekofyear)

    list_id = df['id']
    list_hour = df['hour']
    list_dw = df['dow']


    list_write = list()
    for i in range(0, len(list_dw)):
        print str(list_id[i]) + '\t' + str(list_hour[i]) + '\t' + str(list_dw[i])
        list_write.append(str(list_id[i]) + '\t' + str(list_hour[i]) + '\t' + str(list_dw[i]))

    path_write = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data'
    name_write = 'twitter_hour_dow'
    write_file(path_write, name_write, list_write)


########################################################################
########################################################################
def extract_tweet(list_):
    list_id = list()
    for value in list_:
        split = value.split('\t')
        list_id.append(split[0])
    return list_id


def subset_tweetID(list_icwsm, list_time):
    list_ = extract_tweet(list_icwsm)
    list_time = extract_tweet(list_time)

    list_union = set(list_) & set(list_time)
    print len(list_union)

    for value in list_union:
        print value

    write_file('C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data', 'twitter_correct', list_union)


if __name__ == '__main__':
    path = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data'
    name_icwsm = 'twitter.csv'
    name_time = 'twitter_retweet_hour_dow.csv'

    list_icwsm = load_file(path, name_icwsm)
    list_time = load_file(path, name_time)
    subset_tweetID(list_icwsm, list_time)
