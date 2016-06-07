__author__ = 'vdthoang'
from urlparse import urlparse
import httplib2 as http  # external library
import urllib
import json
from main.writeFile import write_file


if __name__ == '__main__':
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name = 'bussvc_mytransport'

    headers = {'AccountKey': 'ans3d09N6bEgJ7SCHKJzLg==',
               'UniqueUserID': '032108eb-3c63-4c3c-b5c4-dc3c3ba27294',
               'accept': 'application/json'}  # Request results in JSON
    list_svc = list()
    for i in range(0, 650, 50):
        # API parameters
        url = 'http://datamall2.mytransport.sg/ltaodataservice/BusServices?$skip=' + str(i)  # Resource URL
        params = {}

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
        value = jsonObj['value']
        print jsonObj
        for each in value:
            numSer, oriBusStop, desBusStop = each['ServiceNo'], each['OriginCode'], each['DestinationCode']
            print numSer, oriBusStop, desBusStop
            list_svc.append(numSer + '\t' + oriBusStop + '\t' + desBusStop)

    print 'List of bus services:'
    for i in list_svc:
        print i
    # write_file(path, name, list_svc)
