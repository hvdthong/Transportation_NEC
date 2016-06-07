__author__ = 'vdthoang'
import MySQLdb
from main.writeFile import write_file


def data_Twitter(path, command):
    if command == 'twitter':
        sql = 'select tweetID, screenName, createTime, tweetText from twitter_icswsm_all order by tweetID'
    elif command == 'twitter_bussvc':
        sql = 'select * from twitter_icwsm_bussvc order by tweetID'
    elif command == 'twitter_road':
        sql = 'select * from twitter_icwsm_road order by tweetID'
    elif command == 'twitter_busstop':
        sql = 'select * from twitter_icwsm_busstop order by tweetID'
    else:
        print 'Wrong command'
        quit()

    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                      passwd="ducthong",  # your password
                      db="2015_allschemas")  # name of the data base
    cur = db.cursor()

    # Use all the SQL you like
    cur.execute(sql)
    list_ = list()
    for row in cur.fetchall():
        if command == 'twitter':
            line_row = row[0] + '\t' + row[1] + '\t' + row[2] + '\t' + row[3]
        else:
            line_row = row[0] + '\t' + row[1] + '\t' + row[2] + '\t' + row[3] + '\t' + row[4]
        print line_row
        list_.append(line_row)
    print len(list_)

    write_file(path, command, list_)


if __name__ == '__main__':
    # command = 'twitter'
    # command = 'twitter_bussvc'
    # command = 'twitter_road'
    command = 'twitter_busstop'
    path_ = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data'
    data_Twitter(path_, command=command)
