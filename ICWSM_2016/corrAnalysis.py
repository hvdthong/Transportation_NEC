__author__ = 'vdthoang'
from main.loadFile import load_file


def dist_events(list_, event):
    cnt = 0
    for line in list_:
        split_ = line.split('\t')
        if int(split_[1]) == 1:
            cnt += 1

    print event + ':' + '\t' + str(cnt)


#########################################################################################
#########################################################################################
def load_tweetID_event(list_):
    list_id = list()
    for value in list_:
        split = value.split('\t')
        if int(split[1]) == 1:
            list_id.append(split[0])
    return list_id


def bus_event(event, list_event, list_bus):
    list_id_event = load_tweetID_event(list_event)
    list_busvc_event = list()
    for id in list_id_event:
        for line in list_bus:
            split_line = line.split('\t')
            if id == split_line[0]:
                if split_line[3] not in list_busvc_event:
                    list_busvc_event.append(split_line[3])

    print event + '\t' + str(len(list_busvc_event))
    print event, list_busvc_event
    return list_busvc_event


#########################################################################################
#########################################################################################
if __name__ == '__main__':
    # events = ['accident', 'crowd', 'missing', 'skip', 'slow', 'wait']
    # for event in events:
    #     path = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data'
    #     name = 'twitter_event_' + event + '.csv'
    #     list_ = load_file(path, name)
    #     dist_events(list_, event)

    # path = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data'
    path = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/ubicomp2016_paper/data'
    name_bussvc = 'twitter_bussvc.csv'
    list_bus = load_file(path, name_bussvc)

    # events = ['accident', 'crowd', 'missing', 'skip', 'slow', 'wait']
    events = ['crowd', 'skip', 'slow', 'wait']
    all_events_bussvc = list()
    for event in events:
        name = 'twitter_event_' + event + '.csv'
        list_event = load_file(path, name)

        all_events_bussvc.append(bus_event(event, list_event, list_bus))

    for i in range(0, len(all_events_bussvc)):
        j = i + 1
        if i != len(all_events_bussvc) - 1:
            for j in range(i, len(all_events_bussvc)):
                list_i = all_events_bussvc[i]
                list_j = all_events_bussvc[j]

                list_overlap = set(list_i) & set(list_j)
                print i, j, len(list_overlap)
        else:
            break
