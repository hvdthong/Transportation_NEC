'''
Created on 22 Jul 2015

@author: vdthoang
'''
import MySQLdb

from main.extract_tag import extract_tags
from main.writeFile import write_file

#note that we load the data on server into text file 
db = MySQLdb.connect(host="10.0.106.71", # your host, usually localhost
                     user="vdthoang", # your username
                      passwd="LARCuser1142", # your password
                      db="sgforums") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

# Use all the SQL you like
cur.execute("select post_id, summary from all_posts;") #call the database which name 'posts'

list_sql = []
list_write = []

for row in cur.fetchall():
    post_id = str(row[0])
    summray = str(row[1])
    #print (post_id + '\t' + summray)    
    list_sql.append(post_id + '\t' + summray)
    

for line in list_sql:
    split_line = line.split('\t')    
    print (split_line[0] + '\t' + extract_tags(split_line[1]))
    list_write.append(split_line[0] + '\t' + extract_tags(split_line[1]))
    
path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts'   
write_file(path, 'posts_extract', list_write) #extract texts and write it on csv file
cur.close()