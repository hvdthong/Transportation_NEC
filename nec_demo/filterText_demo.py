__author__ = 'vdthoang'
import MySQLdb
from main.writeFile import write_file
from CRF_labeling.filterText_CRF import filter_eachTok_rmLinks
from CRF_labeling.feature_crf_all import isAllDigit, isAllCharacter, is_busPlate, isCapitalize, match_dict
from CRF_labeling.feature_crf_all import reg_bussvc, match_road_busstop, token_aft_matchDict, token_bef_matchDict\
    , token_aft_type, token_bef_type, load_dict_token_bef_aft_Twitter, ftr_token_bef_road_busstop\
    , ftr_token_bef_aft_svc, load_dict_token_bef_aft, load_dict_token_bef_aft_Facebook


def load_sql(command):
    if command == 'twitter':
        sql = 'select tweetText from tweet_2015 order by tweetID;'
        return sql
    elif command == 'sgforums':
        sql = 'select summary from sgforums_2015 order by post_id;'
        return sql
    elif command == 'facebook':
        sql = 'select post from facebook_2015 order by facebookID;'
        return sql
    else:
        print 'Give the correct command'
        quit()


def table_SQL(sql):
    # load data to server
    db = MySQLdb.connect(host="10.0.106.71",  # your host, usually localhost
                     user="vdthoang",  # your username
                      passwd="LARCuser1142",  # your password
                      db="nec_demo")  # name of the data base

    cur = db.cursor()
    # Use all the SQL you like
    cur.execute(sql)

    list_row = list()
    # print all the first cell of all the rows
    for row in cur.fetchall():
        # print row[0]
        list_row.append(row[0])
    return list_row


def filtering_text_demo(list_line, command):
    list_demo = list()
    for line in list_line:
        text = ''
        split_line = line.split()
        for token in split_line:
            token_filter = filter_eachTok_rmLinks(token, command)

            if len(token_filter) != 0:
                text += token_filter + '\t'

        # print text.strip()
        list_demo.append(text.strip())
        list_demo.append('\n')
        list_demo.append('\n')
    return list_demo


if __name__ == '__main__':
    ######################################################################################################
    ######################################################################################################
    # TWITTER
    # sql = load_sql(command='twitter')
    # list_row = table_SQL(sql)
    # list_line = filtering_text_demo(list_row, '')  # remmeber that we remove links in Twitter
    #
    # list_line_ = list_line
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/twitter/crf_features'

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
    # ftr_reg_svc = reg_bussvc(list_line_, n_token=5)
    # write_file(path_write, 'ftr_reg_svc', ftr_reg_svc)
    # ftr_match_road = match_road_busstop(list_line_, 'road')
    # write_file(path_write, 'ftr_reg_match_road', ftr_match_road)
    # ftr_match_busstop = match_road_busstop(list_line_, command='busstop')
    # write_file(path_write, 'ftr_reg_match_busstop', ftr_match_busstop)

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

    ######################################################################################################
    ######################################################################################################
    # SGFORUMS
    # sql = load_sql(command='sgforums')
    # list_row = table_SQL(sql)
    # list_line = filtering_text_demo(list_row, 'sgforums')  # remmeber that we only remove links in Twitter
    # print len(list_line)
    #
    # list_line_ = list_line
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/sgforums/crf_features'

    # -------------- loading all token features type
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
    # ftr_reg_svc = reg_bussvc(list_line_, n_token=5, command='sgforums')
    # write_file(path_write, 'ftr_reg_svc', ftr_reg_svc)
    # ftr_match_road = match_road_busstop(list_line_, 'road')
    # write_file(path_write, 'ftr_reg_match_road', ftr_match_road)
    # ftr_match_busstop = match_road_busstop(list_line_, command='busstop')
    # write_file(path_write, 'ftr_reg_match_busstop', ftr_match_busstop)

    # -------------- loading all token before and after match dictionary
    # command = ['svc', 'road', 'busstop']
    # for value in command:
    #     list_command = token_bef_matchDict(list_line_, value)
    #     write_file(path_write, 'ftr_tok_bef_match_' + value, list_command)
    #
    # for value in command:
    #     list_command = token_aft_matchDict(list_line_, value)
    #     write_file(path_write, 'ftr_tok_aft_match_' + value, list_command)
    #
    # # -------------- loading all token type before and after labeling
    # types = ['Capitalized', 'Digit', 'Character', 'BusPlate']
    # for value in types:
    #     list_command = token_bef_type(list_line_, value)
    #     write_file(path_write, 'ftr_tok_bef_is' + value, list_command)
    #
    # for value in types:
    #     list_command = token_aft_type(list_line_, value)
    #     write_file(path_write, 'ftr_tok_aft_is' + value, list_command)
    #
    # # -------------- create list of features using actual word for token before in road and bus stop
    # # use for road and bus stop
    # command = ['road', 'busstop']
    # for value in command:
    #     dict_ = load_dict_token_bef_aft(value)
    #     ftr_token_bef_road_busstop(path_write, 'ftr_token_bef_' + value, list_line_, dict_)
    #
    # command = ['bef_svc', 'aft_svc']
    # for value in command:
    #     dict_ = load_dict_token_bef_aft(value)
    #     ftr_token_bef_aft_svc(value, path_write, 'ftr_token_' + value, list_line_, dict_)

    ######################################################################################################
    ######################################################################################################
    # FACEBOOK
    sql = load_sql(command='facebook')
    list_row = table_SQL(sql)
    list_line = filtering_text_demo(list_row, 'facebook')  # remmeber that we remove links in Twitter
    print len(list_line)

    list_line_ = list_line
    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/facebook/crf_features'

    # -------------- loading all token features type
    # ftr_isDigit = isAllDigit(list_line_)
    # write_file(path_write, 'ftr_isDigit', ftr_isDigit)
    # ftr_isCharacter = isAllCharacter(list_line_)
    # write_file(path_write, 'ftr_isCharacter', ftr_isCharacter)
    # ftr_isBusPlate = is_busPlate(list_line_)
    # write_file(path_write, 'ftr_isBusPlate', ftr_isBusPlate)
    # ftr_isCapitalized = isCapitalize(list_line_)
    # write_file(path_write, 'ftr_isCapitalized', ftr_isCapitalized)

    # -------------- loading all tokens match dictionary, note that we need bus stop code in Facebook
    # note that the dictionary is the same in different datasets: SGFORUMS, TWITTER, FACEBOOK
    # ftr_match_dict_svc = match_dict(list_line_, command='svc')
    # write_file(path_write, 'ftr_match_dict_svc', ftr_match_dict_svc)
    # ftr_match_dict_road = match_dict(list_line_, command='road')
    # write_file(path_write, 'ftr_match_dict_road', ftr_match_dict_road)
    # ftr_match_dict_busstop = match_dict(list_line_, command='busstop')
    # write_file(path_write, 'ftr_match_dict_busstop', ftr_match_dict_busstop)
    #
    # # # add bus stop code
    # ftr_match_dict_busstopCode = match_dict(list_line_, command='busstopCode')
    # write_file(path_write, 'ftr_match_dict_busstopCode', ftr_match_dict_busstopCode)

    # -------------- loading all tokens match bus service, road and bus stop using regular expression
    # note that the regular expression is the same in different datasets: SGFORUMS, TWITTER, FACEBOOK
    # ftr_reg_svc = reg_bussvc(list_line_, n_token=10, command='facebook')  # for the facebook, if token > 3, return False
    # write_file(path_write, 'ftr_reg_svc', ftr_reg_svc)
    # ftr_match_road = match_road_busstop(list_line_, command='road')
    # write_file(path_write, 'ftr_reg_match_road', ftr_match_road)
    # ftr_match_busstop = match_road_busstop(list_line_, command='busstop')
    # write_file(path_write, 'ftr_reg_match_busstop', ftr_match_busstop)

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
    #
    # # -------------- loading all token type before and after labeling
    # types = ['Capitalized', 'Digit', 'Character', 'BusPlate']
    # for value in types:
    #     list_command = token_bef_type(list_line_, value)
    #     write_file(path_write, 'ftr_tok_bef_is' + value, list_command)
    #
    # for value in types:
    #     list_command = token_aft_type(list_line_, value)
    #     write_file(path_write, 'ftr_tok_aft_is' + value, list_command)
    #
    # # -------------- create list of features using actual word for token before in road and bus stop
    # # use for road and bus stop
    # command = ['road', 'busstop']
    # for value in command:
    #     dict_ = load_dict_token_bef_aft_Facebook(value)
    #     ftr_token_bef_road_busstop(path_write, 'ftr_token_bef_' + value, list_line_, dict_)
    #
    # command = ['bef_svc', 'aft_svc']
    # for value in command:
    #     dict_ = load_dict_token_bef_aft_Facebook(value)
    #     ftr_token_bef_aft_svc(value, path_write, 'ftr_token_' + value, list_line_, dict_)
