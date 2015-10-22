'''
Created on 30 Jul 2015

@author: vdthoang
'''
from main.loadFile import load_file
from main.writeFile import write_file
from extract.road_extraction import match_road

# Guideline for bus stop extraction
# First, extract bus stop based on the bus stop code
# Second, extract bus stop based on the bus stop name
# Merge file bus stop name & code
# Clean bus stop


def convert_busCode(list_busCode):
    list_ = []
    for index in range(1, len(list_busCode)):
        split_line = list_busCode[index].split('\t')
        busStopName = split_line[1].lower()
        list_.append(busStopName)
    return list_


def codeName_extraction(path, name, list_busCode, list_busCode_original):
    list_extract = []
    cnt = 0
    with open(path + '/' + name) as f:
        for line in f:
            cnt += 1

            split_line = line.split('\t')
            # we can also use the function in extract road name in extract the bus code name
            list_index = match_road(split_line[1].lower(), list_busCode)
            if len(list_index) > 0:
                for index in list_index:
                    # list_busCode_original have different index with list_busCode;
                    print (split_line[0] + '\t' + list_busCode_original[index + 1])
                    list_extract.append(split_line[0] + '\t' + list_busCode_original[index + 1])

            print cnt

    for value in list_extract:
        print value

    write_file(path, 'facebook_2015_BusNews_filtering_busStopName', list_extract)


##########################################################################################
##########################################################################################
def fix_busCodeName(path, name, list_busStopName, list_busCode_original):
    list_idBusStop = list()
    for index in range(1, len(list_busStopName)):
        split_line = list_busStopName[index].split('\t')
        id_index = split_line[0].lower()

        if id_index not in list_idBusStop:
            list_idBusStop.append(id_index)

    # cnt = 1
    list_extract = list()
    with open(path + '/' + name) as f:
        for text in f:
            split_line = text.strip().split('\t')
            id_text = split_line[0]
            if id_text in list_idBusStop:
                # we can also use the function in extract road name in extract the bus code name
                list_index = match_road(split_line[1].lower(), list_busCode)
                if len(list_index) > 0:
                    for index in list_index:
                        # list_busCode_original have different index with list_busCode;
                        print split_line[0] + '\t' + list_busCode_original[index + 1]
                        list_extract.append(split_line[0] + '\t' + list_busCode_original[index + 1])

    # write_file(path, 'tweet_2015_filtering_busStopName_fix', list_extract)
    # write_file(path, 'facebook_2015_filtering_busStopName_fix', list_extract)


if __name__ == '__main__':
    # extract the bus stop code name in text
    path_busCode = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name_busCode = 'bus_stop.csv'

    list_busCode_original = load_file(path_busCode, name_busCode)
    list_busCode = convert_busCode(list_busCode_original)  # convert list bus code to a right structure (not including the bus stop code and delete the first line
#     for each in list_busCode:
#         print each
#         
#     print (len(list_busCode) - 1)

#     path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts'
#     name_text = 'posts_filter_v2.csv'

    #################################################################################
    #################################################################################
    # path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter'
    # name_text = 'tweet_2015_filtering.csv'

    # path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook'
    # name_text = 'sg_fb_biz_feed_filtering.csv'
    # codeName_extraction(path_text, name_text, list_busCode, list_busCode_original)

    # path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    # name_text = 'sg_fb_biz_feed_BusNews_filtering.csv'
    # codeName_extraction(path_text, name_text, list_busCode, list_busCode_original)
    #################################################################################
    #################################################################################
    # FIX bus stop name on the Facebook & Twitter
    # Twitter
    # path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter'
    # name_text = 'tweet_2015_filtering.csv'
    #
    # path_BusStopName = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter'
    # name_BusStopName = 'tweet_2015_filtering_busStopName.csv'
    # loadBusStopName = load_file(path_BusStopName, name_BusStopName)

    # Facebook ---------------------------------------------------------------------------------

    # --all
    # path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook'
    # name_text = 'sg_fb_biz_feed_filtering.csv'
    #
    # path_BusStopName = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook'
    # name_BusStopName = 'facebook_2015_filtering_busStopName.csv'
    # loadBusStopName = load_file(path_BusStopName, name_BusStopName)
    # fix_busCodeName(path_text, name_text, loadBusStopName, list_busCode_original)

    # # --busNews
    # path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    # name_text = 'sg_fb_biz_feed_BusNews_filtering.csv'
    #
    # path_BusStopName = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    # name_BusStopName = 'facebook_2015_BusNews_filtering_busStopName.csv'
    # loadBusStopName = load_file(path_BusStopName, name_BusStopName)
    # fix_busCodeName(path_text, name_text, loadBusStopName, list_busCode_original)
