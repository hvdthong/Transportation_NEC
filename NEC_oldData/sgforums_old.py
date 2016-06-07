__author__ = 'vdthoang'
import MySQLdb


def sgforums_old():
    db = MySQLdb.connect(host="10.0.106.71",  # your host, usually localhost
                         user="vdthoang",  # your username
                          passwd="LARCuser1142",  # your password
                          db="sgforums")  # name of the data base

    # you must create a Cursor object. It will let
    # you execute all the queries you need
    cur = db.cursor()
    query = "select * from posts where published_date >= '2015-01-01 00:00:00' " + \
            "and published_date < '2016-03-31 23:59:59' " + \
            "and forum_id = 1279 order by published_date desc;"
    cur.execute(query)
    listText = list()
    for row in cur.fetchall():
        print str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3]) + '\t' + str(row[4]) \
              + '\t' + str(row[5]) + '\t' + str(row[6]) + '\t' + str(row[7]) + '\t' + str(row[8]) + '\t' \
              + str(row[9]) + '\t' + str(row[10])
        listText.append(str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3]) + '\t' \
              + str(row[4]) + '\t' + str(row[5]) + '\t' + str(row[6]) + '\t' + str(row[7]) + '\t' + str(row[8]) \
              + '\t' + str(row[9]) + '\t' + str(row[10]))
    db.close()
    return listText


def insert_data(list_):
    db = MySQLdb.connect(host="10.4.8.139",  # your host, usually localhost
                         user="bussense",  # your username
                          passwd="Bussense2016!",  # your password
                          db="bussense_archive")  # name of the data base
    cur = db.cursor()
    list_insert = list()
    for value in list_:
        split_value = value.split('\t')
        forum_id, topic_id, post_id, id_str = split_value[0], split_value[1], split_value[2], split_value[3]
        link, title, author, publish_date = split_value[4], split_value[5], split_value[6], split_value[7]
        summary, update_date, collection_date = split_value[8], split_value[9], split_value[10]

        update_date = None

        list_insert.append((forum_id, topic_id, post_id, id_str, link, title, author, publish_date, summary
                            , update_date, collection_date))

    sql = "INSERT INTO sgforums(forum_id, topic_id, post_id, id_str, link, title, author" \
          ", published_date, summary, updated_date, collection_date) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    print sql
    cur.executemany(sql, list_insert)
    db.commit()
    db.close()
    print 'Finish insert data to sql'

if __name__ == '__main__':
    list_ = sgforums_old()
    insert_data(list_)
