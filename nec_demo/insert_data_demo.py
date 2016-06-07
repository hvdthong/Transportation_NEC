__author__ = 'vdthoang'
from main.loadFile import load_file
import MySQLdb
from time import time


def insert_to_server(list_data, command):
    db = MySQLdb.connect(host="10.0.106.71",  # your host, usually localhost
                     user="vdthoang",  # your username
                      passwd="LARCuser1142",  # your password
                      db="nec_demo")  # name of the data base
    cur = db.cursor()

    if command == 'sgforums':
        table_name = 'sgforums_2015_Aug_Oct'
        create_table = "CREATE TABLE " + table_name \
            + "(forum_id INT NULL COMMENT '', topic_id INT NULL COMMENT '', post_id INT NULL COMMENT '', " \
            + "id_str VARCHAR(100) NULL COMMENT '', link VARCHAR(255) NULL COMMENT '', " \
            + "title VARCHAR(255) NULL COMMENT '', author VARCHAR(255) NULL COMMENT '', " \
            + "published_date DATETIME NULL COMMENT '', summary TEXT NULL COMMENT '', " \
            + "updated_date DATETIME NULL COMMENT '', collection_date DATETIME NULL COMMENT '');"

        print create_table
        cur.execute(create_table)

        list_error, cnt, t0 = list(), 0, time()
        for line in list_data:
            cnt += 1
            split_line = line.split('\t')

            forum_id, topic_id, post_id, id_str = split_line[0], split_line[1], split_line[2], split_line[3]
            link, title, author, published_date = split_line[4], split_line[5], split_line[6], split_line[7]
            summary, updated_date, collection_date = split_line[8], split_line[9], split_line[10]

            sql = """INSERT INTO """ + table_name + "(forum_id, topic_id, post_id, id_str, link, title, author, published_date, summary, updated_date, collection_date) " \
                  + "VALUES ('""" + forum_id + "'," + topic_id + "," + post_id \
                  + ",'" + id_str + "','" + link + "','" + title.replace('\'', '\'\'').replace('\\', '\\\\') \
                  + "','" + author + "','" + published_date + "','" \
                  + summary.replace('\'', '\'\'').replace('\\', '\\\\') + "','" \
                  + updated_date + "','" + collection_date + "');"

            try:
                cur.execute(sql)
                db.commit()
            except ():
                print (id + '\t' + sql)
                list_error.append(id + '\t' + sql)

            if cnt % 1000 == 0:
                print 'Processing ' + str(cnt) + ' records take ' + str(time() - t0)

            for value in list_error:
                print value

    print 'Done process'
    db.close()


if __name__ == '__main__':
    ####################################################################
    # TWITTER: with the twitter data, we refer to the file 'event_extract\json_filter.py'
    # FACEBOOK: with the twitter data, we refer to the file 'event_extract\json_filter.py'

    ####################################################################
    # This file only use for sgforums
    # Sgforums: insert sgforums to database
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/sgforums'
    name = 'sgforums_2015_Aug_Oct.csv'
    command = 'sgforums'

    list_data = load_file(path, name)
    insert_to_server(list_data, command)

