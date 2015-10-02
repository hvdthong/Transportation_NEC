'''
Created on 27 Jul 2015

@author: vdthoang
'''
import requests
from bs4 import BeautifulSoup
import string

def trade_street(url, pattern):
    source_code = requests.get(url)
    plain_text = source_code.text
    
    #soup = BeautifulSoup(plain_text.encode('utf-8'),"html5lib")
    soup = BeautifulSoup(plain_text,"html5lib")
    
    list_street = []
    count = 0      
    #for tag in soup.findAll('a', {'name':'namesearch'}):
    for tag in soup.findAll('a'):
        href = tag.get('href')
        
        if (pattern in href) & (len(href) > len(pattern) + 2):            
            title = tag.string
            list_street.append(title)
#             print (href)
#             print (title)
#             print (url)
        count += 1
    
    print (url)
    return list_street
if __name__ == '__main__':
    ## crawler all the roads in Singapore
    
    web = 'http://www.nearby.sg/streetnames'    
    pattern = '/streetnames/'    

    list_page = []
    for each in string.ascii_lowercase:
        list_page.append(each)
    
    list_streets = []
    for page in list_page:
        url = web + '/' + page
        streets = trade_street(url, pattern) 
        list_streets = list_streets + streets
    
    for street in list_streets:
        print (street)
    print (len(list_streets))