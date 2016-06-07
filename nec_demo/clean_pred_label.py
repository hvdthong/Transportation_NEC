__author__ = 'vdthoang'
from main.loadFile import load_file
from main.writeFile import write_file


def convert_CRF_pred(path_write, name_write, list_pred):
    list_write = list()

    for j in range(0, len(list_pred)):
        # if j == 6:
        #     print 'hello'
        label = list_pred[j]
        convert_label = ''
        split_label = label.split('\t')
        for i in range(0, len(split_label)):
            token = split_label[i]
            if len(split_label) > 1:
                if i == 0:
                    if (token == '2') or (token == '3'):
                        next_token = split_label[i + 1]
                        if (next_token == '0') or (next_token == '1'):
                            convert_label += '0' + '\t'
                        else:
                            convert_label += token + '\t'
                    else:
                        convert_label += token + '\t'
                else:
                    if i == (len(split_label) - 1):
                        if (token == '2') or (token == '3'):
                            prev_token = split_label[i - 1]
                            if (prev_token == '0') or (prev_token == '1'):
                                convert_label += '0' + '\t'
                            else:
                                convert_label += token + '\t'
                        else:
                            convert_label += token + '\t'

                    else:
                        if (token == '2') or (token == '3'):
                            prev_token, next_token = split_label[i - 1], split_label[i + 1]
                            if ((prev_token == '0') or (prev_token == '1')) \
                                    and ((next_token == '0') or (next_token == '1')):
                                convert_label += '0' + '\t'
                            else:
                                convert_label += token + '\t'
                        else:
                            convert_label += token + '\t'
            else:
                convert_label += '0' + '\t'
        list_write.append(convert_label.strip())

    write_file(path_write, name_write, list_write)

if __name__ == '__main__':
    # USING FOR SGFORUMS
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/sgforums'
    # name = 'pred_label_sgforums.csv'
    # name_write = 'pred_label_sgforums_convert'
    # list_pred = load_file(path, name)
    # convert_CRF_pred(path, name_write, list_pred)

    # USING FOR FACEBOOK
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/facebook'
    name = 'pred_label_facebook.csv'
    name_write = 'pred_label_facebook_convert'
    list_pred = load_file(path, name)
    convert_CRF_pred(path, name_write, list_pred)
