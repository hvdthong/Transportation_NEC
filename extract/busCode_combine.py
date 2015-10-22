__author__ = 'vdthoang'

from main.loadFile import load_file
from main.writeFile import write_file


def stop_dict():
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name = 'bus_stop.csv'

    dictionary = load_file(path, name)[1:]
    all, codes, names = list(), list(), list()
    for word in dictionary:
        split_word = word.split('\t')
        code, name = split_word[0], split_word[1]
        codes.append(code), names.append(name)
    all.append(codes), all.append(names)
    # print len(codes), len(names), len(all)
    return all


def get_stopName(list_stopCode, dict):
    list_name = list()
    codes, names = dict[0], dict[1]
    for stop in list_stopCode:
        split_stop = stop.strip().split('\t')
        id, code = split_stop[0], split_stop[1]
        index = codes.index(code)
        name = names[index]

        string = id + '\t' + code + '\t' + name
        list_name.append(string)
    return list_name


if __name__ == '__main__':
    # this function use to combine between bus stop code and bus stop name

    # TWITTER
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter'
    # stop_name = 'tweet_2015_filtering_busStopName_fix.csv'
    # stop_code = 'tweet_2015_filtering_busStop.csv'
    #
    # load_stopName = load_file(path_, stop_name)  # load all stop name
    # # print len(load_stopName)
    # load_stopCode = load_file(path_, stop_code)[1:]  # load all stop code
    # # print len(load_stopCode)
    #
    # dictionary = stop_dict()
    # # get the stop name from stop code
    # list_stopCodeName = get_stopName(load_stopCode, dictionary)
    # list_all = load_stopName + list_stopCodeName
    # for value in list_all:
    #     print value
    # print len(list_all)
    # write_file(path_, 'tweet_2015_filtering_busStop_all', list_all)

    # FACEBOOK
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews'
    stop_name = 'facebook_2015_BusNews_filtering_busStopName.csv'
    stop_code = 'facebook_2015_BusNews_filtering_busStop.csv'

    load_stopName = load_file(path_, stop_name)  # load all stop name
    # print len(load_stopName)
    load_stopCode = load_file(path_, stop_code)  # load all stop code
    # print len(load_stopCode)

    dictionary = stop_dict()
    # get the stop name from stop code
    list_stopCodeName = get_stopName(load_stopCode, dictionary)
    list_all = load_stopName + list_stopCodeName

    for value in list_all:
        print value
    print len(list_all)
    write_file(path_, 'facebook_2015_BusNews_filtering_busStop_all', list_all)
