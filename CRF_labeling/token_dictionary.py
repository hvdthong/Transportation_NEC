__author__ = 'vdthoang'
from main.loadFile import load_file
from nltk.stem import PorterStemmer
from main.filter_text import filter_token
from nltk.corpus import stopwords
from classification_busService.ftr_bussvc_extraction import is_int


def road_stop_token(list_line, command, stop_en):
    list_token = []
    cnt = 0
    for line in list_line:
        if command == 'abbr':  # no need to use
            split_line = line.split('\t')
            # port = PorterStemmer()
            # try:
            #     stem_word = port.stem(split_line[0])
            # except UnicodeDecodeError:
            #     # do nothing
            #     print 'Wrong stemming'
            # print split_line[0], stem_word  # get the word and stemmer word
            print split_line[0]

        elif command == 'road':
            split_line = line.split(';')
            for element in split_line:
                tokens = element.split()
                for each in tokens:
                    each = filter_token(each)
                    if (each not in list_token) and (each not in stop_en):
                        if is_int(each) is False:
                            list_token.append(each)

        elif command == 'busstop':
            cnt += 1
            split_line = line.split('\t')
            # if ('code' not in line) and ('name' not in line):
            if cnt > 1:
                tokens = split_line[1].split()
                for each in tokens:
                    filter_each = filter_token(each.strip())
                    if (filter_each not in list_token) and (len(filter_each) > 0) and (each not in stop_en):
                        if is_int(each) is False:
                            list_token.append(filter_each.strip())

        elif command == 'bussvc':
            cnt += 1
            split_line = line.split('\t')
            # if ('no' not in line) and ('routes' not in line) and ('type' not in line) and ('operator' not in line) and ('name' not in line):
            if cnt > 1:
                list_token.append(split_line[0].strip())
                # print split_line[0], cnt

    # for value in sorted(list_token):
    #     print value.lower()
    for value in list_token:
        print value.lower()
    print 'Total length of list: %i' % len(list_token)


if __name__ == '__main__':
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    # name = 'road_abbrevation.csv'
    # list_line = load_file(path, name)
    # command = 'abbr'  # no need to do the stemming
    # road_stop_token(list_line, command)

    # stop = stopwords.words('english')  # just to check all the stop words that need to be removed
    # stop = ['of', 'the']  # we can remove these words
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    # name = 'road_abbrevation_all.csv'
    # list_line = load_file(path, name)
    # command = 'road'  # no need to do the stemming
    # road_stop_token(list_line, command, stop)

    # stop = stopwords.words('english')  # just to check all the stop words that need to be removed
    # stop = ['at', 'of', 'the', 'by']
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    # name = 'bus_stop.csv'
    # list_line = load_file(path, name)
    # command = 'busstop'  # no need to do the stemming
    # road_stop_token(list_line, command, stop)

    stop = list()  # no need to use stop words in bus service
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name = 'bus_services.csv'
    list_line = load_file(path, name)
    command = 'bussvc'  # no need to do the stemming
    road_stop_token(list_line, command, stop)
