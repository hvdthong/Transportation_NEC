__author__ = 'vdthoang'
import json
import urllib
from urlparse import urlparse
import httplib2 as http #External library
from main.writeFile import write_file


def top_retrieve_busstop(total):
    skip = list()
    for i in range(0, total, 50):
        if i == 0:
            skip.append('')
        else:
            skip.append('?$skip=' + str(i))
    return skip


if __name__ == '__main__':
    skips = top_retrieve_busstop(5300)
    headers = {'AccountKey': 'ans3d09N6bEgJ7SCHKJzLg==',
               'UniqueUserID': '032108eb-3c63-4c3c-b5c4-dc3c3ba27294',
               'accept': 'application/json'}  # Request results in JSON

    busstop_desc = list()

    for skip in skips:
        url = 'http://datamall2.mytransport.sg/ltaodataservice/BusStops' + skip  # Resource URL
        # url = 'http://datamall2.mytransport.sg/ltaodataservice/TaxiAvailability'
        # # Build query string & specify type of API call
        params = {}
        target = urlparse(url + urllib.urlencode(params))
        print target.geturl()
        method = 'GET'
        body = ''
        # # Get handle to http
        h = http.Http()
        # Obtain results
        response, content = h.request(
            target.geturl(),
            method,
            body,
            headers)
        # Parse JSON to print
        jsonObj = json.loads(content)
        value = jsonObj['value']
        print len(value)
        for each in value:
            print each['BusStopCode'], each['RoadName'], each['Description'], each['Latitude'], each['Longitude']
            busstop_desc.append(each['BusStopCode'] + '\t' + each['RoadName'] + '\t' + each['Description'] \
                                 + '\t' + str(each['Latitude']) + '\t' + str(each['Longitude']))

    print len(busstop_desc)

    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name = 'busstop_mytransport_lat_long'
    write_file(path, name, busstop_desc)

