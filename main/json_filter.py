# -*- coding: utf-8 -*-
#!/usr/bin/env python
from main.convertTime import convertTime_facebook
from main.writeFile import write_file
import os, sys
import json
import MySQLdb
from main.loadFile import load_file
import time
from main.convertTime import convertTime_twitter, timeSpam_twitter


__author__ = 'vdthoang'


# reload(sys)
# sys.setdefaultencoding('utf8')
#####################################################################################################
#####################################################################################################
########### FACEBOOK
def json_facebook(path, name, name_write):
    # Use to extract json text on json file
    # Use for facebook dataset
    with open(path + '/' + name) as data_file:
        data = json.load(data_file)

    list_info = []
    for element in data:
        from_data = element['from']

        print (element['id']
               + '\t' + from_data['name'].encode('utf-8').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
               + '\t' + element['created_time']
               + '\t' + element['message'].encode('utf-8').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip())

        list_info.append(element['id']
                         + '\t' + from_data['name'].encode('utf-8').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
                         + '\t' + element['created_time']
                         + '\t' + element['message'].encode('utf-8').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip())
        # break

        # time_convert = convertTime_facebook(element['created_time'])
        # if (time_convert >= 1420041600):
        #     # print (element['id'] + '\t' + from_data['name'].encode('utf-8').replace('\n','').replace('\t','').strip() + '\t' + element['message'].encode('utf-8').replace('\n','').replace('\t','').strip() + '\t' + element['created_time'] + '\t' + str(cnt))
        #     # print (element['id'])
        #     # list_test.append(element['id'])
        #
        #     # print (from_data['name'].encode('utf-8').replace('\n','').replace('\t','').strip())
        #     # list_test.append(from_data['name'].encode('utf-8').replace('\n','').replace('\t','').strip())
        #
        #     print (element['message'].encode('utf-8').replace('\n','').replace('\t','').strip())
        #     list_test.append(from_data['name'].encode('utf-8').replace('\n','').replace('\t','').strip())
        #     cnt += 1
        #     # if (cnt == 8984):
        #     #     print ('heelo')
        #     #     break
        # # if (cnt == 6):
        # #     break
        #
        # print (element['message'].encode('utf-8').replace('\n','').replace('\t','').strip())
        # list_test.append(from_data['name'].encode('utf-8').replace('\n','').replace('\t','').strip())

    # print (len(list_info))
    # print (cnt)

    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="ducthong", # your password
                      db="facebook_bus") # name of the data base
    cur = db.cursor()

    t0 = time()
    cnt = 0
    list_error = []

    for line in list_info:
        cnt += 1
        # print (cnt)

        split_line = line.strip().split('\t')
        facebookID = split_line[0]
        screenName = split_line[1]
        createTime = split_line[2]
        post = split_line[3]

        sql = """INSERT INTO facebook_posts(facebookID, screenName, createTime, post) VALUES ('""" \
              + facebookID + "','" + screenName.replace('\'','\'\'').replace('\\', '\\\\') + "','" + createTime + "','" \
              + post.replace('\'','\'\'').replace('\\', '\\\\') + "')"
        # print (sql)
        try:
            cur.execute(sql)
            db.commit()
        except:
            print (facebookID + '\t' + sql)
            list_error.append(facebookID + '\t' + sql)

        if (cnt % 1000 == 0):
            print 'Processing ' + str(cnt) + ' records takes ' + str(time() - t0)

    write_file(path, name_write + '_errorPost', list_error)
    print ('Done process')

    db.close()

def json_facebookBusTransport(path, name, name_write):
    with open(path + '/' + name) as data_file:
        data = json.load(data_file)

    SMRT_id = '566549713366262'
    LTA_id = '132581033478808'

    list_info = []
    for element in data:
        print element

        facebookID = element['id']

        screenName = ''
        if (SMRT_id == element['biz_id']):
            screenName = 'SMRT'
        elif (LTA_id == element['biz_id']):
            screenName = 'Land Transport Authority - We Keep Your World Moving'

        createTime = element['created_time']

        message = ''
        if (element['message'] != None):
            message = element['message'].encode('utf-8').replace('\n',' ').replace('\r', ' ').replace('\t',' ').strip()
        else:
            if (element['description'] != None):
                message = element['description'].encode('utf-8').replace('\n',' ').replace('\r', ' ').replace('\t',' ').strip()
            else:
                message = 'None'
        line = facebookID + '\t' + screenName + '\t' + createTime + '\t' + message
        print line
        list_info.append(line)

    print len(list_info)

    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="ducthong", # your password
                      db="2015_allschemas") # name of the data base
    cur = db.cursor()

    t0 = time()
    cnt = 0
    list_error = []

    for line in list_info:
        cnt += 1
        # print (cnt)

        split_line = line.strip().split('\t')
        facebookID = split_line[0]
        screenName = split_line[1]
        createTime = split_line[2]
        post = split_line[3]

        sql = """INSERT INTO facebook_BusPosts(facebookID, screenName, createTime, post) VALUES ('""" \
              + facebookID + "','" + screenName.replace('\'','\'\'').replace('\\', '\\\\') + "','" + createTime + "','" \
              + post.replace('\'','\'\'').replace('\\', '\\\\') + "')"
        # print (sql)
        try:
            cur.execute(sql)
            db.commit()
        except:
            print (facebookID + '\t' + sql)
            list_error.append(facebookID + '\t' + sql)

        if (cnt % 1000 == 0):
            print 'Processing ' + str(cnt) + ' records takes ' + str(time() - t0)

    write_file(path, name_write + '_errorPost', list_error)
    print ('Done process')

    db.close()


def json_facebookBusNews(path, name, name_write, command):
    with open(path + '/' + name) as data_file:
        data = json.load(data_file)

    SMRT = '566549713366262'  # SMRT
    LTA = '132581033478808'  # Land Transport Authority - We Keep Your World Moving
    CNAS = '93889432933'  # Channel NewsAsia Singapore
    TST = "129011692114"  # The Straits Times
    Today = "147858757571"  # TODAY
    C8N = "140711089280549"  # Channel 8 News

    list_info = list()
    for element in data:
        # print element

        facebookID = element['id']
        screenName = ''
        if SMRT == element['biz_id']:
            screenName = 'SMRT'
        elif LTA == element['biz_id']:
            screenName = 'Land Transport Authority - We Keep Your World Moving'
        elif CNAS == element['biz_id']:
            screenName = 'Channel NewsAsia Singapore'
        elif TST == element['biz_id']:
            screenName = 'The Straits Times'
        elif Today == element['biz_id']:
            screenName = 'TODAY'
        elif C8N == element['biz_id']:
            screenName = 'Channel 8 new'

        createTime = element['created_time']

        message = ''
        if element['message'] is not None:
            message = element['message'].encode('utf-8').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        else:
            if element['description'] is not None:
                message = element['description'].encode('utf-8').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            else:
                message = 'None'

        line = facebookID + '\t' + screenName + '\t' + createTime + '\t' + message
        print line
        list_info.append(line)

    if command == 'nec_demo':
        # list_write = list()
        # for value in list_info:
        #     split_value = value.split('\t')
        #     createAt = split_value[2]
        #
        #     if ('2015-08' in createAt) or ('2015-09' in createAt) or ('2015-10' in createAt):
        #         list_write.append(value)

        write_file(path, name_write, list_info)

    # db = MySQLdb.connect(host="localhost", # your host, usually localhost
    #                  user="root", # your username
    #                   passwd="ducthong", # your password
    #                   db="2015_allschemas") # name of the data base
    # cur = db.cursor()
    #
    # t0 = time()
    # cnt = 0
    # list_error = []
    #
    # for line in list_info:
    #     cnt += 1
    #     # print (cnt)
    #
    #     split_line = line.strip().split('\t')
    #     facebookID = split_line[0]
    #     screenName = split_line[1]
    #     createTime = split_line[2]
    #     post = split_line[3]
    #
    #     # sql = """INSERT INTO facebook_BusNews(facebookID, screenName, createTime, post) VALUES ('""" \
    #     #       + facebookID + "','" + screenName.replace('\'','\'\'').replace('\\', '\\\\') + "','" + createTime + "','" \
    #     #       + post.replace('\'','\'\'').replace('\\', '\\\\') + "')"
    #     sql = """INSERT INTO facebook_BusNews_ver2(facebookID, screenName, createTime, post) VALUES ('""" \
    #           + facebookID + "','" + screenName.replace('\'', '\'\'').replace('\\', '\\\\') + "','" + createTime + "','" \
    #           + post.replace('\'', '\'\'').replace('\\', '\\\\') + "')"
    #     # print (sql)
    #     try:
    #         cur.execute(sql)
    #         db.commit()
    #     except:
    #         print (facebookID + '\t' + sql)
    #         list_error.append(facebookID + '\t' + sql)
    #
    #     if cnt % 1000 == 0:
    #         print 'Processing ' + str(cnt) +  ' records takes ' + str(time() - t0)
    #
    # write_file(path, name_write + '_errorPost', list_error)
    # print ('Done process')

    # db.close()
#####################################################################################################
#####################################################################################################
########### TWITTER
def json_tweet(path, name, name_write):
    # Use to extract json text on json file
    # Use for tweeter dataset
    with open(path + '/' + name) as data_file:
        data = json.load(data_file)

    cnt = 0
    list_ = []
    t_first = time()
    for element in data:
        cnt += 1
        user = element['user']
        list_.append(str(element['id']) + '\t' + user['screenName'] + '\t' + str(element['createAtMilis'])
                     + '\t' + element['text'].encode('utf-8').replace('\n','').strip()
                     + '\t' + str(element['retweetCount']) + '\t' + str(element['favoriteCount']))
        print (str(element['id']) + '\t' + user['screenName'] + '\t' + str(element['createAtMilis'])
                     + '\t' + element['text'].encode('utf-8').replace('\n','').strip()
                     + '\t' + str(element['retweetCount']) + '\t' + str(element['favoriteCount']))
        if cnt % 10000 == 0:
            print ('Loading ' + str(cnt) + ' records take ' + str(time() - t_first) + ' secs')

    # if os.path.exists(path + "/" + name_write + '.csv'):
    #     print("The file already appears in the path folder")
    # else:
    #     file_ = file(path + "/" + name_write + '.csv', 'w')
    #     for each in list_:
    #         file_.write(each + '\n')
    #         print (each)
    #     file_.close()


#####################################################################################################
#####################################################################################################
def extract_tweet_post(str_json):
    # don't need to worry about retweetedStatus
    id = str(str_json['id'])
    user = str_json['user']
    screenName = user['screenName']
    createdAt = str(str_json['createdAt'])
    # text = str_json['text'].encode('utf-8').replace('\n','').replace('\t','').strip()
    text = str_json['text'].encode('utf-8').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
    # text = str_json['text'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()

    # if id == '557750586159157250':
    #     print text
    #     quit()

    # text = unicode(str_json['text'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip())

    # if (id == '551933944875065344'):
    #     print ('testing')
    #
    # if ('\n' in text):
    #     split_text = text.split('\n')
    #     new_text = ''
    #     for line in split_text:
    #         new_text = new_text + line + ' '
    #     text = new_text.strip()

    retweetCount = str(str_json['retweetCount'])
    favoriteCount = str(str_json['favoriteCount'])
    return id + '\t' + screenName + '\t' + createdAt + '\t' + text + '\t' + retweetCount + '\t' + favoriteCount


def extract_retweet(str_json):
    # the retweet is included the retweetedStatus which are the original post of tweet
    retweetedStatus = str_json['retweetedStatus']
    tweet_post = extract_tweet_post(retweetedStatus)

    retweet_id = str(str_json['id'])
    user = str_json['user']
    retweet_screenName = user['screenName']
    split_post = tweet_post.split('\t')
    post_id = split_post[0]
    post_screenName = split_post[1]
    retweet = retweet_id + '\t' + retweet_screenName + '\t' + post_id + '\t' + post_screenName

    d = {'post': tweet_post, 'retweet': retweet}
    return d


def json_tweet_filtering(path, name, name_write):
    # Use for tweet data set
    # For each tweets, dectect post_tweet and retweet and extract the information
    with open(path + '/' + name) as data_file:
        data = json.load(data_file)

    cnt_post = 0
    cnt_retweet = 0
    list_post = list()
    list_retweet = list()

    for element in data:
        post_tweet = element['retweetedStatus']

        if post_tweet is not None:  # this tweet is a retweet
            cnt_retweet += 1
            dict_retweet = extract_retweet(element)
            post = dict_retweet['post']
            retweet = dict_retweet['retweet']
            # if (post not in list_post):
            #     list_post.append(post)
            # if (retweet not in list_retweet):
            #     list_retweet.append(retweet)
            list_post.append(post)
            list_retweet.append(retweet)
            print (str(cnt_retweet) + '\t' + 'Retweet_id:' + '\t' + str(element['id']))
        else:
            cnt_post += 1
            post = extract_tweet_post(element)
            # if (post not in list_post):
            #     list_post.append(post)
            list_post.append(post)
            print (str(cnt_post) + '\t' + 'Post_tweet_id:' + '\t' + str(element['id']))

    write_file(path, name_write + '_post', list_post)
    # write_file(path, name_write + '_retweet', list_retweet)
    # print (str(cnt_retweet) + '\t' + str(cnt_post))
    # print (str(len(list_post)) + '\t' + str(len(list_retweet)))

    # db = MySQLdb.connect(host="localhost", # your host, usually localhost
    #                  user="root", # your username
    #                   passwd="ducthong", # your password
    #                   db="twitter_bus") # name of the data base
    #
    # # you must create a Cursor object. It will let
    # #  you execute all the queries you need
    # cnt = 0
    # t0 = time()
    # cur = db.cursor()
    #
    # list_error = []
    # for line in list_post:
    #     cnt += 1
    #     print (cnt)

    #     split_line = line.strip().split('\t')
    #     tweetID = split_line[0]
    #     screenName = split_line[1]
    #     createTime = split_line[2]
    #     tweetText = split_line[3]
    #     retweetCnt = split_line[4]
    #     favoriteCnt = split_line[5]
    #
    #     sql = """INSERT INTO twitter_posts(tweetID, screenName, createTime, tweetText, retweetCnt, favoriteCnt) VALUES ('""" + tweetID + "','" + screenName + "','" + createTime + "','" + tweetText.replace('\'','\'\'').replace('\\', '\\\\') + "'," + retweetCnt + "," + favoriteCnt + ")"
    #     # print (sql)
    #     try:
    #         cur.execute(sql)
    #         db.commit()
    #     except:
    #         print (tweetID + '\t' + sql)
    #         list_error.append(tweetID + '\t' + sql)
    #
    #     if (cnt % 1000 == 0):
    #         print 'Processing ' + str(cnt) +  ' records takes ' + str(time() - t0)
    #
    # write_file(path, name_write + '_errorPost', list_error)
    # print ('Done process')

    # db.close()

#####################################################################################################
#####################################################################################################
def json_filtering(path, name, name_write, command):
    # user command to identify when we use Json for Twitter or Facebook dataset
    with open(path + '/' + name) as data_file:
        data = json.load(data_file)

    list_post, list_retweet = list(), list()
    cnt_retweet, cnt_post = 0, 0

    if command == 'twitter':
        for element in data:
            post = extract_tweet_post(element)
            list_post.append(post)
            print (str(cnt_post) + '\t' + 'Post_tweet_id:' + '\t' + str(element['id']))

        write_file(path, name_write + '_post', list_post)
        print len(list_post), len(list_retweet)


def insert_SQL(path, name, tablename, command):
    data = load_file(path, name)

    # for element in data:
    #     print element
    # print len(data)

    if command == 'twitter':
        create_table = "CREATE TABLE " + tablename \
            + "(tweetID VARCHAR(200) NULL COMMENT '', screenName VARCHAR(200) NULL COMMENT ''," \
            + "createTime TIMESTAMP NULL COMMENT '', tweetText TEXT NULL COMMENT ''," \
            + "retweetCnt INT NULL COMMENT '', favCnt INT NULL COMMENT '');"

    elif command == 'facebook':
        create_table = "CREATE TABLE " + tablename \
            + "(facebookID VARCHAR(200) NULL COMMENT '', screenName VARCHAR(500) NULL COMMENT ''," \
            + "createTime TIMESTAMP NULL COMMENT '', post TEXT NULL COMMENT '');"
    print create_table

    # load data to desktop
    # db = MySQLdb.connect(host="localhost",  # your host, usually localhost
    #                  user="root",  # your username
    #                   passwd="ducthong",  # your password
    #                   db="2015_demo_dec")  # name of the data base

    # load data to server
    db = MySQLdb.connect(host="10.0.106.71",  # your host, usually localhost
                     user="vdthoang",  # your username
                      passwd="LARCuser1142",  # your password
                      db="nec_demo")  # name of the data base

    cur = db.cursor()
    cur.execute(create_table)
    # list_error, cnt, t0 = list(), 0, time()
    list_error, cnt = list(), 0
    if command == 'twitter':
        for line in data:
            cnt += 1
            split_line = line.strip().split('\t')
            tweetID, screenName, createTime = split_line[0], split_line[1], split_line[2]
            tweetText, retweetCnt, favCnt = split_line[3], split_line[4], split_line[5]

            # convert to timespam
            # epoch_createTime = convertTime_twitter(createTime)
            timespam = timeSpam_twitter(createTime)

            sql = """INSERT INTO """ + tablename + "(tweetID, screenName, createTime, tweetText, retweetCnt, favCnt) VALUES ('""" \
                  + tweetID + "','" + screenName + "','" + timespam + "','" \
                  + tweetText.replace('\'', '\'\'').replace('\\', '\\\\') + "'," + retweetCnt + "," + favCnt + ")"
            # print sql

            try:
                cur.execute(sql)
                db.commit()
            except ():
                print (tweetID + '\t' + sql)
                list_error.append(tweetID + '\t' + sql)

            if cnt % 1000 == 0:
                # print 'Processing ' + str(cnt) + ' records take ' + str(time() - t0)
                print 'Processing ' + str(cnt)

    elif command == 'facebook':
        for line in data:
            cnt += 1
            split_line = line.strip().split('\t')
            facebookID, screenName, createTime, post = split_line[0], split_line[1], split_line[2], split_line[3]

            split_post = post.split()
            if len(split_post) > 1:
                sql = """INSERT INTO """ + tablename + "(facebookID, screenName, createTime, post) VALUES ('""" \
                      + facebookID + "','" + screenName.replace('\'', '\'\'').replace('\\', '\\\\') \
                      + "','" + createTime + "','" + post.replace('\'', '\'\'').replace('\\', '\\\\') + "');"

                # print sql
                try:
                    cur.execute(sql)
                    db.commit()
                except ():
                    print (facebookID + '\t' + sql)
                    list_error.append(facebookID + '\t' + sql)

            if cnt % 1000 == 0:
                # print 'Processing ' + str(cnt) + ' records take ' + str(time() - t0)
                print 'Processing ' + str(cnt)

    write_file(path, tablename + '_errorPost', list_error)
    print ('Done process')
    db.close()


#####################################################################################################
#####################################################################################################
if __name__ == '__main__':
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter'
    # name = 'plr_sg_tweet_2015.json'
    # name_write = 'plr_sg_tweet_2015'

    path = 'd:/'
    name = 'plr_sg_tweet_2015_PeiHua.json'
    name_write = 'plr_sg_tweet_2015_PeiHua'

    # json_tweet(path, name, name_write)
    json_tweet_filtering(path, name, name_write)

    # path = 'd:/Project/Transportation_SMU-NEC_collaboration/Data_NEC_oldDATA'
    # name = 'plr_sg_tweet_2015_Jan_Dec.json'
    # name_write = 'plr_sg_tweet_2015_Jan_Dec'
    # json_tweet_filtering(path, name, name_write)

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook'
    # name = 'sg_fb_biz_feed.json'
    # name_write = 'sg_fb_biz_feed'
    # json_facebook(path, name, name_write)

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook'
    # name = 'sg_fb_biz_feed_BusTransport.json'
    # name_write = 'sg_fb_biz_feed_BusTransport'
    # json_facebookBusTransport(path, name, name_write)

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    # name = 'sg_fb_biz_feed_BusNews.json'
    # name_write = 'sg_fb_biz_feed_BusNews'

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    # name = 'sg_fb_biz_feed_BusNews_ver2.json'
    # name_write = 'sg_fb_biz_feed_BusNews_ver2'
    # json_facebookBusNews(path, name, name_write)

    #####################################################################################################
    # TWITTER
    # using json to get all the necessary information
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/twitter'
    # name = 'plr_sg_tweet_2015_Aug_Oct.json'
    # name_write = 'plr_sg_tweet_2015_Aug_Oct_post'
    # json_filtering(path, name, name_write, command='twitter')

    # load data to the database
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/twitter'
    # name = 'plr_sg_tweet_2015_Aug_Oct_post.csv'
    # table_name = 'tweet_2015_timespam'
    # insert_SQL(path, name, table_name, command='twitter')


    #####################################################################################################
    # FACEBOOK
    # using json to get all the necessary information
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/facebook'
    # # name = 'sg_fb_biz_feed_BusNews_Oct.json'
    # name = 'sg_fb_biz_feed_BusNews_Aug_Oct_new.json'
    # name_write = 'facebook_2015'
    # json_facebookBusNews(path, name, name_write, command='nec_demo')  # we get data from Aug. to Oct. 2015

    # load data to the database
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/facebook'
    # name = 'facebook_2015.csv'
    # table_name = 'facebook_2015'
    # insert_SQL(path, name, table_name, command='facebook')
