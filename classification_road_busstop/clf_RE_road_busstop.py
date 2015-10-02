__author__ = 'vdthoang'
from main.loadFile import load_file
from sklearn import metrics
from crawl.abbreviation import pattern_match
from main.writeFile import write_file
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def extract_road_busstop_expression(list_line, list_dict):
    y_label = []
    y_reg = []
    list_svc = []
    cnt = 1

    list_write = []
    for line in list_line:
        split_line = line.split('\t')

        index = split_line[0]
        label = split_line[1].strip()
        y_label.append(label)
        svc = split_line[2].strip()
        list_svc.append(svc)
        text = split_line[3].strip().lower()  # this is a text for road or bus stop
        # print index, label, svc

        list_road_match = []
        for index in range(0, len(list_dict)):
            road = list_road[index]
            split_road = road.split(';')
            for token in split_road:
                if pattern_match(token.lower(), text) is True:
                    split_token = token.split()
                    for value in split_token:
                        if value not in list_road_match:
                            list_road_match.append(value.lower())
                    break

        flag = 'FALSE'
        if svc in list_road_match:
            flag = 'TRUE'
            y_reg.append(flag)
        else:
            flag = 'FALSE'
            y_reg.append(flag)

        print '-- finished this line -- %i' % cnt + '\t' + flag
        list_write.append('-- finished this line -- %i' % cnt + '\t' + flag)
        cnt += 1
        break

    # for value in y_reg:
    #     print value

    # for i in range(0, len(y_reg)):
    #     if y_label[i] != y_reg[i]:
    #         print list_svc[i]

    write_file('d:/', 'busstop', list_write)

    print metrics.accuracy_score(y_label, y_reg)
    print metrics.classification_report(y_label, y_reg)
    print metrics.confusion_matrix(y_label, y_reg)


if __name__ == '__main__':
    # extract road and bus stop using regular expression
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    # name = 'feature_road_n5.txt'
    name = 'feature_busstop_n5.txt'
    list_line = load_file(path, name)

    # path_road = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    # name_road = 'road_abbrevation_all.csv'
    # list_road = load_file(path_road, name_road)

    path_road = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name_road = 'bus_stop_crf.csv'
    list_road = load_file(path_road, name_road)

    extract_road_busstop_expression(list_line, list_road)
