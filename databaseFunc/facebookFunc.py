__author__ = 'vdthoang'
from main.filter_text import filter_token
import MySQLdb
from main.writeFile import write_file


def filtering_facebookText(path, name_write):
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="ducthong", # your password
                      db="facebook_bus") # name of the data base
    cur = db.cursor()
    list_write = []

    cnt = 0
    sql = 'select facebookID, post from facebook_posts_distinct'
    cur.execute(sql)
    for row in cur.fetchall():
        tweetID = row[0]
        tweetText = filter_token(row[1])

        print (tweetID + '\t' + tweetText)
        list_write.append(tweetID + '\t' + tweetText)

    db.close()
    write_file(path, name_write, list_write)

def filtering_facebookBusText(path, name_write):
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="ducthong", # your password
                      db="2015_allschemas") # name of the data base
    cur = db.cursor()
    list_write = []

    cnt = 0
    sql = 'select facebookID, post from facebook_busposts'
    cur.execute(sql)
    for row in cur.fetchall():
        tweetID = row[0]
        tweetText = filter_token(row[1])

        print (tweetID + '\t' + tweetText)
        list_write.append(tweetID + '\t' + tweetText)

    db.close()
    write_file(path, name_write, list_write)

def filtering_facebookBusNews(path, name_write):
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="ducthong", # your password
                      db="2015_allschemas") # name of the data base
    cur = db.cursor()
    list_write = []

    cnt = 0
    # sql = 'select facebookID, post from facebook_busnews'
    sql = 'select facebookID, post from facebook_busnews_ver2'
    cur.execute(sql)
    for row in cur.fetchall():
        tweetID = row[0]
        tweetText = filter_token(row[1])

        print (tweetID + '\t' + tweetText)
        list_write.append(tweetID + '\t' + tweetText)

    db.close()
    write_file(path, name_write, list_write)
if __name__ == '__main__':
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook'
    # name_write = 'sg_fb_biz_feed_filtering'
    # filtering_facebookText(path, name_write)

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook'
    # name_write = 'sg_fb_biz_feed_BusTransport_filtering'
    # filtering_facebookBusText(path, name_write)

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    # name_write = 'sg_fb_biz_feed_BusNews_filtering'

    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    name_write = 'sg_fb_biz_feed_BusNews_filtering_ver2'
    filtering_facebookBusNews(path, name_write)

