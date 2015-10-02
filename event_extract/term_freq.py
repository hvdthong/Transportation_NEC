# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'vdthoang'
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
import MySQLdb
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.porter import *

############using with NLTK
def term_freq_all(path, name):
    file = path + '/' + name

    fdist = FreqDist()
    list_line = []
    with open(file) as f:
        for line in f:
            split_line = line.split('\t')
            words = nltk.word_tokenize(split_line[1].decode('utf-8').lower().strip())
            fdist.update(words)
            print split_line[0]

            # list_stem = []
            # for token in words:
            #     # st = LancasterStemmer()
            #     # try:
            #     #     list_stem.append(st.stem(token).decode('utf-8'))
            #     # except:
            #     #     print (split_line[0])
            #
            #     st = PorterStemmer()
            #     try:
            #         list_stem.append(st.stem(token).decode('utf-8'))
            #     except:
            #         print (split_line[0])
            # fdist.update(list_stem)


            #print (line)

    print ('==========================================')
    print ('==========================================')
    print (len(fdist))
    stop = stopwords.words('english')


    for value in fdist.most_common(15000):
        # if (value[0] not in stop and (len(value[0]) >= 4)):
        if (value[0] not in stop):
            print (str(value[0].encode('utf-8')) + '\t' + str(value[1]))

def term_freq_time(first, last):
    ## get the time convert in sgforum
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                         user="root", # your username
                          passwd="ducthong", # your password
                          db="sgforums_singaporebuses") # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    # Use all the SQL you like
    sql = "select p.post_id, s.createdAtSecond, p.summary from posts_filter p, posts_createatsecond s where p.post_id = s.post_id and s.createdAtSecond >= " \
          + str(first) + " and s.createdAtSecond <= " + str(last) + " order by s.createdAtSecond;"
    cur.execute(sql) #call the database which name 'posts'

    fdist = FreqDist()
    for row in cur.fetchall():
        post_id = str(row[0])
        createdAtSecond = str(row[1])
        summary = unicode(str(row[2]), errors='ignore')
        #print (post_id + '\t' + createdAtSecond + '\t' + summary)
        words = nltk.word_tokenize(summary.lower().strip().decode('utf-8'))
        # try:
        #     words = nltk.word_tokenize(summary.lower().strip().decode('utf-8'))
        # except:
        #     print (post_id + '\t' + summary)
        fdist.update(words)
    cur.close()
    print ('==========================================')
    print ('==========================================')
    print (len(fdist))
    stop = stopwords.words('english')

    for value in fdist.most_common(200):
        if (value[0] not in stop and len(value[0]) >= 3):
            print (str(value[0]).encode('utf-8') + '\t' + str(value[1]))

if __name__ == '__main__':
    ## week 72
    # first = 1435330575
    # last = 1435935375

    ## week 74
    # first = 1436540175
    # last = 1437144975

    ## day 422
    # first = 1428764175
    # last = 1428850575

    ## day 443
    # first = 1430578575
    # last = 1430664975
    # term_freq_time(first, last)

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts'
    # name = 'posts_filter_v2.csv'

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter'
    # name = 'tweet_2015_filtering.csv'

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook'
    # name = 'sg_fb_biz_feed_filtering.csv'

    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    name = 'sg_fb_biz_feed_BusNews_filtering.csv'

    term_freq_all(path, name)

