__author__ = 'vdthoang'
from main.loadFile import load_file
from CRF_labeling.feature_crf_all import filterTxt_CRF
from CRF_labeling.feature_crf_all import isAllDigit, isCapitalize, is_busPlate, isAllCharacter\
    , token_bef_matchDict, token_aft_matchDict, match_dict, reg_bussvc, match_road_busstop, load_dict_POS\
    , ftr_POS, token_bef_type, token_aft_type, load_dict_token_bef_aft_Twitter, ftr_token_bef_road_busstop\
    , ftr_token_bef_aft_svc
from main.writeFile import write_file


def create_part_of_speech(list_line):
    list_all, text_line, pos_line = list(), '', ''
    for line in list_line:
        if len(line) == 0:
            list_all.append(text_line.strip()), list_all.append(pos_line.strip()), list_all.append('\n')
            text_line, pos_line = '', ''
        else:
            split_line = line.split()
            text_line += '\t' + split_line[0]
            pos_line += '\t' + split_line[1]
    print len(list_line), len(list_all)

    # test if we have correct format for POS
    for i in range(0, len(list_all), 3):
        split_first = list_all[i].strip().split('\t')
        split_second = list_all[i + 1].strip().split('\t')

        if len(split_first) != len(split_second):
            print len(split_first), len(split_second)
            print list_all[i]
            print list_all[i + 1]
    return list_all


def count_POS(list_line):
    pos_list = list()
    for line in list_line:
        if len(line) != 0:
            split_line = line.split()
            if split_line[1] not in pos_list:
                pos_list.append(split_line[1])
    for pos in pos_list:
        print pos
    print len(pos_list)


def count_POS_ver2(list_line):
    pos_list = list()
    for i in range(0, len(list_line), 3):
        split_pos = list_line[i + 1].split('\t')
        for value in split_pos:
            if value not in pos_list:
                pos_list.append(value)
    for pos in pos_list:
        print pos
    print len(pos_list)


##############################################################################
##############################################################################
# intersection between POS & CRF, make them having the same length
def intersection(pos, crf):
    inter = set(pos).intersection(crf)
    return inter


def text_label_inter(list_, list_inter):
    cnt, list_all = 0, list()
    for i in range(0, len(list_), 3):
        text, label = list_[i].split('\t'), list_[i + 1].split('\t')
        new_text, new_lable = '', ''
        for j in range(0, len(text)):
            if text[j] in list_inter[cnt]:
                new_text += text[j] + '\t'
                new_lable += label[j] + '\t'
        list_all.append(new_text.strip()), list_all.append(new_lable.strip()), list_all.append('\n')
        cnt += 1
    return list_all


def intersection_POS_CRF(list_POS, list_CRF):
    list_inter = list()
    for i in range(0, len(list_POS), 3):
        pos, crf = list_POS[i].split('\t'), list_CRF[i].split('\t')
        list_inter.append(intersection(pos, crf))

    list_new_POS = text_label_inter(list_POS, list_inter)
    list_new_CRF = text_label_inter(list_CRF, list_inter)

    # for i in range(0, len(list_new_POS), 3):
    #     pos, crf = list_new_POS[i].split('\t'), list_new_CRF[i].split('\t')
    #     label_pos, label_crf = list_new_POS[i + 1].split('\t'), list_new_CRF[i + 1].split('\t')
    #     print pos
    #     print label_pos
    #     print len(pos), len(label_pos)
    #     print crf
    #     print label_crf
    #     print len(crf), len(label_crf)

    print len(list_new_POS), len(list_new_CRF)
    list_all_ = list()
    list_all_.append(list_new_POS), list_all_.append(list_new_CRF)
    return list_all_


if __name__ == '__main__':
    # USING FOR TWITTER

    # check the list of part-of-speech that we need to use
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    # name_POS = 'labeling_text_POS.txt'
    # list_ = load_file(path, name_POS)
    # count_POS(list_)
    # count_POS_ver2(list_new[0])

    # get the text for part-of-speech and our lablled data
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_POS'
    name_POS = 'labeling_text_POS.txt'
    name_CRF = 'labeling_all.txt'

    list_ = load_file(path, name_POS)
    list_all = create_part_of_speech(list_)
    list_POS = filterTxt_CRF(list_all, command='removeLink', command_data='twitter')
    list_CRF = filterTxt_CRF(load_file(path, name_CRF), command='removeLink', command_data='twitter')

    list_new = intersection_POS_CRF(list_POS, list_CRF)
    list_new_POS, list_new_CRF = list_new[0], list_new[1]  # note that part-of-speech will have same length now
    list_line_ = list_new_CRF

    # checking if our code is correct
    # for i in range(0, len(list_new_POS), 3):
    #     pos, crf = list_new_POS[i].split('\t'), list_new_CRF[i].split('\t')
    #     label_pos, label_crf = list_new_POS[i + 1].split('\t'), list_new_CRF[i + 1].split('\t')
    #     print len(pos), len(label_pos), len(crf), len(label_crf)

    # -------------- loading all tokens features type
    # ftr_isDigit = isAllDigit(list_line_)
    # write_file(path_write, 'ftr_isDigit', ftr_isDigit)
    # ftr_isCharacter = isAllCharacter(list_line_)
    # write_file(path_write, 'ftr_isCharacter', ftr_isCharacter)
    # ftr_isBusPlate = is_busPlate(list_line_)
    # write_file(path_write, 'ftr_isBusPlate', ftr_isBusPlate)
    # ftr_isCapitalized = isCapitalize(list_line_)
    # write_file(path_write, 'ftr_isCapitalized', ftr_isCapitalized)

    # -------------- loading all tokens match dictionary
    # note that the dictionary is the same in different datasets: SGFORUMS, TWITTER, FACEBOOK
    # ftr_match_dict_svc = match_dict(list_line_, command='svc')
    # write_file(path_write, 'ftr_match_dict_svc', ftr_match_dict_svc)
    # ftr_match_dict_road = match_dict(list_line_, command='road')
    # write_file(path_write, 'ftr_match_dict_road', ftr_match_dict_road)
    # ftr_match_dict_busstop = match_dict(list_line_, command='busstop')
    # write_file(path_write, 'ftr_match_dict_busstop', ftr_match_dict_busstop)

    # -------------- loading all tokens match bus service, road and bus stop using regular expression
    # note that the regular expression is the same in different datasets: SGFORUMS, TWITTER, FACEBOOK
    # ftr_reg_svc = reg_bussvc(list_line_, n_token=5, command='twitter')
    # write_file(path_write, 'ftr_reg_svc', ftr_reg_svc)
    # ftr_match_road = match_road_busstop(list_line_, command='road', num_process=1, data='twitter')
    # write_file(path_write, 'ftr_reg_match_road', ftr_match_road)
    # ftr_match_busstop = match_road_busstop(list_line_, command='busstop', num_process=1, data='twitter')
    # write_file(path_write, 'ftr_reg_match_busstop', ftr_match_busstop)

    # -------------- loading all tokens of part-of-speech
    # pos_dict = load_dict_POS()
    # ftr_POS(path_write, 'ftr_POS', list_new_POS, pos_dict)

    # -------------- loading all token before and after match dictionary
    # note that the dictionary is the same in different datasets: SGFORUMS, TWITTER, FACEBOOK
    # command = ['svc', 'road', 'busstop']
    # for value in command:
    #     list_command = token_bef_matchDict(list_line_, value)
    #     write_file(path_write, 'ftr_tok_bef_match_' + value, list_command)
    #
    # for value in command:
    #     list_command = token_aft_matchDict(list_line_, value)
    #     write_file(path_write, 'ftr_tok_aft_match_' + value, list_command)

    # -------------- loading all token type before and after labeling
    # types = ['Capitalized', 'Digit', 'Character', 'BusPlate']
    # for value in types:
    #     list_command = token_bef_type(list_line_, value)
    #     write_file(path_write, 'ftr_tok_bef_is' + value, list_command)
    #
    # for value in types:
    #     list_command = token_aft_type(list_line_, value)
    #     write_file(path_write, 'ftr_tok_aft_is' + value, list_command)

    # -------------- create list of features using actual word for token before in road and bus stop
    # use for road and bus stop
    # command = ['road', 'busstop']
    # for value in command:
    #     dict_ = load_dict_token_bef_aft_Twitter(value)
    #     ftr_token_bef_road_busstop(path_write, 'ftr_token_bef_' + value, list_line_, dict_)
    #
    # command = ['bef_svc', 'aft_svc']
    # for value in command:
    #     dict_ = load_dict_token_bef_aft_Twitter(value)
    #     ftr_token_bef_aft_svc(value, path_write, 'ftr_token_' + value, list_line_, dict_)
