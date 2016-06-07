'''
Created on 14 Jul 2015

@author: vdthoang
'''
from main.writeFile import write_file
import MySQLdb


def query(command):
    if command == 'recent':
        string = "select * from posts where published_date like '%2015-08%' union " \
            + "select * from posts where published_date like '%2015-09%' union select * from posts " \
            + "where published_date like '%2015-10%' order by published_date;"
        return string
    else:
        print 'Give the correct command'
        quit()


def makeString(row):
    # this function use to make a single string from multiple column on row; \t is used to separate between column
    text = ''
    for each in row:
        if type(each) == str:  # check if the column is string or the other types (int, long, etc.)
            text = text + str(each.replace('\t', ' ')) + '\t'
        else:
            text = text + str(each) + '\t'
        # text = text + str(each) + '\t'
    return text.strip()


def retrive_data(query_sql, path, name):
    # note that we load the data on server into text file
    db = MySQLdb.connect(host="10.0.106.71",  # your host, usually localhost
                         user="vdthoang",  # your username
                          passwd="LARCuser1142",  # your password
                          db="sgforums")  # name of the data base

    # you must create a Cursor object. It will let
    # you execute all the queries you need
    cur = db.cursor()

    # Use all the SQL you like
    # cur.execute("select * from posts;")  # call the database which name 'posts'
    cur.execute(query_sql)  # call the database which name 'posts'

    # print all the first cell of all the rows
    listText = list()
    for row in cur.fetchall():
        print makeString(row)
        listText.append(makeString(row))

    print len(listText)
    write_file(path, name, listText)


if __name__ == '__main__':
    # path = "D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums"
    # name = "sgforums_posts"

    path = 'D:/'
    name = 'sgforums_posts_Aug_Nov'
    print query(command='recent')
    retrive_data(query(command='recent'), path, name)

