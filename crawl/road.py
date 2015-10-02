'''
Created on 27 Jul 2015

@author: vdthoang
'''
from types import NoneType

import requests
from bs4 import BeautifulSoup

from main.writeFile import write_file
from main.loadFile import load_file


def trade_bus_road(url, service):
        
    source_code = requests.get(url)
    plain_text = source_code.text
    
    soup = BeautifulSoup(plain_text,"html5lib")    
    list_street = []
    count = 0
    
    for tag in soup.findAll('td'):
        if ('<td class="subhead2 route">' in str(tag)):
            if (type(tag.string) != NoneType):
                list_street.append(service + '\t' + 'subhead2' + '\t' + tag.string)
                print (service + '\t' + 'subhead2' + '\t' + str(tag.string))
        else:
            if (('class="route"' in str(tag)) & ('Road / Bus Stop Description' not in str(tag))):            
                if (type(tag.string) != NoneType):
                    list_street.append(service + '\t' + 'route' + '\t' + str(tag.string.replace(u'\xa0\u2022\xa0', '')))
                    print (service + '\t' + 'route' + '\t' + tag.string.replace(u'\xa0\u2022\xa0', ''))
                                
        count += 1
            
    return list_street

if __name__ == '__main__':
    ## cralwer all the road name of each bus stops  
    ## url = 'http://www.transitlink.com.sg/eservice/eguide/service_route.php?service='
    
    path_service = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name_service = 'bus_services.csv'
    list_all = load_file(path_service, name_service)
    list_services = []
    for index in range(1, len(list_all)):
        split_service = list_all[index].split('\t')
        list_services.append(split_service[0])
        
    print (list_services)
    
    list_all_streets = []
    url = 'http://www.transitlink.com.sg/eservice/eguide/service_route.php?service='
    for service in list_services:
        url_service = url + service
        print (url_service)
        list_all_streets = list_all_streets + trade_bus_road(url_service, service)
        
    write_file(path_service, 'bus_service_road', list_all_streets)