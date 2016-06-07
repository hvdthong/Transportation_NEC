__author__ = 'vdthoang'
import MySQLdb
import random


def random_selection(sql):
    list_text = list()
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                      passwd="ducthong",  # your password
                      db="2015_allschemas")  # name of the data base
    cur = db.cursor()

    # Use all the SQL you like
    cur.execute(sql)
    for row in cur.fetchall():
        line = row[0]
        list_text.append(line)
        # print line
    return list_text

if __name__ == '__main__':
    sql = 'select tweetText from twitter_icswsm_all order by tweetID'
    list_ = random_selection(sql)
    print len(list_)
    list_random = random.sample(list_, 500)

    for text in list_random:
        print text
