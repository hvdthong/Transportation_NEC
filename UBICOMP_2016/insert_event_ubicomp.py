__author__ = 'vdthoang'
from main.loadFile import load_file
from main.writeFile import write_file


if __name__ == '__main__':
    path = 'C:/Users/vdthoang/Google Drive/LARC - NEC Project/ubicomp2016_paper/data'
    events = ['accident', 'crowd', 'missing', 'skip', 'slow', 'wait']
    list_all = list()
    for event in events:
        list_ = load_file(path, 'twitter_event_' + event + '.csv')
        list_all.append(list_)

    length = len(list_all[0])
    list_new = list()
    for i in range(0, length):
        for j in range(0, len(list_all)):
            j_dex = list_all[j]
            split_ = j_dex[i].split('\t')
            id_, label = split_[0], split_[1]
            new_label = ''
            if j == 0 and int(label) == 1:
                new_label = 'accident'
            elif j == 1 and int(label) == 1:
                new_label = 'crowd'
            elif j == 2 and int(label) == 1:
                new_label = 'missing'
            elif j == 3 and int(label) == 1:
                new_label = 'skip'
            elif j == 4 and int(label) == 1:
                new_label = 'slow'
            elif j == 5 and int(label) == 1:
                new_label = 'wait'

            if new_label != '':
                list_new.append(id_ + '\t' + new_label)
                print id_ + '\t' + new_label
    write_file(path, 'twitter_event', list_new)
    print len(list_new)
