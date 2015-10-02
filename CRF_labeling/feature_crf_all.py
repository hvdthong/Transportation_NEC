__author__ = 'vdthoang'import sysfrom main.loadFile import load_filefrom main.writeFile import write_filefrom CRF_labeling.feature_crf import match_dict, reg_bussvc, isCapitalize, match_road_busstop, matching_token_bef, matching_token_aftfrom os import listdirimport re# make the default is 'utf-8'reload(sys)sys.setdefaultencoding('utf8')def folder_files(path):    # list of all files in folder    files = [f for f in listdir(path)]    return filesdef loading_ftr_CRF(list_line_):    # loading CRF features to a folder for running CRF    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features/features'    ftr_match_dict_svc = match_dict(list_line_, command='svc')    write_file(path_write, 'ftr_match_dict_svc', ftr_match_dict_svc)    ftr_match_dict_road = match_dict(list_line_, command='road')    write_file(path_write, 'ftr_match_dict_road', ftr_match_dict_road)    ftr_match_dict_busstop = match_dict(list_line_, command='busstop')    write_file(path_write, 'ftr_match_dict_busstop', ftr_match_dict_busstop)    print 'Finished loading match dictionary ------------------------------------'    ftr_isCapitalize = isCapitalize(list_line_)    write_file(path_write, 'ftr_isCapitalize', ftr_isCapitalize)    ftr_reg_svc = reg_bussvc(list_line_, n_token=10)    write_file(path_write, 'ftr_reg_svc', ftr_reg_svc)    ftr_match_road = match_road_busstop(list_line_, command='road')    write_file(path_write, 'ftr_match_road', ftr_match_road)    ftr_match_busstop = match_road_busstop(list_line_, command='busstop')    write_file(path_write, 'ftr_match_busstop', ftr_match_busstop)    print 'Finished loading regular expression and matching for road and bus stop ------------------------------------'    ftr_match_token_bef_svc = matching_token_bef(list_line_, command='svc')    write_file(path_write, 'ftr_match_token_bef_svc', ftr_match_token_bef_svc)    ftr_match_token_bef_road = matching_token_bef(list_line_, command='road')    write_file(path_write, 'ftr_match_token_bef_road', ftr_match_token_bef_road)    ftr_match_token_bef_busstop = matching_token_bef(list_line_, command='busstop')    write_file(path_write, 'ftr_match_token_bef_busstop', ftr_match_token_bef_busstop)    ftr_match_token_aft_svc = matching_token_aft(list_line_, command='svc')    write_file(path_write, 'ftr_match_token_aft_svc', ftr_match_token_aft_svc)    print 'Finished loading for token before and after the label ------------------------------------'    return None############################################################################################################################################################################################################# CONTINUE TO CREATE A LIST OF FEATURESdef isAllDigit(list_line):    # check if string is number or not    # Ex: "123" -> True, "3.43" -> False, "a12" -> False    list_ftr = []    for i in range(0, len(list_line), 3):        split_first = 0        split_second = 0        if i % 3 == 0:            split_first = list_line[i].strip().split('\t')        j = i + 1        if j % 3 == 1:            split_second = list_line[j].strip().split('\t')        feature = ''        for value in split_first:            if value.isdigit() is True:                feature += '1'            else:                feature += '0'        # print len(split_first), split_first        # print len(feature), feature        list_ftr.append(feature)    return list_ftrdef isAllCharacter(list_line):    # Return true if all characters in the string are alphabetic and there is at least one character, false otherwise.    # Ex: "ab23" -> False, "abc" -> True    list_ftr = []    for i in range(0, len(list_line), 3):        split_first = 0        split_second = 0        if i % 3 == 0:            split_first = list_line[i].strip().split('\t')        j = i + 1        if j % 3 == 1:            split_second = list_line[j].strip().split('\t')        feature = ''        for value in split_first:            if value.isalpha() is True:                feature += '1'            else:                feature += '0'        # print len(split_first), split_first        # print len(feature), feature        list_ftr.append(feature)    return list_ftrdef is_busPlate(list_line):    # check if the token is a bus plate number or not    list_ftr = []    for i in range(0, len(list_line), 3):        split_first = 0        split_second = 0        if i % 3 == 0:            split_first = list_line[i].strip().split('\t')        j = i + 1        if j % 3 == 1:            split_second = list_line[j].strip().split('\t')        pattern = r'[A-z]{3}[0-9]+[A-z]{1}'        feature = ''        for value in split_first:            if re.match(pattern, value):                feature += '1'            else:                feature += '0'        # print len(split_first), split_first        # print len(feature), feature        list_ftr.append(feature)    return list_ftr############################################################################################################################################################################################################def token_bef_matchDict(list_line, command):    # check the token before labeling, if it matches dictionary -> return True, else -> return False    for i in range(0, len(list_line), 3):        split_first = 0        split_second = 0        if i % 3 == 0:            split_first = list_line[i].strip().split('\t')        j = i + 1        if j % 3 == 1:            split_second = list_line[j].strip().split('\t')        print split_first############################################################################################################################################################################################################if __name__ == '__main__':    # construct list of all features used for running CRF    # loading list of features we have in to folder    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'    # name_ = 'Label_all_crf.txt'    # list_line = load_file(path_, name_)    # loading_ftr_CRF(list_line)    # print len(list_line)    # list of all files in folder    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features/features'    # files_ = folder_files(path_)    #    # for f in files_:    #     print f    #    # print len(files_)    ######################################################################################################    ######################################################################################################    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'    name_ = 'Label_all_crf.txt'    list_line_ = load_file(path_, name_)    # isAllDigit(list_line)    # isAllCharacter(list_line_)    # is_busPlate(list_line_)    token_bef_matchDict(list_line_, command='svc')