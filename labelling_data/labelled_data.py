__author__ = 'vdthoang'
import MySQLdb
from nltk.tokenize import sent_tokenize
import sys
from main.writeFile import write_file


reload(sys)
sys.setdefaultencoding('utf8')


def calling_table(data):
    if data == 'facebook':
        sql = "select post from facebook_2015_Entity where (CRF like '%1%') or (CRF like '%3%') or (CRF like '%2%') order by facebookID;"
    elif data == 'twitter':
        sql = "select distinct tweetText from tweet_2015_filtering_ver3_roads r, twitter_posts p where r.tweetID = p.tweetID " \
            + "union select distinct tweetText from tweet_2015_filtering_ver3_busstop b, twitter_posts p where b.tweetID = p.tweetID " \
            + "union select distinct tweetText from tweet_2015_filtering_ver3_busservices s, twitter_posts p where s.tweetID = p.tweetID "
    else:
        print 'Give the correct for data'
        quit()
    return sql


def loading_labelData(sql, data):
    if data == 'facebook':
        # load data to server
        db = MySQLdb.connect(host="10.0.106.71",  # your host, usually localhost
                         user="vdthoang",  # your username
                          passwd="LARCuser1142",  # your password
                          db="nec_demo")  # name of the data base
    elif data == 'twitter':
        # load data to server
        db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                          passwd="ducthong",  # your password
                          db="2015_allschemas")  # name of the data base
    else:
        print 'You need to give the correct command'
        quit()

    cur = db.cursor()
    # Use all the SQL you like
    cur.execute(sql)

    list_row_id = list()
    # print all the first cell of all the rows
    for row in cur.fetchall():
        list_row_id.append(row[0])

    return list_row_id


def split_sentence_event(list_post):
    list_sent_split = list()
    cnt_error, cnt_id = 0, 0
    for i in range(0, len(list_post)):
        id, post = cnt_id, list_post[i]
        try:
            sent_tokenize_list = sent_tokenize(post.strip())
            for sent in sent_tokenize_list:
                print str(id) + '\t' + sent
                list_sent_split.append(str(id) + '\t' + sent)
        except UnicodeDecodeError:
            print id, sent
            cnt_error += 1
        cnt_id += 1
    print len(list_sent_split), cnt_error
    return list_sent_split


def split_sentence_CRF(list_post, path_write, name):
    list_sent_split, list_sent_origin = list(), list()
    for i in range(0, len(list_post)):
        post = list_post[i].replace("\"", '')
        split_post, sentence = post.split(), ''

        for value in split_post:
            sentence = sentence + value + '\t'
        # print sentence.strip()
        # print post
        # print '\n'
        list_sent_split.append(sentence.strip()), list_sent_split.append('\n')
        list_sent_origin.append(post), list_sent_origin.append('\n')
    print len(list_sent_split), len(list_sent_origin)
    write_file(path_write, name + '_CRF', list_sent_split)
    write_file(path_write, name + '_origin', list_sent_origin)
    return None


if __name__ == '__main__':
    # using for Facebook
    # sql = calling_table(data='facebook')
    # list_post = loading_labelData(sql, data='facebook')
    # # split_sentence_event(list_post)
    #
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF/labelingStudent'
    # name = 'facebook'
    # split_sentence_CRF(list_post, path_write, name)

    # using for Twitter
    sql = calling_table(data='twitter')
    list_post = loading_labelData(sql, data='twitter')

    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/labelingStudent'
    name = 'twitter'
    split_sentence_CRF(list_post, path_write, name)
