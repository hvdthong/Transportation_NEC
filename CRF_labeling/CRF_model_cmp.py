__author__ = 'vdthoang'
from main.writeFile import write_file
from main.loadFile import load_file
from CRF_labeling.feature_crf_all import isAllDigit, isAllCharacter, is_busPlate, \
    token_bef_matchDict, token_aft_matchDict, token_bef_type, token_aft_type, \
    load_dict_token_bef_aft, ftr_token_bef_road_busstop, ftr_token_bef_aft_svc, \
    load_dict_token_bef_aft_Twitter, load_dict_token_bef_aft_Facebook
from CRF_clf import featuers_CRF
from CRF_labeling.feature_crf_all import folder_files
from feature_crf import construct_ftr_CRF, load_target_label\
    , metrics_crf, confusion_matrix_CRF, match_dict, reg_bussvc, \
    isCapitalize, match_road_busstop

from CRF_labeling.filterText_CRF import filterTxt_CRF
import numpy as np
from pystruct.models import ChainCRF
from pystruct.learners import FrankWolfeSSVM


def create_ftrList(path_write, command):
    if command == 'twitter_vs_sgforums' or command == 'facebook_vs_sgforums':
        path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
        name_ = 'Label_all_crf.txt'
        list_line_ = load_file(path_, name_)
    elif command == 'sgforums_vs_twitter' or command == 'facebook_vs_twitter':
        path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
        name_ = 'labeling_all.txt'
        list_line_ = filterTxt_CRF(load_file(path_, name_), command='removeLink')
    elif command == 'twitter_vs_facebook' or command == 'sgforums_vs_facebook':
        path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF'
        name_ = 'label.txt'
        list_line_ = filterTxt_CRF(load_file(path_, name_), command='removePunc')
    else:
        print 'Need to give the correct command'
        quit()

    # -------------- loading all tokens features type
    ftr_isDigit = isAllDigit(list_line_)
    write_file(path_write, 'ftr_isDigit', ftr_isDigit)
    ftr_isCharacter = isAllCharacter(list_line_)
    write_file(path_write, 'ftr_isCharacter', ftr_isCharacter)
    ftr_isBusPlate = is_busPlate(list_line_)
    write_file(path_write, 'ftr_isBusPlate', ftr_isBusPlate)
    ftr_isCapitalized = isCapitalize(list_line_)
    write_file(path_write, 'ftr_isCapitalized', ftr_isCapitalized)

    # -------------- loading all tokens match dictionary
    # note that the dictionary is the same in different datasets: SGFORUMS, TWITTER, FACEBOOK
    ftr_match_dict_svc = match_dict(list_line_, command='svc')
    write_file(path_write, 'ftr_match_dict_svc', ftr_match_dict_svc)
    ftr_match_dict_road = match_dict(list_line_, command='road')
    write_file(path_write, 'ftr_match_dict_road', ftr_match_dict_road)
    ftr_match_dict_busstop = match_dict(list_line_, command='busstop')
    write_file(path_write, 'ftr_match_dict_busstop', ftr_match_dict_busstop)

    if command == 'facebook_vs_sgforums' or command == 'facebook_vs_twitter':
        ftr_match_dict_busstopCode = match_dict(list_line_, command='busstopCode')
        write_file(path_write, 'ftr_match_dict_busstopCode', ftr_match_dict_busstopCode)

    # -------------- loading all tokens match bus service, road and bus stop using regular expression
    # note that the regular expression is the same in different datasets: SGFORUMS, TWITTER, FACEBOOK
    ftr_reg_svc = reg_bussvc(list_line_, n_token=10)
    write_file(path_write, 'ftr_reg_svc', ftr_reg_svc)
    ftr_match_road = match_road_busstop(list_line_, command='road')
    write_file(path_write, 'ftr_reg_match_road', ftr_match_road)
    ftr_match_busstop = match_road_busstop(list_line_, command='busstop')
    write_file(path_write, 'ftr_reg_match_busstop', ftr_match_busstop)

    # -------------- loading all token before and after match dictionary
    # note that the dictionary is the same in different datasets: SGFORUMS, TWITTER, FACEBOOK
    types = ['svc', 'road', 'busstop']
    for value in types:
        list_command = token_bef_matchDict(list_line_, value)
        write_file(path_write, 'ftr_tok_bef_match_' + value, list_command)

    for value in types:
        list_command = token_aft_matchDict(list_line_, value)
        write_file(path_write, 'ftr_tok_aft_match_' + value, list_command)

    # -------------- loading all token type before and after labeling
    types = ['Capitalized', 'Digit', 'Character', 'BusPlate']
    for value in types:
        list_command = token_bef_type(list_line_, value)
        write_file(path_write, 'ftr_tok_bef_is' + value, list_command)

    for value in types:
        list_command = token_aft_type(list_line_, value)
        write_file(path_write, 'ftr_tok_aft_is' + value, list_command)

    if command == 'twitter_vs_sgforums' or command == 'twitter_vs_facebook':
        # -------------- create list of features using actual word for token before in road and bus stop
        # use for road and bus stop
        types = ['road', 'busstop']
        for value in types:
            dict_ = load_dict_token_bef_aft_Twitter(value)
            ftr_token_bef_road_busstop(path_write, 'ftr_token_bef_' + value, list_line_, dict_)

        types = ['bef_svc', 'aft_svc']
        for value in types:
            dict_ = load_dict_token_bef_aft_Twitter(value)
            ftr_token_bef_aft_svc(value, path_write, 'ftr_token_' + value, list_line_, dict_)

    elif command == 'sgforums_vs_twitter' or command == 'sgforums_vs_facebook':
        # -------------- create list of features using actual word for token before in road and bus stop
        # use for road and bus stop
        types = ['road', 'busstop']
        for value in types:
            dict_ = load_dict_token_bef_aft(value)
            ftr_token_bef_road_busstop(path_write, 'ftr_token_bef_' + value, list_line_, dict_)

        types = ['bef_svc', 'aft_svc']
        for value in types:
            dict_ = load_dict_token_bef_aft(value)
            ftr_token_bef_aft_svc(value, path_write, 'ftr_token_' + value, list_line_, dict_)

    elif command == 'facebook_vs_twitter' or command == 'facebook_vs_sgforums':
        # -------------- create list of features using actual word for token before in road and bus stop
        # use for road and bus stop
        types = ['road', 'busstop']
        for value in types:
            dict_ = load_dict_token_bef_aft_Facebook(value)
            ftr_token_bef_road_busstop(path_write, 'ftr_token_bef_' + value, list_line_, dict_)

        types = ['bef_svc', 'aft_svc']
        for value in types:
            dict_ = load_dict_token_bef_aft_Facebook(value)
            ftr_token_bef_aft_svc(value, path_write, 'ftr_token_' + value, list_line_, dict_)


def loading_ftr_CRFs(command):
    ##############################################################################
    if command == 'twitter_vs_sgforums_twitter_training':
        # loading CRF features for training
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLink'

    elif command == 'twitter_vs_sgforums_sgforums_testing':
        # loading CRF features for testing
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/CRFs_compareModel/sgforums/ftr_twitter'

    ##############################################################################
    if command == 'twitter_vs_facebook_twitter_training':
        # loading CRF features for training
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLink'

    elif command == 'twitter_vs_facebook_facebook_testing':
        # loading CRF features for testing
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/CRFs_compareModel/facebook/ftr_twitter'

    ##############################################################################
    elif command == 'sgforums_vs_twitter_sgforums_training':
        # features for training
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features/features'

    elif command == 'sgforums_vs_twitter_twitter_testing':
        # features for testing
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/CRFs_compareModel/twitter/ftr_sgforums'

    ##############################################################################
    elif command == 'sgforums_vs_facebook_sgforums_training':
        # features for training
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features/features'

    elif command == 'sgforums_vs_facebook_facebook_testing':
        # features for testing
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/CRFs_compareModel/facebook/ftr_sgforums'

    ##############################################################################
    elif command == 'facebook_vs_twitter_facebook_training':
        # features for training
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF/crf_features/features'

    elif command == 'facebook_vs_twitter_twitter_testing':
        # features for testing
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/CRFs_compareModel/twitter/ftr_facebook'

    ##############################################################################
    elif command == 'facebook_vs_sgforums_facebook_training':
        # features for training
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF/crf_features/features'

    elif command == 'facebook_vs_sgforums_sgforums_testing':
        # features for testing
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/CRFs_compareModel/sgforums/ftr_facebook'

    files_ = folder_files(path_ftr)
    features = featuers_CRF(files_, path_ftr)
    X = np.array(construct_ftr_CRF(features))  # construct the features for CRF
    print 'Finish loading features for CRF ' + command
    return X


def loading_target_CRFs(command):
    if command == 'twitter':
        # loading target labels
        path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
        name_ = 'labeling_all.txt'
        list_line_ = filterTxt_CRF(load_file(path_, name_), command='removeLink')

    elif command == 'sgforums':
        # loading target labels
        path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
        name_ = 'Label_all_crf.txt'
        list_line_ = load_file(path_, name_)

    elif command == 'facebook':
        # loading target labels
        path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF'
        name_ = 'label.txt'
        list_line_ = filterTxt_CRF(load_file(path_, name_), command='removePunc')

    Y = np.array(load_target_label(list_line_))
    print 'Finish loading target label ' + command
    return Y


def create_model_CRFs(command, results):
    ################################################################################################
    if command == 'twitter_vs_sgforums':
        X_training, Y_training = loading_ftr_CRFs('twitter_vs_sgforums_twitter_training'), loading_target_CRFs('twitter')
        X_testing, Y_testing = loading_ftr_CRFs('twitter_vs_sgforums_sgforums_testing'), loading_target_CRFs('sgforums')
        print len(X_training), len(Y_training)
        print len(X_testing), len(Y_testing)

    elif command == 'twitter_vs_facebook':
        X_training, Y_training = loading_ftr_CRFs('twitter_vs_facebook_twitter_training'), loading_target_CRFs('twitter')
        X_testing, Y_testing = loading_ftr_CRFs('twitter_vs_facebook_facebook_testing'), loading_target_CRFs('facebook')
        print len(X_training), len(Y_training)
        print len(X_testing), len(Y_testing)

    ################################################################################################
    elif command == 'sgforums_vs_twitter':
        X_training, Y_training = loading_ftr_CRFs('sgforums_vs_twitter_sgforums_training'), loading_target_CRFs('sgforums')
        X_testing, Y_testing = loading_ftr_CRFs('sgforums_vs_twitter_twitter_testing'), loading_target_CRFs('twitter')
        print len(X_training), len(Y_training)
        print len(X_testing), len(Y_testing)

    elif command == 'sgforums_vs_facebook':
        X_training, Y_training = loading_ftr_CRFs('sgforums_vs_facebook_sgforums_training'), loading_target_CRFs('sgforums')
        X_testing, Y_testing = loading_ftr_CRFs('sgforums_vs_facebook_facebook_testing'), loading_target_CRFs('facebook')
        print len(X_training), len(Y_training)
        print len(X_testing), len(Y_testing)

    ################################################################################################
    elif command == 'facebook_vs_twitter':
        X_training, Y_training = loading_ftr_CRFs('facebook_vs_twitter_facebook_training'), loading_target_CRFs('facebook')
        X_testing, Y_testing = loading_ftr_CRFs('facebook_vs_twitter_twitter_testing'), loading_target_CRFs('twitter')
        print len(X_training), len(Y_training)
        print len(X_testing), len(Y_testing)

    elif command == 'facebook_vs_sgforums':
        X_training, Y_training = loading_ftr_CRFs('facebook_vs_sgforums_facebook_training'), loading_target_CRFs('facebook')
        X_testing, Y_testing = loading_ftr_CRFs('facebook_vs_sgforums_sgforums_testing'), loading_target_CRFs('sgforums')
        print len(X_training), len(Y_training)
        print len(X_testing), len(Y_testing)

    results_CRFs(X_training, Y_training, X_testing, Y_testing, results)


############################################################################
############################################################################
def write_CRFs_compare(y_test, y_pred):
    list_write = list()
    for i in range(0, len(y_test)):
        list_ = list()
        pred, test = y_pred[i], y_test[i]
        list_.append(pred)
        list_.append(test)
        list_write.append(list_)
    return list_write


def results_CRFs(X_training, Y_training, X_testing, Y_testing, command):
    crf = ChainCRF(inference_method='max-product', directed=False, class_weight=None)
    ssvm = FrankWolfeSSVM(model=crf, C=1.0, max_iter=100)
    ssvm.fit(X_training, Y_training)
    y_pred = ssvm.predict(X_testing)

    list_write = list()
    print 'Accuracy of linear-crf %f:' % ssvm.score(X_testing, Y_testing)
    if command == 'metrics_F1':
        metrics_crf(Y_testing, y_pred)
    elif command == 'confusion_matrix':
        confusion_matrix_CRF(Y_testing, y_pred)
    elif command == 'write_results':
        list_write = write_CRFs_compare(Y_testing, y_pred)
        for value in list_write:
            pred_list = value[0]
            test_list = value[1]

            for i in range(0, len(pred_list)):
                print str(pred_list[i]) + '\t' + str(test_list[i])


if __name__ == '__main__':
    # use to compare the different between different models
    ############################################################################
    ############################################################################
    # TWITTER VS. SGFORUMS
    # create model for Twitter data and use it in Sgforums

    ############################################################################
    # first we need to construct features for Sgforums based on Twitter information
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/CRFs_compareModel/sgforums/ftr_twitter'
    # create_ftrList(path_write, command='twitter_vs_sgforums')

    ############################################################################
    # load Twitter data and create CRFs model
    # create_model_CRFs(command='twitter_vs_sgforums', results='metrics_F1')
    # create_model_CRFs(command='twitter_vs_sgforums', results='confusion_matrix')
    # create_model_CRFs(command='twitter_vs_sgforums', results='write_results')

    ############################################################################
    ############################################################################
    # TWITTER VS. FACEBOOK
    # create model for Twitter data and use it in Facebook

    ############################################################################
    # first we need to construct features for Facebook based on Twitter information
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/CRFs_compareModel/facebook/ftr_twitter'
    # create_ftrList(path_write, command='twitter_vs_facebook')

    ############################################################################
    # load Twitter data and create CRFs model
    # create_model_CRFs(command='twitter_vs_facebook', results='metrics_F1')
    # create_model_CRFs(command='twitter_vs_facebook', results='confusion_matrix')
    # create_model_CRFs(command='twitter_vs_facebook', results='write_results')

    ############################################################################
    ############################################################################
    # SGFORUMS VS. TWITTER
    # create model for Sgforums data and use it in Twitter
    ###########################################################################
    # first we need to construct features for Twitter based on Sgforums information
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/CRFs_compareModel/twitter/ftr_sgforums'
    # create_ftrList(path_write, command='sgforums_vs_twitter')

    ############################################################################
    # load Twitter data and create CRFs model
    # create_model_CRFs(command='sgforums_vs_twitter', results='metrics_F1')

    ############################################################################
    ############################################################################
    # SGFORUMS VS. FACEBOOK
    # create model for Sgforums data and use it in Facebook
    ###########################################################################
    # first we need to construct features for Twitter based on Sgforums information
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/CRFs_compareModel/facebook/ftr_sgforums'
    # create_ftrList(path_write, command='sgforums_vs_facebook')

    ############################################################################
    # load Twitter data and create CRFs model
    # create_model_CRFs(command='sgforums_vs_facebook', results='metrics_F1')

    ############################################################################
    ############################################################################
    # FACEBOOK VS. TWITTER
    # create model for Facebook data and use it in Twitter

    ############################################################################
    # first we need to construct features for Twitter based on Facebook information
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/CRFs_compareModel/twitter/ftr_facebook'
    # create_ftrList(path_write, command='facebook_vs_twitter')

    ############################################################################
    # load Twitter data and create CRFs model
    # create_model_CRFs(command='facebook_vs_twitter', results='metrics_F1')

    ############################################################################
    ############################################################################
    # FACEBOOK VS. SGFORUMS
    # create model for Facebook data and apply it on Sgforums

    ############################################################################
    # first we need to construct features for Twitter based on Facebook information
    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/CRFs_compareModel/sgforums/ftr_facebook'
    # create_ftrList(path_write, command='facebook_vs_sgforums')

    ############################################################################
    # load Twitter data and create CRFs model
    create_model_CRFs(command='facebook_vs_sgforums', results='metrics_F1')
