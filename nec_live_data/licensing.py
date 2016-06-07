__author__ = 'vdthoang'
from main.loadFile import load_file
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS


def remove_stopWord_list(data):
    list_new = list()
    for word in data:
        if word.lower() not in ENGLISH_STOP_WORDS:
            list_new.append(word)
    return list_new


def check_value(value):
    if value >= 2:
        return True

if __name__ == '__main__':
    path = 'D:/PYTHON_CODE/license_crf/training_data/before_after'
    names = ['facebook_aft_bussvc', 'facebook_bef_busstop', 'facebook_bef_bussvc', 'facebook_bef_road']

    for name in names:
        list_load = remove_stopWord_list(load_file(path, name + '.csv'))
        print len(list_load)

    list_ = [1, 2, 3, 4, 5, 6]
    list_value = [check_value(x) for x in list_]
    print list_value