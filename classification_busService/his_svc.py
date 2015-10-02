__author__ = 'vdthoang'
from main.loadFile import load_file


if __name__ == '__main__':
    path = 'D:/'
    # name = 'notcorrect_clf.txt'
    name = 'notcorrect_RE.txt'
    list_ = load_file(path, name)

    cnt_1 = 0
    cnt_2 = 0
    cnt_3 = 0

    for value in list_:
        print value, len(value)

        if len(value) == 1:
            cnt_1 += 1
        if len(value) == 2:
            cnt_2 += 1
        if len(value) == 3:
            cnt_3 += 1

    print cnt_1, cnt_2, cnt_3