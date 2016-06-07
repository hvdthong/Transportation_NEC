__author__ = 'vdthoang'
import MySQLdb
import gensim
from scipy import spatial
from CRF_labeling.filterText_CRF import filter_eachTok_rmLinks
from main.writeFile import write_file


def load_TwitterText():
    # note that we load the data on server into text file
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                         passwd="ducthong",  # your password
                         db="2015_allschemas")  # name of the data base
    # you must create a Cursor object. It will let
    # you execute all the queries you need
    cur = db.cursor()
    query_sql = 'select distinct tweetText from twitter_icwsm_correct;'

    # Use all the SQL you like
    # cur.execute("select * from posts;")  # call the database which name 'posts'
    cur.execute(query_sql)  # call the database which name 'posts'

    # print all the first cell of all the rows
    list_text = list()
    for row in cur.fetchall():
        list_text.append(row[0])
    print len(list_text)
    return list_text


def wordVector(sents, path_w, name_w, win_size):
    list_all = list()
    for i in range(0, len(sents)):
        split_sent = sents[i].split()
        tokens = list()
        for token in split_sent:
            token_filter = filter_eachTok_rmLinks(token, 'twitter')
            if len(token_filter) > 0:
                tokens.append(token_filter.lower())
        print i
        list_all.append(tokens)

    model = gensim.models.Word2Vec(list_all, size=win_size, window=5, min_count=1, workers=5)
    print model.most_similar(['crowd'])

    list_write = list()
    for i in range(0, len(model.index2word)):
        # print model.index2word[i], model.syn0norm[i]
        line = model.index2word[i]
        for value in model.syn0norm[i]:
            line += '\t' + str(value)
        line = line.strip()
        list_write.append(line)
        # print line
    write_file(path_w, name_w + '_%i' % win_size, list_write)


if __name__ == '__main__':
    tweets = load_TwitterText()
    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/WordVector'
    name_write = 'word_vec'
    win_size = 200
    wordVector(tweets, path_write, name_write, win_size)
