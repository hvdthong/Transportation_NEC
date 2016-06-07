'''
Created on 20 Jul 2015

@author: vdthoang
'''
import MySQLdb

db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                      passwd="ducthong",  # your password
                      db="sgforums_permanent")  # name of the data base

#  you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

# Use all the SQL you like
cur.execute("select distinct author from posts")
list_author = []
# print all the first cell of all the rows
# for row in cur.fetchall():
#     row = str(row)
#     list_author.append(row[1:len(row)-2])

while (1):
    row = cur.fetchone()
    if row == None:
        break
    
    list_author.append(row[0])
    print str(row[0])
    
# print list_author[0]
# print ('select count(distinct topic_id) as cnt, author from posts where author = ' + str(list_author[0]) + '')

list_author_topic = []
for author in list_author:
    cur.execute('select count(distinct topic_id) as cnt, author from posts where author = \'' + str(author) + '\'')
    for row in cur.fetchall():
        print str(row[0]) + '\t' + str(row[1])

# for each in list_author:
#     print each