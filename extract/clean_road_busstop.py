__author__ = 'vdthoang'
import MySQLdb
from main.writeFile import write_file


def filter_road(list_road):

    list_ = list()
    list_remove = list()
    for i in range(0, len(list_road)):
        value_first = list_road[i]
        for j in range(i + 1, len(list_road)):
            value_second = list_road[j]

            if (value_first in value_second) or (value_second in value_first):
                token_first = value_first.split()
                token_second = value_second.split()
                if len(token_first) > len(token_second):
                    if value_first not in list_:
                        list_.append(value_first)
                    list_remove.append(value_second)
                elif len(token_first) == len(token_second):
                    if value_first not in list_:
                        list_.append(value_first)
                    if value_second not in list_:
                        list_.append(value_second)
                    # list_.append(value_first)
                    # list_.append(value_second)
                elif len(token_first) < len(token_second):
                    if value_second not in list_:
                        list_.append(value_second)
                    list_remove.append(value_first)
                break

        if (value_first not in list_remove) and (value_first not in list_):
            list_.append(value_first)

        if i == len(list_road) - 1:
            if (value_first not in list_remove) and (value_first not in list_):
                list_.append(value_first)
    return list_


def clean_roadName(path, name_write, table):
    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                      passwd="ducthong",  # your password
                      db="2015_allschemas")  # name of the data base
    cur = db.cursor()
    list_write = list()

    cnt = 0
    # sql = 'select distinct post_id from ' + table  # sgforum
    # sql = 'select distinct facebookID from ' + table  # facebook
    # sql = 'select distinct tweetID from ' + table  # twitter

    sql = 'select distinct facebookID from ' + table  # facebook
    print sql
    cur.execute(sql)

    list_id = list()
    for row in cur.fetchall():
        list_id.append(row[0])
        # print row[0]

    print len(list_id)
    list_write = list()

    for id_value in list_id:
        # used for road
        # sql_id = 'select distinct road from ' + table + ' where post_id = ' \
        #          + str(id_value) + ' order by road' #sgforum
        # sql_id = 'select distinct road from ' + table + ' where facebookID = ' \
        #          + "'" + str(id_value) + "'" + ' order by road'  # facebook
        # sql_id = 'select distinct road from ' + table + ' where tweetID = ' \
        #          + "'" + str(id_value) + "'" + ' order by road'  # twitter

        # used for bus stop
        # sql_id = 'select distinct busstop from ' + table + ' where tweetID = ' \
        #          + "'" + str(id_value) + "'" + ' order by busstop'  # twitter
        sql_id = 'select distinct busstop from ' + table + ' where facebookID = ' \
                 + "'" + str(id_value) + "'" + ' order by busstop'  # facebook
        print(sql_id)
        cur.execute(sql_id)
        list_road = list()
        for row in cur.fetchall():
            list_road.append(row[0])
            # print row[0]

        # if (id_value == 11089472):
        #     print 'hello'

        if len(list_road) > 1:
            list_road = filter_road(list_road)

        for road in list_road:
            list_write.append(str(id_value) + '\t' + road)
            print str(id_value) + '\t' + road
    db.close()

    print (len(list_write))
    write_file(path, name_write, list_write)


if __name__ == '__main__':
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts'
    # name_write = 'posts_roads_ver2'
    # table = 'posts_roads_ver2'

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    # name_write = 'facebook_2015_BusNews_filtering_roads_ver2'
    # table = 'facebook_2015_BusNews_filtering_roads'

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter'
    # # name_write = 'tweet_2015_filtering_roads_ver3'
    # # table = 'tweet_2015_filtering_roads_ver2'
    #
    # name_write = 'tweet_2015_filtering_busstop_all_clean'
    # table = 'tweet_2015_ver4_stopall'
    # clean_roadName(path, name_write, table)

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    # name_write = 'facebook_2015_BusNews_filtering_busStop_all_clean'
    # table = 'facebook_2015_busnews_filtering_busstop_all'

    clean_roadName(path, name_write, table)
