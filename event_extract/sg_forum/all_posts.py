from main.convertTime import week_second
from main.convertTime import day_second
from main.convertTime import convertTime_allpost

__author__ = 'vdthoang'

import MySQLdb
#note that we load the data on server into text file
def load_time_sgforum_all_post():
    db = MySQLdb.connect(host="10.0.106.71", # your host, usually localhost
                         user="vdthoang", # your username
                          passwd="LARCuser1142", # your password
                          db="sgforums") # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    # Use all the SQL you like
    cur.execute("select topic_id, post_id, published_date from all_posts order by published_date;") #call the database which name 'posts'
    list_sql = []
    for row in cur.fetchall():
        topic_id = str(row[0])
        post_id = str(row[1])
        published_date = str(row[2])
        #print (topic_id + '\t' + post_id + '\t' + published_date)
        list_sql.append(topic_id + '\t' + post_id + '\t' + published_date)
    cur.close()
    return list_sql

def get_time_convert_sgforum():
    ## get the time convert in sgforum
    db = MySQLdb.connect(host="10.0.106.71", # your host, usually localhost
                         user="vdthoang", # your username
                          passwd="LARCuser1142", # your password
                          db="sgforums") # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    # Use all the SQL you like
    cur.execute("select topic_id, post_id, published_date from all_posts order by published_date;") #call the database which name 'posts'
    list_sql = []
    for row in cur.fetchall():
        topic_id = str(row[0])
        post_id = str(row[1])
        published_date = str(row[2])
        print (topic_id + '\t' + post_id + '\t' + str(convertTime_allpost(published_date)))
        list_sql.append(topic_id + '\t' + post_id + '\t' + str(convertTime_allpost(published_date)))
    cur.close()
    return list_sql

def time_week_package_all_post(list_date, pack_str):
    if (pack_str == 'week'):
        pack_time = week_second()
    elif (pack_str == 'day'):
        pack_time = day_second()
    first = convertTime_allpost(list_date[0])
    last = convertTime_allpost(list_date[len(list_date) - 1])

    list_pack = []
    while (True):
        if (first < last):
            list_pack.append(str(first) + '\t' + str(first + pack_time))
            first = first + pack_time
        else:
            break
    return list_pack

def histogram_pin(list_all, list_pack):
    for pack in list_pack:
        split_pack = pack.split('\t')
        first = int(split_pack[0])
        second = int(split_pack[1])

        count = 0
        for line in list_all:
            split_line = line.split('\t')
            published_date = split_line[2]
            time_ = convertTime_allpost(published_date)
            if (time_ >= first and time_ < second):
                count += 1
        print (str(first) + '\t' + str(second) + '\t' + str(count))

if __name__ == '__main__':
    # get all_posts in sql and draw the bin graph
    list_all = load_time_sgforum_all_post()
    list_date = []
    for line in list_all:
        split_line = line.split('\t')
        list_date.append(split_line[2])
        #print (split_line[2])

    #list_pack_time = time_week_package_all_post(list_date, 'week')
    list_pack_time = time_week_package_all_post(list_date, 'day')
    # for each in list_pack_time:
    #     print (each)
    # print (len(list_pack_time))
    histogram_pin(list_all, list_pack_time)

    #get_time_convert_sgforum()


