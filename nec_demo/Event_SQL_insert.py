__author__ = 'vdthoang'
from nec_demo.CRF_SQL_insert import load_data_ID
from main.loadFile import load_file
import MySQLdb
from time import time


def insert_events_SQL(list_id, list_events, command):
    db = MySQLdb.connect(host="10.0.106.71",  # your host, usually localhost
                     user="vdthoang",  # your username
                      passwd="LARCuser1142",  # your password
                      db="nec_demo")  # name of the data base
    cur = db.cursor()

    if command == 'twitter':
        table_name = 'tweet_2015_Aug_Oct_Events'
        create_table = "CREATE TABLE " + table_name \
            + "(tweetID VARCHAR(200) NULL COMMENT '', wait INT NULL COMMENT '', missing INT NULL COMMENT '', " \
            + "skip INT NULL COMMENT '', slow INT NULL COMMENT '', " \
            + "accident INT NULL COMMENT '', crowd INT NULL COMMENT '');"
        print create_table
        cur.execute(create_table)

        wait, missing, skip = list_events[0], list_events[1], list_events[2]
        slow, accident, crowd = list_events[3], list_events[4], list_events[5]
        list_error, cnt, t0 = list(), 0, time()
        for i in range(0, len(list_id)):
            cnt += 1
            id, wait_row, missing_row, skip_row = list_id[i], wait[i], missing[i], skip[i]
            slow_row, accident_row, crowd_row = slow[i], accident[i], crowd[i]

            sql = """INSERT INTO """ + table_name + "(tweetID, wait, missing, skip, slow, accident, crowd) VALUES ('""" \
                  + id + "'," + wait_row + "," + missing_row + "," + skip_row + "," + slow_row + "," + accident_row \
                  + "," + crowd_row + ');'
            # print sql

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

    print ('Done process')
    db.close()

if __name__ == '__main__':
    #########################################################################################################
    # TWITTER
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/twitter/events_pred'
    events = ['wait', 'missing', 'skip', 'slow', 'accident', 'crowd']
    command = 'twitter'
    list_id = load_data_ID(command)
    all_events = list()
    for event in events:
        list_event = load_file(path, event + '.csv')
        all_events.append(list_event)

    print len(list_id), len(all_events)
    insert_events_SQL(list_id, all_events, command)
