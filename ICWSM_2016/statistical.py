__author__ = 'vdthoang'
from main.loadFile import load_file


def num_statis(event, list_):
    if event == 'crowd':
        value = list_[1]
    elif event == 'slow':
        value = list_[5]
    elif event == 'missing':
        value = list_[9]
    elif event == 'wait':
        value = list_[13]
    elif event == 'skip':
        value = list_[17]

    split_value = value.split(',')
    for num in split_value:
        print num


if __name__ == '__main__':
    path = 'D:'
    name = 'GeoDistances.txt'

    list_ = load_file(path, name)
    # for value in list_:
    #     print value

    # num_statis('crowd', list_)
    # num_statis('slow', list_)
    # num_statis('missing', list_)
    # num_statis('wait', list_)
    num_statis('skip', list_)