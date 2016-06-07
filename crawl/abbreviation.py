'''
Created on 28 Jul 2015

@author: vdthoang
'''
import re

from main.loadFile import load_file
from main.writeFile import write_file


def check_abb(path, name):
    list_ = load_file(path, name)
    
    list_check = []
    for each in list_:
        split = each.split('\t')
        
        if (len(split) not in list_check):
            list_check.append(len(split))
    print (list_check)
    
def load_abb(path, name):
    list_ = load_file(path, name)
    list_all = []
    list_abb = []
    list_word = []
    
    for each in list_:
        split = each.split('\t')
        list_abb.append(split[0])
        list_word.append(split[1])
#         print (split[0] + '\t' + split[1])
    list_all.append(list_abb)
    list_all.append(list_word)
    return list_all


def pattern_match(word, string):
    pattern_1 = r'.* ' + word + '\\b'
    pattern_2 = r'\b' + word + '\\b'
    
    if (re.match(pattern_1, string) or re.match(pattern_2, string)):
        return True
    else:
        return False

def road_abb(path, name, list_all):
    list_road = load_file(path, name)
    
    list_abb = list_all[0]
    list_word = list_all[1]
    
#     for abb in list_all:
#         for road in list_road:
#             if (pattern_match(abb, road) == True):
#                 new_road = road
    list_new_road = []
    for road in list_road:
#         print (road)
        new_road = road.lower()
        for index in range(len(list_word)):
            word = list_word[index].lower()
            abb = list_abb[index].lower()
            
            if (pattern_match(word, new_road) == True):
                new_road = new_road.replace(word, abb)
        list_new_road.append(new_road)
        print (new_road)
    #print (len(list_new_road))
    
    list_line = []
    for index in range(0, len(list_new_road)):
        line = list_road[index].lower() + ";" + list_new_road[index]
        list_line.append(line)
        print (line)
    
    # write_file(path, 'road_abbrevation_all', list_line)
if __name__ == '__main__':
    ## write the list of all roads including the abbrevation roads
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    
    name_abb = 'road_abbrevation.csv'
    name_road = 'road.csv'
    # check_abb(path, name)
    load_abb(path, name_abb)
    road_abb(path, name_road, load_abb(path, name_abb))
    