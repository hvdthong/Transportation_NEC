'''
Created on 16 Jul 2015

@author: vdthoang
'''
import re

from main.writeFile import write_file


def pattern_busPlate(string):
    #used to make the pattern of bus plate number of text
    #take all the tokens of string and detect the bus plate number 
    
    split_str = string.split()
    # print (string)
    
    list_busPlate = []
    for text in split_str:
        pattern = r'\b[A-z]{3}[0-9]+[A-z]{1}\b'

        if (re.match(pattern, text)):
            if (text not in list_busPlate):
                if ('(' in text):
                    index_ = text.index('(')
                    text = text[:index_]
                    
                    if text not in list_busPlate:
                        list_busPlate.append(text)
                else:
                    list_busPlate.append(text)
              
    # print (list_busPlate)
    
    return list_busPlate


def check_busPlate(string):
    #check if bus plate number is author name or not 
    string = string.replace('Originally posted by', '')
    split_str = string.split()
    new_string = ''
    for index in range(1, len(split_str)):
        new_string = new_string + ' ' + split_str[index]
    return new_string.strip()


def pattern_plate(path, name):
    list_write = []
    with open(path + '/' + name) as f:
        i = 0
        for line in f:
            if (i != 0):
                split_line = line.split('\t')
                list_busPlate = pattern_busPlate(check_busPlate(split_line[1]))
                if (len(list_busPlate) != 0):
                    for each in list_busPlate:
                        list_write.append(split_line[0] + '\t' + each)
                    
                    #print (split_line[0] + '\t' + str(len(pattern_busPlate(split_line[1]))))
            i += 1
            
    for value in list_write:
        print (value)
        
    # write_file(path, 'posts_busPlate', list_write)
    # write_file(path, 'posts_busPlate_v2', list_write)
    # write_file(path, 'tweet_2015_filtering_busPlate', list_write)
    # write_file(path, 'facebook_2015_filtering_busPlate', list_write)
    # write_file(path, 'facebook_2015_BusTransport_filtering_busPlate', list_write)
    write_file(path, 'facebook_2015_BusNews_filtering_busPlate', list_write)
        
    print (len(list_write))
    
if __name__ == '__main__':
    ###### REMEMBER TO CHANGE THE NAME OF WRITE_FILE

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20150714'
    # name = 'posts_filter.csv'

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts'
    # name = 'posts_filter.csv'

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter'
    # name = 'tweet_2015_filtering.csv'

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook'
    # name = 'sg_fb_biz_feed_filtering.csv'

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook'
    # name = 'sg_fb_biz_feed_BusTransport_filtering.csv'

    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    name = 'sg_fb_biz_feed_BusNews_filtering.csv'
    # pattern_plate(path, name)