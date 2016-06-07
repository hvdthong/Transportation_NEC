__author__ = 'vdthoang'
import json
import urllib
from urlparse import urlparse
import httplib2 as http # external library
from main.loadFile import load_file
from main.writeFile import write_file
from datetime import datetime


def load_busstop(busstop):
    code = list()
    for stop in busstop:
        split_stop = stop.split('\t')
        if split_stop[0] not in code:
            code.append(split_stop[0])
    return code


if __name__=="__main__":
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name = 'busstop_mytransport.csv'
    busstop_code = load_busstop(load_file(path, name))

    # Authentication parameters
    headers = {'AccountKey': 'ans3d09N6bEgJ7SCHKJzLg==',
               'UniqueUserID': '032108eb-3c63-4c3c-b5c4-dc3c3ba27294',
               'accept': 'application/json'}  # Request results in JSON

    path_write = path + '/busarrivalTime'
    write_ = list()
    cnt = 0
    while True:
        cnt += 1
        for i in range(0, len(busstop_code)):
            stop = busstop_code[i]
            stop = '31009'
            time_ = str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
            # API parameters
            url = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrival?'  # Resource URL
            params = {'BusStopID': stop, 'SST': True}

            # Build query string & specify type of API call
            target = urlparse(url + urllib.urlencode(params))
            # print target.geturl()
            method = 'GET'
            body = ''

            # Get handle to http
            h = http.Http()
            # Obtain results
            response, content = h.request(
                target.geturl(),
                method,
                body,
                headers)
            # Parse JSON to print
            jsonObj = json.loads(content)
            print jsonObj
            # print time_ + '\t' + str(jsonObj)
            # write_.append(time_ + '\t' + str(jsonObj))
            print cnt, i
            quit()

        # if (cnt % 1) == 0:
        #     write_file(path_write,  'busarrivalTime_' + str(cnt), write_)
        #     write_ = list()