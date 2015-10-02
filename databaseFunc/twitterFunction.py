from main.filter_text import filter_token

__author__ = 'vdthoang'
import MySQLdb
from main.convertTime import convertTime_twitter
from time import time
import time
from main.writeFile import write_file

def filtering_tweetText(path, name_write):
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="ducthong", # your password
                      db="twitter_bus") # name of the data base
    cur = db.cursor()
    list_write = []

    cnt = 0
    sql = 'select tweetID, tweetText from twitter_posts_distinct'
    cur.execute(sql)
    for row in cur.fetchall():
        tweetID = row[0]
        tweetText = filter_token(row[1])

        print (tweetID + '\t' + tweetText)
        list_write.append(tweetID + '\t' + tweetText)

    db.close()
    write_file(path, name_write, list_write)

if __name__ == '__main__':
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter'
    name_write = 'plr_sg_tweet_2015_filtering'
    filtering_tweetText(path, name_write)