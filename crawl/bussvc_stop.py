__author__ = 'vdthoang'
from main.loadFile import load_file
from bs4 import BeautifulSoup
import requests
from main.writeFile import write_file


def is_Int_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def load_bussvc_direct(url, service, direct):
    source_code = requests.get(url)
    plain_text = source_code.text

    soup = BeautifulSoup(plain_text, "html5lib")
    list_bus_stop = list()
    if direct == 1:
        for tag in soup.findAll('td'):
            if 'DIRECTION 1' in str(tag):
                split_tag = tag.text.split()
                for each in split_tag:
                    if (len(each) == 5) and (is_Int_number(each) is True):
                        print str(service) + '\t' + each
                        list_bus_stop.append(str(service) + '\t' + each)
    elif direct == 2:
        for tag in soup.findAll('td'):
            if 'DIRECTION 2' in str(tag):
                split_tag = tag.text.split()
                for each in split_tag:
                    if (len(each) == 5) and (is_Int_number(each) is True):
                        print str(service) + '\t' + each
                        list_bus_stop.append(str(service) + '\t' + each)
    elif direct == 3:
        for tag in soup.findAll('td'):
            if 'LOOP SERVICE' in str(tag):
                split_tag = tag.text.split()
                for each in split_tag:
                    if (len(each) == 5) and (is_Int_number(each) is True):
                        print str(service) + '\t' + each
                        list_bus_stop.append(str(service) + '\t' + each)
    else:
        print 'You need to give correct direction'
        quit()
    return list_bus_stop


if __name__ == '__main__':
    path_service = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name_service = 'bus_services.csv'
    list_all = load_file(path_service, name_service)
    list_services = []
    for index in range(1, len(list_all)):
        split_service = list_all[index].split('\t')
        list_services.append(split_service[0])

    print (list_services)

    list_all_busstop = []
    url = 'http://www.transitlink.com.sg/eservice/eguide/service_route.php?service='
    for service in list_services:
        url_service = url + service
        print (url_service)
        # list_all_busstop += load_bussvc_direct(url_service, service, 1)
        # list_all_busstop += load_bussvc_direct(url_service, service, 2)
        list_all_busstop += load_bussvc_direct(url_service, service, 3)  # LOOP SERVICE
    # write_file(path_service, 'bus_service_stop_direct_one', list_all_busstop)
    # write_file(path_service, 'bus_service_stop_direct_two', list_all_busstop)
    write_file(path_service, 'bus_service_stop_direct_three', list_all_busstop)
