__author__ = 'vdthoang'
import json
import time
from main.writeFile import write_file
from main.loadFile import load_file
from main.writeFile import write_file
import MySQLdb


def filtering_json_tweet_ver2(path, name, name_write):
    # Use for tweet data set
    # For each tweets, dectect post_tweet and retweet and extract the information

    with open(path + '/' + name) as data_file:
        data = json.load(data_file)
    cnt, list_write = 0, list()
    for element in data:
        id_ = element['id']
        user = element['user']
        screenName = user['screenName']
        createdAt = element['createAtMilis']
        text = element['text'].encode('utf-8').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()

        date_format = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(createdAt / 1000)))
        print cnt, id_, str(date_format)
        line = str(id_) + '\t' + screenName + '\t' + date_format + '\t' + text
        list_write.append(line)
        cnt += 1

    print len(list_write)
    write_file(path, name_write, list_write)


def filtering_json_facebook_ver2(path, name, name_write):
    with open(path + '/' + name) as data_file:
        data = json.load(data_file)
    cnt, list_write = 0, list()
    for element in data:
        from_data = element['from']

        print (element['id']
               + '\t' + from_data['name'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
               + '\t' + element['created_time']
               + '\t' + element['message'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip())
        list_write.append(element['id']
               + '\t' + from_data['name'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
               + '\t' + element['created_time']
               + '\t' + element['message'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip())
        cnt += 1
    print cnt
    write_file(path, name_write, list_write)


def insert_sql_json(path, name, data):
    list_ = load_file(path, name)
    db = MySQLdb.connect(host='10.4.8.139',  # your host, usually localhost
                         user='bussense',  # your username
                          passwd='Bussense2016!',  # your password
                          db='bussense_archive')  # name of the data base
    cur = db.cursor()
    if data == 'twitter':
        list_insert = list()
        for value in list_:
            split_value = value.split('\t')
            tweetID, screenName, createdAt, tweetText = split_value[0], split_value[1], split_value[2], split_value[3]
            list_insert.append((tweetID, screenName, createdAt, tweetText))
        sql = "INSERT INTO tweets(tweetID, screenName, createdAt, tweetText) VALUE(%s,%s,%s,%s);"
        print sql
    elif data == 'facebook':
        list_insert = list()

        for value in list_:
            split_value = value.split('\t')
            postID, name, createdTime, post = split_value[0], split_value[1], split_value[2], split_value[3]
            list_insert.append((postID, name, createdTime.replace('+0000', ''), post))
        sql = "INSERT INTO fb_posts(postID, name, createdTime, post) VALUE(%s,%s,%s,%s);"
        print sql

    cur.executemany(sql, list_insert)
    db.commit()
    db.close()
    print 'Finish insert data to sql'


if __name__ == '__main__':
    #################################################################################
    # TWITTER
    # path = 'd:/Project/Transportation_SMU-NEC_collaboration/Data_NEC_oldDATA'
    # name = 'plr_sg_tweet_2015_Jan_Dec.json'
    # name_write = 'plr_sg_tweet_2015_Jan_Dec'
    # filtering_json_tweet_ver2(path, name, name_write)

    # path = 'd:/Project/Transportation_SMU-NEC_collaboration/Data_NEC_oldDATA'
    # name = 'plr_sg_tweet_2016_Jan_Mar.json'
    # name_write = 'plr_sg_tweet_2016_Jan_Mar'
    # filtering_json_tweet_ver2(path, name, name_write)

    # path = 'd:/Project/Transportation_SMU-NEC_collaboration/Data_NEC_oldDATA'
    # name_write = 'plr_sg_tweet_old_2015_Mar_2016.csv'
    # insert_sql_json(path, name_write, 'twitter')

    #################################################################################
    # FACEBOOK
    # path = '/home/vdthoang/NEC_oldData'
    # name = 'sg_fb_feed_2015_bus.json'
    # name_write = 'sg_fb_feed_2015_bus'
    # filtering_json_facebook_ver2(path, name, name_write)

    # path = '/home/vdthoang/NEC_oldData'
    # name = 'sg_fb_post_2016_bus.json'
    # name_write = 'sg_fb_post_2016_bus'
    # filtering_json_facebook_ver2(path, name, name_write)

    path = 'd:/Project/Transportation_SMU-NEC_collaboration/Data_NEC_oldDATA'
    name_write = 'sg_fb_feed_old_2015_Mar_2016.csv'
    insert_sql_json(path, name_write, 'facebook')
