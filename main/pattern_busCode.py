'''
Created on 20 Jul 2015

@author: vdthoang
'''


def load_bus_stop_code(path, name):
    i = 0    
    list_bus_code = []
    
    with open(path + '/' + name) as f:
        for line in f:
            if (i != 0):
                split_line = line.split('\t')
                list_bus_code.append(split_line[0])
            i += 1
    return list_bus_code


def find_bus_code(text, list_bus_stop):
    split_text = text.split()
    post_bus_stop = list()
    
    for token in split_text:
        if token in list_bus_stop:
            if token not in post_bus_stop:
                post_bus_stop.append(token)
    return post_bus_stop


def extract_bus_code(path, name, list_bus_stop):
    list_write = []
    
    with open(path + '/' + name) as f:
        i = 0
        for line in f:
            split_line = line.split('\t')
            post_bus_stop = find_bus_code(split_line[1], list_bus_stop)
            if len(post_bus_stop) != 0:
                for each in post_bus_stop:
                    list_write.append(split_line[0] + '\t' + each)
                print str(i) + '\t' + split_line[0] + '\t' + str(post_bus_stop)
                # print (str(i) + '\t' + split_line[0] + '\t' + str(len(post_bus_stop)))
                i += 1
            
    for each in list_write:
        print each
    
if __name__ == '__main__':
    path_bus_stop = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name_bus_stop = 'bus_stop.csv'
    list_bus_stop = load_bus_stop_code(path_bus_stop, name_bus_stop)
    
#     path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20150714'
#     name_text = 'posts_filter.csv'

    # path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts'
    # name_text = 'posts_filter.csv'

    #####################################################################################
    #####################################################################################
    # Using for Twitter collection
    path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter'
    name_text = 'plr_sg_tweet_2015_filtering.csv'

    # Using for Facebook collection
    path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook'
    name_text = 'sg_fb_biz_feed_filtering.csv'

    # Using for Facebook BUS TRANSPORTATION (LTA and SMRT) collection
    path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook'
    name_text = 'sg_fb_biz_feed_BusTransport_filtering.csv'

    # Using for Facebook BUS NEWS collection
    path_text = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    name_text = 'sg_fb_biz_feed_BusNews_filtering.csv'
    extract_bus_code(path_text, name_text, list_bus_stop)
