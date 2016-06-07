__author__ = 'vdthoang'
from main.loadFile import load_file
from ICWSM_2016.corrAnalysis import bus_event


if __name__ == '__main__':
    # path = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data'
    path = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/ubicomp2016_paper/data'
    name_bussvc = 'twitter_bussvc.csv'
    list_bus = load_file(path, name_bussvc)

    events = ['crowd', 'skip', 'slow', 'wait']
    all_events_bussvc = list()
    for event in events:
        name = 'twitter_event_' + event + '.csv'
        list_event = load_file(path, name)

        all_events_bussvc.append(bus_event(event, list_event, list_bus))

    for i in range(0, len(all_events_bussvc)):
        unique = list(set(all_events_bussvc[i]))
        print len(unique), unique

    total_bussvc = 277
    for i in range(0, len(all_events_bussvc)):
        j = i + 1
        if i != len(all_events_bussvc) - 1:
            for j in range(i, len(all_events_bussvc)):
                list_i = all_events_bussvc[i]
                list_j = all_events_bussvc[j]

                list_merge_distinct = list(set(list_i + list_j))
                print str(i) + '\t' + str(j) + '\t' + str(277 - len(list_merge_distinct))
        else:
            break