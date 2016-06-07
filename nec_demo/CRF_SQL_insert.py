__author__ = 'vdthoang'
from nec_demo.filterText_demo import table_SQL
from main.loadFile import load_file
from CRF_labeling.filterText_CRF import filter_eachToken
import MySQLdb
from time import time


def load_data_ID(command):
    if command == 'twitter':
        sql = 'select tweetID from tweet_2015 order by tweetID;'
    elif command == 'sgforums':
        sql = 'select id_str from sgforums_2015 order by post_id;'
    elif command == 'facebook':
        sql = 'select facebookID from facebook_2015 order by facebookID;'

    list_id = table_SQL(sql)
    return list_id


def load_text_CRF_label(path, name, command):
    list_file = load_file(path, name)
    list_text, list_label, list_svc = list(), list(), list()
    for i in range(0, len(list_file)):
        if i % 2 == 0:
            text = list_file[i]
            list_text.append(text)
        else:
            label = list_file[i]
            list_label.append(label)

    for i in range(0, len(list_text)):
        svc, split_text, split_label = '', list_text[i].split(), list_label[i].split()
        for j in range(0, len(split_text)):
            token_label = split_label[j]
            # get the token for bus services
            if token_label == '1':
                token_text = filter_eachToken(split_text[j], command)
                svc += token_text + ' '

        if len(svc) != 0:
            list_svc.append(svc.strip())
        else:
            list_svc.append('None')

    list_all = list()
    list_all.append(list_text), list_all.append(list_label), list_all.append(list_svc)
    return list_all


def insert_SQL_demo(list_id, list_text, list_predLabel, list_svc, command):
    # load data to server
    db = MySQLdb.connect(host="10.0.106.71",  # your host, usually localhost
                     user="vdthoang",  # your username
                      passwd="LARCuser1142",  # your password
                      db="nec_demo")  # name of the data base
    cur = db.cursor()

    if command == 'twitter':
        table_name = 'tweet_2015_Entity'
        create_table = "CREATE TABLE " + table_name \
            + "(tweetID VARCHAR(200) NULL COMMENT '', tweetText TEXT NULL COMMENT '', " \
            + "CRF TEXT NULL COMMENT '', bussvc TEXT NULL COMMENT '');"
        print create_table
        cur.execute(create_table)

        list_error, cnt, t0 = list(), 0, time()
        for i in range(0, len(list_id)):
            cnt += 1
            tweetID, tweetText, CRF, bussvc = list_id[i], list_text[i], list_predLabel[i], list_svc[i]
            sql = """INSERT INTO """ + table_name + "(tweetID, tweetText, CRF, bussvc) VALUES ('""" \
                  + tweetID + "','" + tweetText.replace('\'', '\'\'').replace('\\', '\\\\') + "','" + CRF + "','" \
                  + str(bussvc) + "')"
            # print sql

            try:
                cur.execute(sql)
                db.commit()
            except ():
                print (tweetID + '\t' + sql)
                list_error.append(tweetID + '\t' + sql)

            if cnt % 1000 == 0:
                print 'Processing ' + str(cnt) + ' records take ' + str(time() - t0)
            for value in list_error:
                print value

    elif command == 'sgforums':
        table_name = 'sgforums_2015_Entity'
        create_table = "CREATE TABLE " + table_name \
            + "(id_str VARCHAR(100) NULL COMMENT '', summary TEXT NULL COMMENT '', " \
            + "CRF TEXT NULL COMMENT '', bussvc TEXT NULL COMMENT '');"
        print create_table
        cur.execute(create_table)

        list_error, cnt, t0 = list(), 0, time()
        for i in range(0, len(list_id)):
            cnt += 1
            post_id, summary, CRF, bussvc = list_id[i], list_text[i], list_predLabel[i], list_svc[i]
            sql = """INSERT INTO """ + table_name + "(id_str, summary, CRF, bussvc) VALUES ('" \
                  + str(post_id) + "','" + summary.replace('\'', '\'\'').replace('\\', '\\\\') + "','" + CRF + "','" \
                  + bussvc + "')"
            # print sql

            try:
                cur.execute(sql)
                db.commit()
            except ():
                print (str(post_id) + '\t' + sql)
                list_error.append(str(post_id) + '\t' + sql)

            if cnt % 1000 == 0:
                print 'Processing ' + str(cnt) + ' records take ' + str(time() - t0)
            for value in list_error:
                print value

    elif command == 'facebook':
        table_name = 'facebook_2015_Entity'
        create_table = "CREATE TABLE " + table_name \
            + "(facebookID VARCHAR(200) NULL COMMENT '', post TEXT NULL COMMENT '', " \
            + "CRF TEXT NULL COMMENT '', bussvc TEXT NULL COMMENT '');"
        print create_table
        cur.execute(create_table)

        list_error, cnt, t0 = list(), 0, time()
        for i in range(0, len(list_id)):
            cnt += 1
            post_id, summary, CRF, bussvc = list_id[i], list_text[i], list_predLabel[i], list_svc[i]
            sql = """INSERT INTO """ + table_name + "(facebookID, post, CRF, bussvc) VALUES ('" \
                  + str(post_id) + "','" + summary.replace('\'', '\'\'').replace('\\', '\\\\') + "','" + CRF + "','" \
                  + bussvc + "')"
            # print sql

            try:
                cur.execute(sql)
                db.commit()
            except ():
                print (str(post_id) + '\t' + sql)
                list_error.append(str(post_id) + '\t' + sql)

            if cnt % 1000 == 0:
                print 'Processing ' + str(cnt) + ' records take ' + str(time() - t0)
            for value in list_error:
                print value

    print ('Done process')
    db.close()


if __name__ == '__main__':
    # Using to put the data from CRF
    # TWITTER
    # path = 'D:\Project\Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/twitter'
    # name = 'original_pred_label_twitter.csv'
    # command = 'twitter'

    # SGFORUMS
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/sgforums'
    # name = 'original_pred_label_sgforums.csv'
    # command = 'sgforums'

    # FACEBOOK
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/facebook'
    name = 'original_pred_label_facebook.csv'
    command = 'facebook'

    list_id = load_data_ID(command)
    list_all = load_text_CRF_label(path, name, command)
    list_text, list_label, list_svc = list_all[0], list_all[1], list_all[2]
    insert_SQL_demo(list_id, list_text, list_label, list_svc, command)
