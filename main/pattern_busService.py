'''
Created on 21 Jul 2015

@author: vdthoang
'''
import re

from main.loadFile import load_file
from main.writeFile import write_file


def pattern_bus_service(string, list_bus_services):
    # detect if bus service in token on string or not, if yes => take it
    # note that we don't need to know if the post has to be in the list checkBusServices or not
    pattern_1 = r'[s][v][0-9]+\b'
    pattern_2 = r'[s][v][0-9]+[A-z]{1}\b'
    pattern_3 = r'[s][v][c][0-9]+[A-z]{1}\b'
    
    split_string = string.strip().split()
    list_service = []
    for token in split_string:
        # if (re.match(pattern_1, token)) or (re.match(pattern_2, token)):
        #     token = token[2:]
        #     if (token.lower() in list_bus_services):
        #         list_service.append(token)
        # elif (re.match(pattern_3, token)):
        #     token = token[3:]
        #     if (token.lower() in list_bus_services):
        #         list_service.append(token)
        #
        # elif (len(token) >= 3 and token.lower() in list_bus_services):
        #     list_service.append(token)

        # using for only testing classification for regular expression
        if (len(token) >= 3 and token.lower() in list_bus_services):
            list_service.append(token)

    return list_service

def match_bus_service(string, list_bus_services):
    #extract all the bus services number if the token contain in list_bus_services
    #note that the post has to be in the list checkBusServices
    split_string = string.strip().split()
    list_service = []
    for token in split_string:
        if (token.upper() in list_bus_services):
                list_service.append(token)
    return list_service

def pattern_services(path, name, list_bus_services, list_posts_checkBusServices):
    list_write = []
    with open(path + '/' + name) as f:        
        for line in f:
            split_line = line.split('\t')
            if (name == 'posts_filter_v2.csv'):
                list_pattern_services = pattern_bus_service(split_line[1], list_bus_services)
                list_match_services = []
                if (split_line[0] in list_posts_checkBusServices):
                    list_match_services = match_bus_service(split_line[1], list_bus_services)
            else:
                list_pattern_services = pattern_bus_service(split_line[2], list_bus_services)
                list_match_services = []
                if (split_line[1] in list_posts_checkBusServices):
                    list_match_services = match_bus_service(split_line[2], list_bus_services)
                
            list_total = list(set(list_pattern_services) | set(list_match_services))
            
            #print (split_line[1] + '\t' + str(len(list_total)))
            
            if (len(list_total) != 0):
                for each in list_total:
                    if (name == 'posts_filter_v2.csv'):
                        print (split_line[0] + '\t' + each)
                        list_write.append(split_line[0] + '\t' + each)
                    else:
                        print (split_line[1] + '\t' + each)
                        list_write.append(split_line[1] + '\t' + each)
                    
    write_file(path, 'posts_busService', list_write)
    return list_write

###########################################################################################################
###########################################################################################################
def check_bus_service(token, list_bus_services):
    if (token in list_bus_services):
        return 1 ## this is a bus services
    else:
        return 0 ## it's not a bus service

def pattern_bus_service_ver2(string, list_bus_services):
    # detect if the string contains some sentences like: 'bus 12, 24...'
    # list_word = ['bus', 'buses', 'service', 'services', 'no', 'svc' , 'sv', 'sv.']  # twitter
    list_word = ['service', 'services', 'no', 'svc', 'sv', 'sv.']  # sgforums
    new_string = string.replace('and', '').replace('or', '')  # in case string = 'bus 12 and/or 24'

    split_string = new_string.strip().split()
    list_service = []
    for index in range(0, len(split_string)):
        token = split_string[index]

        if (token in list_word):
            while True:
                if (index < len(split_string) - 1):
                    index += 1
                    if check_bus_service(split_string[index], list_bus_services) == 0:
                        break
                    elif check_bus_service(split_string[index], list_bus_services) == 1:
                        list_service.append(split_string[index])
                else:
                    break
    return list_service

def pattern_services_ver2(path, name, list_bus_services):
    list_write = []

    with open(path + '/' + name) as f:
        for line in f:

            split_line = line.split('\t')
            text = split_line[1].lower()

            list_pattern_services = pattern_bus_service_ver2(text, list_bus_services)
            list_match_services = pattern_bus_service(text, list_bus_services)

            list_total = list(set(list_pattern_services) | set(list_match_services))

            # print (split_line[1] + '\t' + str(len(list_total)))

            if (len(list_total) != 0):
                for each in list_total:
                    print (split_line[0] + '\t' + each)
                    list_write.append(split_line[0] + '\t' + each)

    # write_file(path, 'tweet_2015_filtering_busServices', list_write)
    # write_file(path, 'facebook_2015_filtering_busServices', list_write)
    # write_file(path, 'facebook_2015_BusNews_filtering_busServices', list_write)
    # write_file(path, 'posts_busService_ver2', list_write)

    print len(list_write)
    return list_write

###########################################################################################
###########################################################################################

###########################################################################################
###########################################################################################
def pattern_label_bussvc(string, list_bus_services):
    split_string = string.strip().split()
    list_service = []
    for token in split_string:
        if (len(token) >= 3 and token.lower() in list_bus_services):
            list_service.append(token)
    return list_service

def extract_busSvc_labeling(path, name):
    list_write = []

    with open(path + '/' + name) as f:
        for line in f:
            split_line = line.split('\t')
            text = split_line[1].lower()

            list_pattern_services = pattern_bus_service_ver2(text, list_bus_services)
            list_match_services = pattern_label_bussvc(text, list_bus_services)

            list_total = list(set(list_pattern_services) | set(list_match_services))

            #print (split_line[1] + '\t' + str(len(list_total)))

            if (len(list_total) != 0):
                for each in list_total:
                    print (split_line[0] + '\t' + each)
                    list_write.append(split_line[0] + '\t' + each)

    for value in list_write:
        print value

if __name__ == '__main__':
    #===========================================================================
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20150714'
    # 
    # #load bus services number
    # name_bus_services = 'bus_services.csv'
    # list_bus_services = load_file(path, name_bus_services)
    # list_bus_services = [item.upper() for item in list_bus_services]
    # 
    # #load posts_checkBusServices
    # name_posts_checkBusServices = 'posts_filter_1279_checkBusServices.csv'
    # list_posts_checkBusServices = load_file(path, name_posts_checkBusServices)
    # 
    # #call the main function
    # name_post = 'posts_filter_1279_v2.csv'
    # pattern_services(path, name_post, list_bus_services, list_posts_checkBusServices)
    #===========================================================================
    
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts'

    #load bus services number
    name_bus_services = 'bus_services.csv'
    list_bus_services = load_file(path, name_bus_services)
    list_bus_services = [item.lower() for item in list_bus_services]


    # #load posts_checkBusServices
    # name_posts_checkBusServices = 'posts_filter_checkBusServices.csv'
    # list_posts_checkBusServices = load_file(path, name_posts_checkBusServices)
    #
    # #call the main function
    # name_post = 'posts_filter_v2.csv'
    # pattern_services(path, name_post, list_bus_services, list_posts_checkBusServices)

    #===========================================================================
    #===========================================================================
    ## Remember to change the name to write file

    ## Extract bus service from Twitter
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter'
    # name = 'tweet_2015_filtering.csv'
    # pattern_services_ver2(path, name, list_bus_services)

    # Extract bus service from Facebook
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook'
    # name = 'sg_fb_biz_feed_filtering.csv'
    # pattern_services_ver2(path, name, list_bus_services)

    # Extract bus service from Facebook Bus News
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    # name = 'sg_fb_biz_feed_BusNews_filtering.csv'
    # pattern_services_ver2(path, name, list_bus_services)
    #===========================================================================
    #===========================================================================

    ## Extract bus services from sgforums
    # path_deploy = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    # name_deploy = 'Deployments.csv'
    #
    # list_deploy = load_file(path_deploy, name_deploy)
    # list_deploy = [item.lower() for item in list_deploy]
    # for value in list_deploy:
    #     print value

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts'
    # name = 'posts_filter.csv'
    # pattern_services_ver2(path, name, list_bus_services)
    # pattern_services_ver2(path, name, list_bus_services)
    # pattern_services_sgforum(path, name, list_bus_services)
    #===========================================================================
    #===========================================================================

    ## Extract bus service using pattern service, compare to labeling data
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling'
    # name = 'sgforum_text_labeling.csv'
    # extract_busSvc_labeling(path, name)
