__author__ = 'vdthoang'
import json
from main.writeFile import write_file


if __name__ == '__main__':
    # path = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data'
    # name = 'tweet_short_for_icwsm2016.json'
    #
    # list_id = list()
    # with open(path + '/' + name) as data:
    #     json_data = json.load(data)
    #
    #     for each in json_data:
    #         print each['id']
    #         list_id.append(each['id'])
    #
    # print len(list_id)

    path = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data'
    name = 'tweet_short_event_tagged_for_icwsm2016.json'
    list_id = list()
    with open(path + '/' + name) as data:
        json_data = json.load(data)

        for each in json_data:
            print str(each['id']) + '\t' + str(each['accident']) + ' ' + str(each['crowd']) + ' ' \
                  + str(each['missing']) + ' ' + str(each['skip']) + ' ' + str(each['slow']) + ' ' + str(each['wait'])
            # print str(each['wait'])
            list_id.append(str(each['id']) + '\t' + str(each['accident']) + ' ' + str(each['crowd']) + ' ' \
                  + str(each['missing']) + ' ' + str(each['skip']) + ' ' + str(each['slow']) + ' ' + str(each['wait']))

    write_file(path, 'tweet_events', list_id)
    print len(list_id)
