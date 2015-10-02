'''
Created on 29 Jul 2015

@author: vdthoang
'''
from main.loadFile import load_file
from crawl.abbreviation import pattern_match
from main.writeFile import write_file


def match_road(string, list_road):
    list_index = []
    
    for index in range(0, len(list_road)):
        road = list_road[index]
        split_road = road.split(';')
        for token in split_road:
            if pattern_match(token, string) is True:
                list_index.append(index)
                break
    return list_index


def road_extract(path, name, list_road, list_road_original):
    list_extract = []
    cnt = 0
    with open(path + '/' + name) as f:
        for line in f:
            cnt += 1
            split_line = line.split('\t')
            list_index = match_road(split_line[1].lower(), list_road)  # make the text is lowercase
            if len(list_index) > 0:
                for index in list_index:
                    print (split_line[0] + '\t' + list_road_original[index])
                    list_extract.append(split_line[0] + '\t' + list_road_original[index])
            print (cnt)

    # write_file(path, 'posts_roads.csv', list_extract)
    # write_file(path, 'tweet_2015_filtering_roads.csv', list_extract)
    write_file(path, 'facebook_2015_BusNews_filtering_roads.csv', list_extract)
    
if __name__ == '__main__':
    # REMEMBER TO CHANGE NAME ON WRITE_FILE (LINE 33)
    path_road = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name_road = 'road_abbrevation_all.csv'
    list_road = load_file(path_road, name_road)
        
    path_road_original = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name_road_original = 'road.csv'
    list_road_original = load_file(path_road_original, name_road_original)
    
    print (str(len(list_road)) + '\t' + str(len(list_road_original)))
    
    # path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts'
    # name_text = 'posts_filter_v2.csv'

    # path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter'
    # name_text = 'tweet_2015_filtering.csv'

    path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    name_text = 'sg_fb_biz_feed_BusNews_filtering.csv'
    road_extract(path_text, name_text, list_road, list_road_original)