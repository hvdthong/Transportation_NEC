__author__ = 'vdthoang'
from urlparse import urlparse
import httplib2 as http  # external library
import urllib
import json


if __name__ == '__main__':
    headers = {'AccountKey': 'ans3d09N6bEgJ7SCHKJzLg==',
               'UniqueUserID': '032108eb-3c63-4c3c-b5c4-dc3c3ba27294',
               'accept': 'application/json'}  # Request results in JSON

    url = 'http://datamall2.mytransport.sg/ltaodataservice/BusRoutes?' # $skip=' + str(i)  # Resource URL
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

    # for i in range(0, 650, 50):
    #     # API parameters
    #     url = 'http://datamall2.mytransport.sg/ltaodataservice/BusRoutes?$skip=' + str(i)  # Resource URL
    #     params = {}
    #
    #     # Build query string & specify type of API call
    #     target = urlparse(url + urllib.urlencode(params))
    #     # print target.geturl()
    #     method = 'GET'
    #     body = ''
    #
    #     # Get handle to http
    #     h = http.Http()
    #     # Obtain results
    #     response, content = h.request(
    #         target.geturl(),
    #         method,
    #         body,
    #         headers)
    #     # Parse JSON to print
    #     jsonObj = json.loads(content)
    #     value = jsonObj['value']
    #     print jsonObj
