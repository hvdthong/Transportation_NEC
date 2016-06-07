__author__ = 'vdthoang'
import MySQLdb
from main.writeFile import write_file


if __name__ == '__main__':
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                        user="root",  # your username
                        passwd='ducthong',
                        db="2015_allschemas")  # name of the data base

    # you must create a Cursor object. It will let
    # you execute all the queries you need
    cur = db.cursor()
    query_sql = 'select distinct tweetID from twitter_posts_distinct_ver2 order by tweetID;'
    # Use all the SQL you like
    # cur.execute("select * from posts;")  # call the database which name 'posts'
    cur.execute(query_sql)  # call the database which name 'posts'

    # print all the first cell of all the rows
    listText = list()
    for row in cur.fetchall():
        print row[0]
        listText.append(row[0])

    write_file('d:/', 'tweetID', listText)
