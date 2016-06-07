__author__ = 'vdthoang'
import json
import time
import MySQLdb
from datetime import datetime, timedelta


def realTime_busstop(path, file):
    with open(path + '/' + file) as data_file:
        data = json.load(data_file)

    cnt = 0
    list_insert = list()
    for element in data:
        if len(element['Services']) == 0:
            pass
        else:
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(element['timestamp'])))
            # print cnt, element['downloadID'], element['BusStopID'], date
            cnt += 1
            list_insert.append((element['downloadID'], element['BusStopID'], date))
    return list_insert


def insert_BusRealTime(list_insert):
    # note that we load the data on server into text file
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                         passwd="ducthong",  # your password
                         db="2015_allschemas")  # name of the data base

    cur = db.cursor()
    create_table = "CREATE TABLE IF NOT EXISTS busstop_mytransport_realTime " \
                + "(downloadID INT NULL, BusStopID VARCHAR(20) NULL COMMENT ''" \
                + ", dateTime timestamp NULL COMMENT '');"
    print create_table
    cur.execute(create_table)
    sql = "INSERT INTO busstop_mytransport_realTime(downloadID, BusStopID, dateTime) VALUE(%s, %s, %s);"
    print sql
    cur.executemany(sql, list_insert)
    db.commit()


def busStopTransport_id():
    # note that we load the data on server into text file
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                         passwd="ducthong",  # your password
                         db="2015_allschemas")  # name of the data base

    cur = db.cursor()
    sql = 'select distinct BusStopID from busstop_mytransport_realtime order by BusStopID;'
    cur.execute(sql)
    stops = list()
    for row in cur:
        stops.append(row[0])
    cur.close()
    db.close()
    print len(stops)
    return stops


##################################################################################################################
##################################################################################################################
def get_Time(date_Time):
    str_split = str(date_Time).split(' ')
    return str_split[1]


def first_last(dates):
    earTime, laTime = get_Time(dates[0]), get_Time(dates[len(dates) - 1])
    return earTime, laTime


def check_duration(dateList):
    date_fmt = '%Y-%m-%d %H:%M:%S'
    earTime, laTime = '', ''
    max_Time = ''
    for i in range(0, len(dateList) - 1):
        date_one, date_two = str(dateList[i]), str(dateList[i + 1])
        tdelta = datetime.strptime(date_two, date_fmt) - datetime.strptime(date_one, date_fmt)
        if i == 0:
            max_Time, earTime, laTime = tdelta, get_Time(date_two), get_Time(date_one)
            # print busstop, max_Time, earTime, laTime
        else:
            if tdelta >= max_Time:
                max_Time, earTime, laTime = tdelta, get_Time(date_two), get_Time(date_one)
    return earTime, laTime


def early_latest_busArr(busstop, delay_mins):
    # note that we load the data on server into text file
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                         passwd="ducthong",  # your password
                         db="2015_allschemas")  # name of the data base

    cur = db.cursor()
    sql = "select dateTime from busstop_mytransport_realtime where BusStopID = '" + busstop + "' order by dateTime;"
    cur.execute(sql)
    dateList = list()
    for row in cur:
        dateList.append(row[0])
    cur.close()
    db.close()

    first_element = dateList[0]
    time_fmt = '%H:%M:%S'
    firstTime = datetime.strptime('00:00:00', time_fmt)
    secondTime = datetime.strptime('05:00:00', time_fmt)
    elementTime = datetime.strptime(get_Time(first_element), time_fmt)

    if (firstTime <= elementTime) and (elementTime <= secondTime):
        earTime, laTime = check_duration(dateList)
    else:
        earTime, laTime = first_last(dateList)


    # date_fmt = '%Y-%m-%d %H:%M:%S'
    # earTime, laTime = '', ''
    # max_Time = ''
    # for i in range(0, len(dateList) - 1):
    #     date_one, date_two = str(dateList[i]), str(dateList[i + 1])
    #     tdelta = datetime.strptime(date_two, date_fmt) - datetime.strptime(date_one, date_fmt)
    #     if i == 0:
    #         max_Time, earTime, laTime = tdelta, get_Time(date_two), get_Time(date_one)
    #         # print busstop, max_Time, earTime, laTime
    #     else:
    #         if tdelta >= max_Time:
    #             max_Time, earTime, laTime = tdelta, get_Time(date_two), get_Time(date_one)
    #             # print busstop, max_Time, earTime, laTime
    #
    # # print '-----Earliest and latest time'
    # # print busstop, earTime, laTime
    # time_fmt = '%H:%M:%S'
    # earTime = datetime.strptime(earTime, time_fmt) - timedelta(minutes=delay_mins)
    # laTime = datetime.strptime(laTime, time_fmt) + timedelta(minutes=delay_mins)
    # return busstop + '\t' + get_Time(earTime) + '\t' + get_Time(laTime)

    return busstop + '\t' + earTime + '\t' + laTime


if __name__ == '__main__':
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/mytransport/elasticSearch_busArri'
    # files = list()
    # # files.append('datamall_bus_arrival_2016_0.json')
    # files.append('datamall_bus_arrival_2016_1.json')
    # files.append('datamall_bus_arrival_2016_2.json')
    # files.append('datamall_bus_arrival_2016_3.json')
    # files.append('datamall_bus_arrival_2016_4.json')
    # files.append('datamall_bus_arrival_2016_5.json')
    # files.append('datamall_bus_arrival_2016_6.json')
    # files.append('datamall_bus_arrival_2016_7.json')
    # files.append('datamall_bus_arrival_2016_8.json')
    #
    # for f_ in files:
    #     list_ = realTime_busstop(path, f_)
    #     insert_BusRealTime(list_)

    stops = busStopTransport_id()
    delay_mins = 15
    for s in stops:
        print early_latest_busArr(s, delay_mins)
