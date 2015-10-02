__author__ = 'vdthoang'

from main.loadFile import load_file
from nltk.stem import PorterStemmer
from main.writeFile import write_file


def eventList():
    event_1 = ['jam']
    event_2 = ['bunch']
    event_3 = ['delay', 'slow']
    event_4 = ['air-con', 'aircon', 'air-condit', 'aircondit']
    event_5 = ['kill', 'dead']
    event_6 = ['accident', 'accid']
    event_7 = ['breakdown', 'break-down']
    event_8 = ['crowd', 'squeeze', 'squeez']

    list_event = []
    list_event.append(event_1)
    list_event.append(event_2)
    list_event.append(event_3)
    list_event.append(event_4)
    list_event.append(event_5)
    list_event.append(event_6)
    list_event.append(event_7)
    list_event.append(event_8)

    return list_event

def eventRecg(port, string, list_event):
    split_string = string.strip().split()
    event_cnt = []

    for token in split_string:
        try:
            stemm = port.stem(token)
            for event in list_event:
                if (stemm in event):
                    if (event[0] not in event_cnt):
                        event_cnt.append(event[0])

        except UnicodeDecodeError: ##error when convert
            ## do nothing
            stemm = ''
    return event_cnt


def detectEvent(path, name, name_write, list_event):
    loadText = load_file(path, name)
    port = PorterStemmer()

    list_write = []
    for text in loadText:
        split_text = text.strip().split('\t')
        if (len(split_text) == 2):
            print text
            events = eventRecg(port, split_text[1].strip().lower(), list_event)

            if (len(events) > 0):
                print split_text[0], '\t', events
                for event in events:
                    list_write.append(split_text[0] + '\t' + event)

    write_file(path, name_write, list_write)

if __name__ == '__main__':
    ## SGFORUMS
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts'
    # name = 'posts_filter_v2.csv'
    # # name_write = 'posts_filter_v2_events' #only 7 events
    # name_write = 'posts_filter_v2_events_ver2' #8 events

    ## TWITTER
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter'
    # name = 'tweet_2015_filtering.csv'
    # # # name_write = 'tweet_2015_filtering_events_ver2' #only 7 events
    # name_write = 'tweet_2015_filtering_events_ver3' #8 events

    ## FACEBOOK
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    name = 'sg_fb_biz_feed_BusNews_filtering.csv'
    # name_write = 'facebook_2015_BusNews_filtering_events' #only 7 events
    name_write = 'facebook_2015_BusNews_filtering_events_ver2' #8 events

    list_event = eventList()
    detectEvent(path, name, name_write, list_event)

    ###################################################################
    # port = PorterStemmer()
    # list_ = eventList()
    # for event in list_:
    #     for value in event:
    #         print value + '\t' + port.stem(value)



