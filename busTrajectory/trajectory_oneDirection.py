__author__ = 'vdthoang'
import MySQLdb
from main.loadFile import load_file
from main.writeFile import write_file


def load_busstop(service, direction):
    # note that we load the data on server into text file
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                          passwd="ducthong",  # your password
                          db="lta_datamall")  # name of the data base

    # you must create a Cursor object. It will let
    # you execute all the queries you need
    cur = db.cursor()
    busstop_direct = list()
    if direction == 1:
        query = 'select * from bus_service_stop_direct_one where busNo = ' + str(service)
    print query
    cur.execute(query)  # call the database which name 'posts'
    for row in cur.fetchall():
        busstop_direct.append(row[1])

    db.close()
    return busstop_direct


def convert_traj(path, name):
    traj = load_file(path, name)
    convert = list()
    for i in xrange(1, len(traj)):
        split_i = traj[i].split()
        # print i - 1, split_i[0], split_i[1], -1
        convert.append(str(i - 1) + ' ' + split_i[0] + ' ' + split_i[1] + ' ' + str(-1))
    convert.append(str(-1))
    return convert


def info_trajs(trajs):
    downloadID, stops, lat, lng = list(), list(), list(), list()
    for i in xrange(0, len(trajs)):
        split_ = trajs[i].split()
        downloadID.append(split_[0]), stops.append(int(split_[1])), lat.append(split_[2]), lng.append(split_[3])
    return downloadID, stops, lat, lng

def get_traj(busstop, trajs):
    downloadID, stops, lat, lng = info_trajs(trajs)

    traj = list()
    list_time = list()
    i = 0
    for k in xrange(1, len(busstop)):
        b = busstop[k]
        for i in xrange(i, len(stops)):
            if int(b) == int(stops[i]):
                time = downloadID[i]
                if time not in list_time:
                    time, lat_traj, lng_traj = downloadID[i], lat[i], lng[i]
                    # print time, stops[i], lat_traj, lng_traj
                    print time, lat_traj, lng_traj, -1
                    list_time.append(time)
                    break



if __name__ == '__main__':
    # path = 'D:/Project/Bus Trajectory'
    # name = '141_lat_lng_direct_one.csv'
    # converts = convert_traj(path, name)
    # write_file(path, name.replace('.csv', '') + '_convert', converts)

    path = 'D:/Project/Bus Trajectory'
    name = '141_lat_lng_direct_one_all.csv'
    trajs = load_file(path, name)

    service = 141
    direction = 1
    busstop = load_busstop(service, direction)

    print len(trajs), len(busstop)
    get_traj(busstop, trajs)