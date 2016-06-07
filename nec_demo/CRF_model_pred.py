__author__ = 'vdthoang'
from CRF_labeling.feature_crf_all import folder_files
from main.loadFile import load_file
import numpy as np
from CRF_labeling.filterText_CRF import filterTxt_CRF
from CRF_labeling.CRF_clf import featuers_CRF
from nec_demo.filterText_demo import load_sql, table_SQL
from CRF_labeling.filterText_CRF import filter_eachToken, filter_eachTok_rmLinks
from CRF_labeling.feature_crf import construct_ftr_CRF, load_target_label
from CRF_labeling.feature_crf import n_cross_valid_crf
from pystruct.models import ChainCRF
from pystruct.learners import FrankWolfeSSVM
from main.writeFile import write_file


def filterText_demo(list_line, command, command_data):
    list_convert = list()
    for i in range(0, len(list_line)):
        text = ''
        split_text = list_line[i].strip().split()
        for token_ in split_text:

            if command == 'removePunc':  # remove all punctuations
                token_filter = filter_eachToken(token_, command_data)
            elif command == 'removeLink':  # remove all punctuations and links in token
                token_filter = filter_eachTok_rmLinks(token_, command_data)
            else:
                print 'You need to give the correct command'
                quit()

            if len(token_filter) != 0:
                text += token_filter + '\t'

        list_convert.append(text.strip())
    return list_convert


def load_demo_text(command):
    sql = load_sql(command)
    list_row = table_SQL(sql)
    return list_row


def load_predLabel(command):
    if command == 'twitter':
        path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/twitter'
        name = 'pred_label_twitter.csv'
        list_pred = load_file(path, name)
    elif command == 'sgforums':
        path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/sgforums'
        name = 'pred_label_sgforums.csv'
        list_pred = load_file(path, name)
    elif command == 'facebook':
        path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/facebook'
        name = 'pred_label_facebook.csv'
        list_pred = load_file(path, name)

    return list_pred


def load_demo_ftr(command):
    if command == 'twitter':
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/twitter/crf_features'
    elif command == 'sgforums':
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/sgforums/crf_features'
    elif command == 'facebook':
        path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/facebook/crf_features'

    files_ = folder_files(path_ftr)
    features = featuers_CRF(files_, path_ftr)
    X = np.array(construct_ftr_CRF(features))
    return X


def CRF_pred_label(X, Y, command):
    texts = load_demo_text(command)
    if command == 'twitter':
        convert_texts = filterText_demo(texts, 'removeLink', command)
        X_ftr = load_demo_ftr(command)
        print len(convert_texts), len(X_ftr)
        path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/twitter'
        name_write = 'pred_label_' + command

    elif command == 'sgforums':
        convert_texts = filterText_demo(texts, 'removePunc', command)
        X_ftr = load_demo_ftr(command)
        print len(convert_texts), len(X_ftr)
        path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/sgforums'
        name_write = 'pred_label_' + command

    elif command == 'facebook':
        convert_texts = filterText_demo(texts, 'removeLink', command)
        X_ftr = load_demo_ftr(command)
        print len(convert_texts), len(X_ftr)
        path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/facebook'
        name_write = 'pred_label_' + command

    crf = ChainCRF(inference_method='max-product', directed=False, class_weight=None)
    ssvm = FrankWolfeSSVM(model=crf, C=1.0, max_iter=100)
    ssvm.fit(X, Y)
    y_pred = ssvm.predict(X_ftr)

    list_write = list()
    for line in y_pred:
        labels = ''
        for label in line:
            labels += str(label) + '\t'
        list_write.append(labels.strip())

    write_file(path_write, name_write, list_write)


##############################################################################################################
##############################################################################################################
def check_tokenize_pred(command):
    # check whether our tokenizes are correct
    if command == 'twitter':
        texts = load_demo_text(command)
        convert_texts = filterText_demo(texts, 'removeLink', command)
        list_pred = load_predLabel('twitter')

        for index in range(0, len(list_pred)):
            text, label = convert_texts[index], list_pred[index]
            split_text, split_label = text.split(), label.split('\t')

            if len(split_text) != len(split_label):
                print index
            # else:
            #     print len(split_text), len(split_label)
    elif command == 'sgforums':
        texts = load_demo_text(command)
        convert_texts = filterText_demo(texts, 'removePunc', command)
        list_pred = load_predLabel(command)

        for index in range(0, len(list_pred)):
            text, label = convert_texts[index], list_pred[index]
            split_text, split_label = text.split(), label.split('\t')

            if len(split_text) != len(split_label):
                print index
    elif command == 'facebook':
        texts = load_demo_text(command)
        convert_texts = filterText_demo(texts, 'removeLink', command)
        list_pred = load_predLabel(command)

        for index in range(0, len(list_pred)):
            text, label = convert_texts[index], list_pred[index]
            split_text, split_label = text.split(), label.split('\t')

            if len(split_text) != len(split_label):
                print index


def check_token(token, command):
    if command == 'twitter':
        text = filter_eachTok_rmLinks(token, command)
        if len(text.strip()) == 0:
            return True
        else:
            return False
    if command == 'sgforums':
        text = filter_eachToken(token, command)
        if len(text.strip()) == 0:
            return True
        else:
            return False
    if command == 'facebook':
        text = filter_eachTok_rmLinks(token, command)
        if len(text.strip()) == 0:
            return True
        else:
            return False


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def originial_token(path, name, original_texts, filtering_texts, labels, command):
    texts_correct, labels_correct = list(), list()
    for index in range(0, len(original_texts)):
        text_org, text_fil, label = original_texts[index], filtering_texts[index], labels[index]
        split_textOrg, split_textFil, split_textLabel = text_org.split(), text_fil.split('\t'), label.split('\t')

        k = 0  # index of text labels
        line_correct, label_correct = '', ''
        for j in range(0, len(split_textOrg)):
            flag = check_token(split_textOrg[j], command)
            if flag is True:
                line_correct += split_textOrg[j] + ' '
                label_correct += '0 '
            else:
                line_correct += split_textOrg[j] + ' '
                if split_textLabel[k] == '1':
                    flag_int = RepresentsInt(filter_eachToken(split_textOrg[j], command))
                    if flag_int is True:
                        label_correct += split_textLabel[k] + ' '
                    else:
                        label_correct += '0 '
                else:
                    label_correct += split_textLabel[k] + ' '
                k += 1
        texts_correct.append(line_correct.strip()), labels_correct.append(label_correct.strip())

    list_write = list()
    for i in range(0, len(texts_correct)):
        list_write.append(texts_correct[i])
        list_write.append(labels_correct[i])
        # list_write.append('\n')

    write_file(path, name + '_' + command, list_write)


def convert_token_label(path, name, command):
    # return to the original texts
    if command == 'twitter':
        texts = load_demo_text(command)
        convert_texts = filterText_demo(texts, 'removeLink', command)
        list_pred = load_predLabel('twitter')
        originial_token(path, name, texts, convert_texts, list_pred, command)

    elif command == 'sgforums':
        texts = load_demo_text(command)
        convert_texts = filterText_demo(texts, 'removePunc', command)
        list_pred = load_predLabel('sgforums')
        originial_token(path, name, texts, convert_texts, list_pred, command)

    elif command == 'facebook':
        texts = load_demo_text(command)
        convert_texts = filterText_demo(texts, 'removeLink', command)
        list_pred = load_predLabel('facebook')
        originial_token(path, name, texts, convert_texts, list_pred, command)


if __name__ == '__main__':
    ###############################################################################################################
    ###############################################################################################################
    # TWITTER
    # loading CRF features, remember that we only remove all punctuation and links in Twitter
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features/features_rmLink'
    # files_ = folder_files(path_ftr)
    # features = featuers_CRF(files_, path_ftr)
    # X = np.array(construct_ftr_CRF(features))  # construct the features for CRF
    # print X.shape
    # print 'Finish loading features for CRF'
    #
    # # loading target labels
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    # name_ = 'labeling_all.txt'
    # list_line_ = filterTxt_CRF(load_file(path_, name_), 'removeLink', 'model')
    # Y = np.array(load_target_label(list_line_))
    # print Y.shape
    #
    # print 'Loading the target labels ------------------------------------'
    # # n_cross_valid_crf(X, Y, K=2, command='metrics_F1')  # use to calculate the F1 for classification
    # CRF_pred_label(X, Y, command='twitter')

    # After finishing getting the predicted label, running to check the tokenizer
    # check_tokenize_pred('twitter')

    # AFter checking, now we assign the labels for the original texts
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/twitter'
    # name = 'original_pred_label'
    # convert_token_label(path, name, 'twitter')

    ###############################################################################################################
    ###############################################################################################################
    # SGFORUMS
    # loading CRF features, remember that we only remove all punctuation and links in Sgforums
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features/features'
    # files_ = folder_files(path_ftr)
    # features = featuers_CRF(files_, path_ftr)
    # X = np.array(construct_ftr_CRF(features))  # construct the features for CRF
    # print X.shape
    # print 'Finish loading features for CRF'
    #
    # # loading target labels
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    # name_ = 'Label_all_crf.txt'
    # list_line_ = load_file(path_, name_)
    # Y = np.array(load_target_label(list_line_))
    # print Y.shape
    #
    # print 'Loading the target labels ------------------------------------'
    # # # n_cross_valid_crf(X, Y, K=2, command='metrics_F1')  # use to calculate the F1 for classification
    # CRF_pred_label(X, Y, command='sgforums')

    # After finishing getting the predicted label, running to check the tokenizer
    # check_tokenize_pred('sgforums')

    # AFter checking, now we assign the labels for the original texts
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/sgforums'
    # name = 'original_pred_label'
    # convert_token_label(path, name, 'sgforums')

    ###############################################################################################################
    ###############################################################################################################
    # FACEBOOK
    # # loading CRF features
    # path_ftr = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF/crf_features/features'
    # files_ = folder_files(path_ftr)
    # features = featuers_CRF(files_, path_ftr)
    # X = np.array(construct_ftr_CRF(features))  # construct the features for CRF
    # print 'Finish loading features for CRF'
    # #
    # # # loading target labels
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF'
    # name_ = 'label.txt'
    # list_line_ = filterTxt_CRF(load_file(path_, name_), command='removePunc', command_data='facebook')
    # Y = np.array(load_target_label(list_line_))
    # print 'Finish loading target label'
    # #
    # # # running CRF models
    # # n_cross_valid_crf(X, Y, K=2, command='metrics_F1')  # use to calculate the F1 for classification
    # CRF_pred_label(X, Y, command='facebook')

    # After finishing getting the predicted label, running to check the tokenizer
    # check_tokenize_pred('facebook')
    # after running this file, running file clean_pred_label.py in nec_demo

    # AFter checking, now we assign the labels for the original texts
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/facebook'
    name = 'original_pred_label'
    convert_token_label(path, name, 'facebook')
