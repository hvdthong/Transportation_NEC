__author__ = 'vdthoang'
from main.loadFile import load_file
from classification_busService.ftr_bussvc_extraction import load_bus_svc
from classification_busService.ftr_bussvc_extraction import range_text_index
from feature_crf import load_dict


def gt_svc(list_line, load_svc):
    list_svc = []
    cnt = 0
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        for k in range(0, len(split_second)):
            if (split_first[k] in load_svc) and (int(split_second[k]) == 1):  # mean bus svc
                svc = split_first[k].lower() + ' '  # take the word which in svc dictionary
                list_svc.append(str(cnt) + '\t' + svc + '\t' + 'TRUE')
            if (split_first[k] in load_svc) and (int(split_second[k]) == 0):  # mean not bus svc
                svc = split_first[k].lower() + ' '  # take the word which in svc dictionary
                list_svc.append(str(cnt) + '\t' + svc + '\t' + 'FALSE')
        cnt += 1

    for value in list_svc:
        print value
    print len(list_svc)


##############################################################################
##############################################################################
def extract_ftr_gt_svc(list_line, load_svc, n_token):
    list_ftr = []
    cnt = 0
    cnt_true_svc = 0
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        for k in range(0, len(split_second)):
            if split_first[k] in load_svc:  # mean bus svc
                svc = split_first[k].lower() + ' '  # take the word which in svc dictionary
                range_k = range_text_index(k, len(split_second), n_token)

                ftr_text = ''
                for m in range(range_k[1], range_k[2] + 1):
                    ftr_text = ftr_text + ' ' + split_first[m]

                ftr_text = ftr_text.strip()

                if int(split_second[k]) == 1:
                    list_ftr.append(str(cnt) + '\t' + 'TRUE' + '\t' + svc + '\t' + ftr_text)
                elif int(split_second[k]) == 0:
                    list_ftr.append(str(cnt) + '\t' + 'FALSE' + '\t' + svc + '\t' + ftr_text)

            if int(split_second[k]) == 1:
                cnt_true_svc += 1
        cnt += 1

    for value in list_ftr:
        print value
    print 'Length of list features is: %i' % len(list_ftr)
    print 'Length of bus service labeling TRUE is: %i' % cnt_true_svc


##############################################################################
##############################################################################
def extract_ftr_gt_road_busstop(list_line, command, n_token):
    list_dict = load_dict(command)
    list_ftr = []
    cnt = 0
    for i in range(0, len(list_line), 3):
        split_first = 0
        split_second = 0

        if i % 3 == 0:
            split_first = list_line[i].strip().split('\t')
        j = i + 1
        if j % 3 == 1:
            split_second = list_line[j].strip().split('\t')

        for k in range(0, len(split_second)):
            label = 0
            if command == 'road':
                label = 2
            elif command == 'busstop':
                label = 3

            if label == 0:  # quit if we don't have the correct command
                print 'Give the correct command'
                quit()

            if (int(split_second[k] == label)) or (split_first[k].strip().lower() in list_dict):
                word = split_first[k].lower() + ' '  # take the word which in svc dictionary
                range_k = range_text_index(k, len(split_second), n_token)

                ftr_text = ''
                for m in range(range_k[1], range_k[2] + 1):
                    ftr_text = ftr_text + ' ' + split_first[m]

                ftr_text = ftr_text.strip()
                if int(split_second[k]) == label:
                    list_ftr.append(str(cnt) + '\t' + 'TRUE' + '\t' + word + '\t' + ftr_text)
                else:
                    list_ftr.append(str(cnt) + '\t' + 'FALSE' + '\t' + word + '\t' + ftr_text)
        cnt += 1

    for value in list_ftr:
        print value
    print 'Length of list features is: %i' % len(list_ftr)

##############################################################################
##############################################################################
if __name__ == '__main__':
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    name_all = 'Label_all_crf.txt'  # good
    file_line_all = load_file(path, name_all)

    # path_sv = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    # name_sv = 'bus_services.csv'
    # load_sv = load_bus_svc(load_file(path_sv, name_sv))
    # load_sv = [item.lower() for item in load_sv]
    #
    # # gt_svc(file_line_all, load_sv)
    #
    # n_ftr = 10
    # extract_ftr_gt_svc(file_line_all, load_sv, n_ftr)

    # extract_ftr_gt_road_busstop(file_line_all, command='road', n_token=5)
    extract_ftr_gt_road_busstop(file_line_all, command='busstop', n_token=5)
