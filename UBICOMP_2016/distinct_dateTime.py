__author__ = 'vdthoang'
import MySQLdb
from datetime import datetime
from main.writeFile import write_file


def load_data_ubicomp_distinct():
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                      passwd="ducthong",  # your password
                      db="2015_allschemas")  # name of the data base

    cur = db.cursor()

    # Use all the SQL you like
    cur.execute("select tweetID, createTime from twitter_icwsm_correct")
    data_id, data_text = list(), list()

    for row in cur.fetchall():
        data_id.append(row[0])
        date = datetime.strptime(row[1], '%b %d, %Y %H:%S:%M %p')
        data_text.append(date.strftime('%Y-%m-%d'))

    db.close()
    return data_id, data_text


def insert_data_daytime(list_):
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                      passwd="ducthong",  # your password
                      db="2015_allschemas")  # name of the data base

    cur = db.cursor()
    create_table = "CREATE TABLE IF NOT EXISTS twitter_icwsm_correct_daytime " \
                + "(tweetID VARCHAR(200) NULL COMMENT '', createTime timestamp NULL COMMENT '');"
    print create_table
    cur.execute(create_table)

    for i in range(0, len(list_)):
        split_ = list_[i].split('\t')
        tweetID, create_time = split_[0], split_[1]
        # sql = """INSERT INTO """ + table_name + "(tweetID, tweetText, CRF, bussvc) VALUES ('""" \
        #       + tweetID + "','" + tweetText.replace('\'', '\'\'').replace('\\', '\\\\') + "','" + CRF + "','" \
        #       + str(bussvc) + "')"

        sql = "INSERT INTO twitter_icwsm_correct_daytime (tweetID, createTime) VALUE('" \
              + tweetID + "','" + create_time + "');"
        print i, sql
        cur.execute(sql)
        db.commit()


def insert_data_daytime_append(list_):
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                      passwd="ducthong",  # your password
                      db="2015_allschemas")  # name of the data base

    cur = db.cursor()
    create_table = "CREATE TABLE IF NOT EXISTS twitter_icwsm_correct_daytime_test " \
                + "(tweetID VARCHAR(200) NULL COMMENT '', createTime timestamp NULL COMMENT '');"
    print create_table
    cur.execute(create_table)

    sql = "INSERT INTO twitter_icwsm_correct_daytime_test(tweetID, createTime) VALUE(%s,%s);"
    print sql
    cur.executemany(sql, list_)
    db.commit()


if __name__ == '__main__':
    id_, text_ = load_data_ubicomp_distinct()
    print len(id_), len(text_)

    path = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/ubicomp2016_paper/data'
    list_new = list()

    list_new_append = list()
    for i in range(0, len(id_)):
        print id_[i] + '\t' + text_[i]
        # list_new.append(id_[i] + '\t' + text_[i])
        list_new_append.append((id_[i], text_[i]))
    # insert_data_daytime(list_new)
    insert_data_daytime_append(list_new_append)