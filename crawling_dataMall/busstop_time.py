__author__ = 'vdthoang'
import MySQLdb


def all_bus_svcs():
    # note that we load the data on server into text file
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                         passwd="ducthong",  # your password
                         db="2015_allschemas")  # name of the data base

    # you must create a Cursor object. It will let
    # you execute all the queries you need
    cur = db.cursor()
    query_sql = 'select distinct numSvc from bussvc_mytransport'

    # Use all the SQL you like
    # cur.execute("select * from posts;")  # call the database which name 'posts'
    cur.execute(query_sql)  # call the database which name 'posts'

    # print all the first cell of all the rows
    list_text = list()
    for row in cur.fetchall():
        list_text.append(row[0])
    return list_text


if __name__ == '__main__':
    list_bus = all_bus_svcs()
    print len(list_bus)
