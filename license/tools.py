__author__ = 'vdthoang'
from main.loadFile import load_file
from main.writeFile import write_file


def distinct_list(list_, path, name):
    new_list = list()
    for value in list_:
        if value not in new_list:
            new_list.append(value)
    print len(new_list)
    write_file(path, name.replace('.txt', '') + '_new', new_list)


if __name__ == '__main__':
    # path = 'D:/PYTHON_CODE/license_crf/bus_dictionary'
    # name = 'dict_busstop.txt'
    # path = 'D:/PYTHON_CODE/license_crf/bus_dictionary'
    # name = 'dict_busstopCode.txt'
    # path = 'D:/PYTHON_CODE/license_crf/bus_dictionary'
    # name = 'dict_bussvc.txt'
    path = 'D:/PYTHON_CODE/license_crf/bus_dictionary'
    name = 'dict_road.txt'

    list_ = load_file(path, name)
    print len(list_)
    distinct_list(list_, path, name)