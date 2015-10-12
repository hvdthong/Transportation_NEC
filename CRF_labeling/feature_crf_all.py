__author__ = 'vdthoang'import sysfrom main.loadFile import load_filefrom main.writeFile import write_filefrom CRF_labeling.feature_crf import match_dict, reg_bussvc, \    isCapitalize, match_road_busstop, matching_token_bef, matching_token_aftfrom os import listdirimport refrom CRF_labeling.feature_crf import load_dictfrom CRF_labeling.feature_token_crf import token_matchDict, \    token_isAllCharacter, token_isAllDigit, token_isBusPlate, token_isCapitalizedfrom CRF_labeling.filterText_CRF import filterTxt_CRF# make the default is 'utf-8'reload(sys)sys.setdefaultencoding('utf8')def folder_files(path):    # list of all files in folder    files = [f for f in listdir(path)]    return filesdef loading_ftr_CRF(list_line_):    # loading CRF features to a folder for running CRF    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features/features'    ftr_match_dict_svc = match_dict(list_line_, command='svc')    write_file(path_write, 'ftr_match_dict_svc', ftr_match_dict_svc)    ftr_match_dict_road = match_dict(list_line_, command='road')    write_file(path_write, 'ftr_match_dict_road', ftr_match_dict_road)    ftr_match_dict_busstop = match_dict(list_line_, command='busstop')    write_file(path_write, 'ftr_match_dict_busstop', ftr_match_dict_busstop)    print 'Finished loading match dictionary ------------------------------------'    ftr_isCapitalized = isCapitalize(list_line_)    write_file(path_write, 'ftr_isCapitalized', ftr_isCapitalized)    ftr_reg_svc = reg_bussvc(list_line_, n_token=10)    write_file(path_write, 'ftr_reg_svc', ftr_reg_svc)    ftr_match_road = match_road_busstop(list_line_, command='road')    write_file(path_write, 'ftr_reg_match_road', ftr_match_road)    ftr_match_busstop = match_road_busstop(list_line_, command='busstop')    write_file(path_write, 'ftr_reg_match_busstop', ftr_match_busstop)    print 'Finished loading regular expression and matching for road and bus stop ------------------------------------'    ftr_match_token_bef_svc = matching_token_bef(list_line_, command='svc')    write_file(path_write, 'ftr_match_token_bef_svc', ftr_match_token_bef_svc)    ftr_match_token_bef_road = matching_token_bef(list_line_, command='road')    write_file(path_write, 'ftr_match_token_bef_road', ftr_match_token_bef_road)    ftr_match_token_bef_busstop = matching_token_bef(list_line_, command='busstop')    write_file(path_write, 'ftr_match_token_bef_busstop', ftr_match_token_bef_busstop)    ftr_match_token_aft_svc = matching_token_aft(list_line_, command='svc')    write_file(path_write, 'ftr_match_token_aft_svc', ftr_match_token_aft_svc)    print 'Finished loading for token before and after the label ------------------------------------'    return None############################################################################################################################################################################################################# CONTINUE TO CREATE A LIST OF FEATURESdef isAllDigit(list_line):    # check if string is number or not    # Ex: "123" -> True, "3.43" -> False, "a12" -> False    list_ftr = []    for i in range(0, len(list_line), 3):        split_first = 0        split_second = 0        if i % 3 == 0:            split_first = list_line[i].strip().split('\t')        j = i + 1        if j % 3 == 1:            split_second = list_line[j].strip().split('\t')        feature = ''        for value in split_first:            if value.isdigit() is True:                feature += '1'            else:                feature += '0'        # print len(split_first), split_first        # print len(feature), feature        list_ftr.append(feature)    return list_ftrdef isAllCharacter(list_line):    # Return true if all characters in the string are alphabetic and there is at least one character, false otherwise.    # Ex: "ab23" -> False, "abc" -> True    list_ftr = []    for i in range(0, len(list_line), 3):        split_first = 0        split_second = 0        if i % 3 == 0:            split_first = list_line[i].strip().split('\t')        j = i + 1        if j % 3 == 1:            split_second = list_line[j].strip().split('\t')        feature = ''        for value in split_first:            if value.isalpha() is True:                feature += '1'            else:                feature += '0'        # print len(split_first), split_first        # print len(feature), feature        list_ftr.append(feature)    return list_ftrdef is_busPlate(list_line):    # check if the token is a bus plate number or not    list_ftr = []    for i in range(0, len(list_line), 3):        split_first = 0        split_second = 0        if i % 3 == 0:            split_first = list_line[i].strip().split('\t')        j = i + 1        if j % 3 == 1:            split_second = list_line[j].strip().split('\t')        pattern = r'[A-z]{3}[0-9]+[A-z]{1}'        feature = ''        for value in split_first:            if re.match(pattern, value):                feature += '1'            else:                feature += '0'        # print len(split_first), split_first        # print len(feature), feature        list_ftr.append(feature)    return list_ftr############################################################################################################################################################################################################def token_bef_matchDict(list_line, command):    # check the token before labeling, if it matches dictionary -> return True, else -> return False    dictionary = []    if command == 'svc' or command == 'road' or command == 'busstop':        dictionary = load_dict(command)    else:        print 'You need to give correct command'        quit()    list_ftr = []    for i in range(0, len(list_line), 3):        split_first = 0        split_second = 0        if i % 3 == 0:            split_first = list_line[i].strip().split('\t')        j = i + 1        if j % 3 == 1:            split_second = list_line[j].strip().split('\t')        ftr = ''        for k in range(0, len(split_first)):            if k == 0:                ftr += '0'            else:                token_bef = split_first[k - 1].strip().lower()                if token_matchDict(token_bef, dictionary) is True:                    ftr += '1'                else:                    ftr += '0'        # print len(split_first), split_first        # print len(ftr), ftr        list_ftr.append(ftr)    return list_ftrdef token_aft_matchDict(list_line, command):    # check the token after labeling, if it matches dictionary -> return True, else -> return False    dictionary = []    if command == 'svc' or command == 'road' or command == 'busstop':        dictionary = load_dict(command)    else:        print 'You need to give correct command'        quit()    list_ftr = []    for i in range(0, len(list_line), 3):        split_first = 0        split_second = 0        if i % 3 == 0:            split_first = list_line[i].strip().split('\t')        j = i + 1        if j % 3 == 1:            split_second = list_line[j].strip().split('\t')        ftr = ''        for k in range(0, len(split_first)):            if k == len(split_first) - 1:                ftr += '0'            else:                token_aft = split_first[k + 1].strip().lower()                if token_matchDict(token_aft, dictionary) is True:                    ftr += '1'                else:                    ftr += '0'        # print len(split_first), split_first        # print len(ftr), ftr        list_ftr.append(ftr)    return list_ftr############################################################################################################################################################################################################def token_bef_type(list_line, command):    # check the type of token before labeling    list_ftr = []    for i in range(0, len(list_line), 3):        split_first = 0        split_second = 0        if i % 3 == 0:            split_first = list_line[i].strip().split('\t')        j = i + 1        if j % 3 == 1:            split_second = list_line[j].strip().split('\t')        ftr = ''        for k in range(0, len(split_first)):            if k == 0:                ftr += '0'            else:                token_bef = split_first[k - 1].strip().lower()                if command == 'Capitalized':                    token_bef = split_first[k - 1].strip()                    if token_isCapitalized(token_bef) is True:                        ftr += '1'                    else:                        ftr += '0'                elif command == 'Digit':                    if token_isAllDigit(token_bef) is True:                        ftr += '1'                    else:                        ftr += '0'                elif command == 'Character':                    if token_isAllCharacter(token_bef) is True:                        ftr += '1'                    else:                        ftr += '0'                elif command == 'BusPlate':                    if token_isBusPlate(token_bef) is True:                        ftr += '1'                    else:                        ftr += '0'                else:                    print 'Please give the correct command'                    quit()        # print len(split_first), split_first        # print len(ftr), ftr        list_ftr.append(ftr)    return list_ftrdef token_aft_type(list_line, command):    # check the type of token after labeling    list_ftr = []    for i in range(0, len(list_line), 3):        split_first = 0        split_second = 0        if i % 3 == 0:            split_first = list_line[i].strip().split('\t')        j = i + 1        if j % 3 == 1:            split_second = list_line[j].strip().split('\t')        ftr = ''        for k in range(0, len(split_first)):            if k == len(split_first) - 1:                ftr += '0'            else:                token_aft = split_first[k + 1].strip().lower()                if command == 'Capitalized':                    token_aft = split_first[k + 1].strip()                    if token_isCapitalized(token_aft) is True:                        ftr += '1'                    else:                        ftr += '0'                elif command == 'Digit':                    if token_isAllDigit(token_aft) is True:                        ftr += '1'                    else:                        ftr += '0'                elif command == 'Character':                    if token_isAllCharacter(token_aft) is True:                        ftr += '1'                    else:                        ftr += '0'                elif command == 'BusPlate':                    if token_isBusPlate(token_aft) is True:                        ftr += '1'                    else:                        ftr += '0'                else:                    print 'Please give the correct command'                    quit()        # print len(split_first), split_first        # print len(ftr), ftr        list_ftr.append(ftr)    return list_ftr############################################################################################################################################################################################################def load_dict_token_bef_aft(command):    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features'    if command == 'road':        name = 'all_token_bef_road.txt'    elif command == 'busstop':        name = 'all_token_bef_busstop.txt'    elif command == 'bef_svc':        name = 'all_token_bef_bussvc.txt'    elif command == 'aft_svc':        name = 'all_token_aft_bussvc.txt'    else:        print 'You need to give the correct command'        quit()    list_file = load_file(path, name)    return list_filedef load_dict_token_bef_aft_Twitter(command):    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features'    if command == 'road':        name = 'all_token_bef_road.csv'    elif command == 'busstop':        name = 'all_token_bef_busstop.csv'    elif command == 'bef_svc':        name = 'all_token_bef_bussvc.csv'    elif command == 'aft_svc':        name = 'all_token_aft_bussvc.csv'    else:        print 'You need to give the correct command'        quit()    list_file = load_file(path, name)    return list_file############################################################################################################################################################################################################def write_ftr_token_bef_road_busstop(path_write, name_write, list_line, dict_token):    list_ftr = []    for i in range(0, len(list_line), 3):        split_first = 0        split_second = 0        if i % 3 == 0:            split_first = list_line[i].strip().split('\t')        j = i + 1        if j % 3 == 1:            split_second = list_line[j].strip().split('\t')        ftr = ''        for k in range(0, len(split_first)):            if k == 0:                ftr += '0'            else:                token_bef = split_first[k - 1].strip().lower()                if token_bef == dict_token:                    ftr += '1'                else:                    ftr += '0'        list_ftr.append(ftr)    write_file(path_write, name_write, list_ftr)    return Nonedef ftr_token_bef_road_busstop(path_write, name_write, list_line, dictionary):    for index in range(0, len(dictionary)):        write_ftr_token_bef_road_busstop(path_write, name_write + '_dict_' + str(index), list_line, dictionary[index])############################################################################################################################################################################################################def write_ftr_token_bef_aft_svc(command, path_write, name_write, list_line, dict_token):    list_ftr = []    for i in range(0, len(list_line), 3):        split_first = 0        split_second = 0        if i % 3 == 0:            split_first = list_line[i].strip().split('\t')        j = i + 1        if j % 3 == 1:            split_second = list_line[j].strip().split('\t')        ftr = ''        for k in range(0, len(split_first)):            if command == 'bef_svc':                if k == 0:                    ftr += '0'                else:                    token_bef = split_first[k - 1].strip().lower()                    if token_bef == dict_token:                        ftr += '1'                    else:                        ftr += '0'            elif command == 'aft_svc':                if k == len(split_first) - 1:                    ftr += '0'                else:                    token_aft = split_first[k + 1].strip().lower()                    if token_aft == dict_token:                        ftr += '1'                    else:                        ftr += '0'            else:                print 'You need to give the correct command'                quit()        list_ftr.append(ftr)    write_file(path_write, name_write, list_ftr)    return Nonedef ftr_token_bef_aft_svc(command, path_write, name_write, list_line, dictionary):    for index in range(0, len(dictionary)):        write_ftr_token_bef_aft_svc(command, path_write, name_write + '_dict_' + str(index), list_line, dictionary[index])############################################################################################################################################################################################################if __name__ == '__main__':    # construct list of all features used for running CRF    # loading list of features we have in to folder    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'    # name_ = 'Label_all_crf.txt'    # list_line = load_file(path_, name_)    # loading_ftr_CRF(list_line)    # print len(list_line)    # list of all files in folder    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features/features'    # files_ = folder_files(path_)    #    # for f in files_:    #     print f    #    # print len(files_)    ######################################################################################################    ######################################################################################################    # EXTRACT FEATURES FOR SGFORUMS DATASET    # path used to load your data    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'    # name_ = 'Label_all_crf.txt'    # list_line_ = load_file(path_, name_)    # path used to write your file    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features/features'    # -------------- loading all token features type    # ftr_isDigit = isAllDigit(list_line_)    # write_file(path_write, 'ftr_isDigit', ftr_isDigit)    # ftr_isCharacter = isAllCharacter(list_line_)    # write_file(path_write, 'ftr_isCharacter', ftr_isCharacter)    # ftr_isBusPlate = is_busPlate(list_line_)    # write_file(path_write, 'ftr_isBusPlate', ftr_isBusPlate)    # -------------- loading all token before and after match dictionary    # command = ['svc', 'road', 'busstop']    # for value in command:    #     list_command = token_bef_matchDict(list_line_, value)    #     write_file(path_write, 'ftr_tok_bef_match_' + value, list_command)    # for value in command:    #     list_command = token_aft_matchDict(list_line_, value)    #     write_file(path_write, 'ftr_tok_aft_match_' + value, list_command)    # -------------- loading all token type before and after labeling    # types = ['Capitalized', 'Digit', 'Character', 'BusPlate']    # for value in types:    #     list_command = token_bef_type(list_line_, value)    #     write_file(path_write, 'ftr_tok_bef_is' + value, list_command)    # for value in types:    #     list_command = token_aft_type(list_line_, value)    #     write_file(path_write, 'ftr_tok_aft_is' + value, list_command)    # -------------- create list of features using actual word for token before in road and bus stop    # use for road and bus stop    # command = ['road', 'busstop']    # for value in command:    #     dict_ = load_dict_token_bef_aft(value)    #     ftr_token_bef_road_busstop(path_write, 'ftr_token_bef_' + value, list_line_, dict_)    # command = ['bef_svc', 'aft_svc']    # for value in command:    #     dict_ = load_dict_token_bef_aft(value)    #     ftr_token_bef_aft_svc(value, path_write, 'ftr_token_' + value, list_line_, dict_)    ######################################################################################################    ######################################################################################################    ######################################################################################################    ######################################################################################################    # EXTRACT FEATURES FOR TWITTER DATASET    # path used to load your data    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'    name_ = 'labeling_all.txt'    # # use to remove all punctuation    # list_line_ = filterTxt_CRF(load_file(path_, name_), command='removePunc')    # # path used to write your file    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features'    list_line_ = filterTxt_CRF(load_file(path_, name_), command='removeLink')    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLink'    # -------------- loading all tokens features type    # ftr_isDigit = isAllDigit(list_line_)    # write_file(path_write, 'ftr_isDigit', ftr_isDigit)    # ftr_isCharacter = isAllCharacter(list_line_)    # write_file(path_write, 'ftr_isCharacter', ftr_isCharacter)    # ftr_isBusPlate = is_busPlate(list_line_)    # write_file(path_write, 'ftr_isBusPlate', ftr_isBusPlate)    # ftr_isCapitalized = isCapitalize(list_line_)    # write_file(path_write, 'ftr_isCapitalized', ftr_isCapitalized)    # -------------- loading all tokens match dictionary    # note that the dictionary is the same in different datasets: SGFORUMS, TWITTER, FACEBOOK    # ftr_match_dict_svc = match_dict(list_line_, command='svc')    # write_file(path_write, 'ftr_match_dict_svc', ftr_match_dict_svc)    # ftr_match_dict_road = match_dict(list_line_, command='road')    # write_file(path_write, 'ftr_match_dict_road', ftr_match_dict_road)    # ftr_match_dict_busstop = match_dict(list_line_, command='busstop')    # write_file(path_write, 'ftr_match_dict_busstop', ftr_match_dict_busstop)    # -------------- loading all tokens match bus service, road and bus stop using regular expression    # note that the regular expression is the same in different datasets: SGFORUMS, TWITTER, FACEBOOK    # ftr_reg_svc = reg_bussvc(list_line_, n_token=10)    # write_file(path_write, 'ftr_reg_svc', ftr_reg_svc)    # ftr_match_road = match_road_busstop(list_line_, command='road')    # write_file(path_write, 'ftr_reg_match_road', ftr_match_road)    # ftr_match_busstop = match_road_busstop(list_line_, command='busstop')    # write_file(path_write, 'ftr_reg_match_busstop', ftr_match_busstop)    # -------------- loading all token before and after match dictionary    # note that the dictionary is the same in different datasets: SGFORUMS, TWITTER, FACEBOOK    # command = ['svc', 'road', 'busstop']    # for value in command:    #     list_command = token_bef_matchDict(list_line_, value)    #     write_file(path_write, 'ftr_tok_bef_match_' + value, list_command)    #    # for value in command:    #     list_command = token_aft_matchDict(list_line_, value)    #     write_file(path_write, 'ftr_tok_aft_match_' + value, list_command)    # -------------- loading all token type before and after labeling    # types = ['Capitalized', 'Digit', 'Character', 'BusPlate']    # for value in types:    #     list_command = token_bef_type(list_line_, value)    #     write_file(path_write, 'ftr_tok_bef_is' + value, list_command)    #    # for value in types:    #     list_command = token_aft_type(list_line_, value)    #     write_file(path_write, 'ftr_tok_aft_is' + value, list_command)    # -------------- create list of features using actual word for token before in road and bus stop    # use for road and bus stop    command = ['road', 'busstop']    for value in command:        dict_ = load_dict_token_bef_aft_Twitter(value)        ftr_token_bef_road_busstop(path_write, 'ftr_token_bef_' + value, list_line_, dict_)    # command = ['bef_svc', 'aft_svc']    # for value in command:    #     dict_ = load_dict_token_bef_aft_Twitter(value)    #     ftr_token_bef_aft_svc(value, path_write, 'ftr_token_' + value, list_line_, dict_)