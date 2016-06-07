__author__ = 'vdthoang'
import json
import MySQLdb


def insert_bus_data(data):
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                          passwd="ducthong",  # your password
                          db="lta_datamall")  # name of the data base
    cur = db.cursor()
    table = "create table if not exists bus_info(busNo INT, busstopID INT, downloadID INT" \
            ", crawlTime int, estimatedArr datetime, lat float, lng float)"
    print table
    cur.execute(table)

    sql = "INSERT INTO bus_info(busNo, busstopID, downloadID, crawlTime, estimatedArr, lat, lng)" \
          " VALUE(%s,%s,%s,%s,%s,%s,%s);"
    print sql
    cur.executemany(sql, data)
    db.commit()
    db.close()


def extract_bus_lat_lon(path, name, svNo):
    with open(path + '/' + name) as data_file:
        data = json.load(data_file)

    bus_info = list()
    for bus in data:
        busstopID, downloadID, timestamp = bus['BusStopID'], bus['downloadID'], bus['timestamp']
        services = bus['Services']
        for sv in services:
            serviceNo = sv['ServiceNo']
            if serviceNo == str(svNo):
                nextBus = sv['NextBus']
                if bool(nextBus) is not False:
                    if nextBus.has_key('Location'):
                        location = nextBus['Location']
                        lat, lng = location['lat'], location['lng']
                        estimatedArr = nextBus['EstimatedArrival']
                        # print serviceNo, busstopID, downloadID, timestamp, estimatedArr, lat, lng
                        print lat, lng
                        bus_info.append((serviceNo, busstopID, downloadID, timestamp, estimatedArr.replace('T', ' ').replace('+08:00', ''), lat, lng))
                    break
    return bus_info


if __name__ == '__main__':
    path = 'D:\Project\Bus Trajectory'
    # name = 'datamall_bus_arrival_2016_v2_141_1463601600_1463687999.json'
    name = 'datamall_bus_arrival_2016_v2_141_1463688000_1463774399.json'
    svNo = 141
    bus_data = extract_bus_lat_lon(path, name, svNo)
    # insert_bus_data(bus_data)


