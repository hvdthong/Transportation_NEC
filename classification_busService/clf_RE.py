__author__ = 'vdthoang'
from main.loadFile import load_file
from classification_busService.ftr_bussvc_extraction import load_bus_svc
from main.pattern_busService import pattern_bus_service_ver2, pattern_bus_service
from sklearn import metrics


def extract_svc_expression(list_line, list_sv):
    y_label = []
    y_reg = []
    list_svc = []
    for line in list_line:
        split_line = line.split('\t')

        index = split_line[0]
        label = split_line[1]
        svc = split_line[2].strip()  # note that svc can be string or int => format svc as string
        list_svc.append(svc)
        text = split_line[3].strip()
        # print index, label, svc

        y_label.append(split_line[1])

        list_pattern_services = pattern_bus_service_ver2(text, list_sv)
        list_match_services = pattern_bus_service(text, list_sv)

        list_total = list(set(list_pattern_services) | set(list_match_services))

        if svc in list_total:
            y_reg.append('TRUE')
        else:
            y_reg.append('FALSE')

    for value in y_reg:
        print value

    # for i in range(0, len(y_reg)):
    #     if y_label[i] != y_reg[i]:
    #         print list_svc[i]

    print metrics.accuracy_score(y_label, y_reg)
    print metrics.classification_report(y_label, y_reg)
    print metrics.confusion_matrix(y_label, y_reg)


if __name__ == '__main__':
    # extract bus service using regular expression
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    name = 'feature_svc_n10.txt'

    path_sv = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name_sv = 'bus_services.csv'
    load_sv = load_bus_svc(load_file(path_sv, name_sv))
    list_sv = [item.lower() for item in load_sv]

    list_ftr = load_file(path, name)
    extract_svc_expression(list_ftr, list_sv)

