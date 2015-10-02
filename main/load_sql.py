'''
Created on 14 Jul 2015

@author: vdthoang
'''
from main.writeFile import write_file
def makeString(row):
    #this function use to make a single string from multiple column on row; \t is used to separate between column
    text = ''
    for each in row:
        text = text + str(each) + '\t'
    return text.strip()

import MySQLdb

#note that we load the data on server into text file 
db = MySQLdb.connect(host="10.0.106.71", # your host, usually localhost
                     user="vdthoang", # your username
                      passwd="LARCuser1142", # your password
                      db="sgforums") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

# Use all the SQL you like
cur.execute("select * from posts;") #call the database which name 'posts'

# print all the first cell of all the rows
listText = []
for row in cur.fetchall():
    print makeString(row)
    listText.append(makeString(row))
    
path = "D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums"
name = "sgforums_posts"
write_file(path, name, listText)
    
    