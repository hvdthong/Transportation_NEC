__author__ = 'vdthoang'

from main.loadFile import load_file
from main.writeFile import write_file
if __name__ == '__main__':
    # sgforums
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    # name = 'Label_PeiHua.txt'
    # name = 'Label_Philips.txt'
    # name = 'Label_Thong.txt'

    # twitter
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    # # name = 'Label_PeiHua.txt'
    # # name = 'Label_Philips.txt'
    # name = 'Label_Thong.txt'

    # facebook
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF'
    name = 'CRF_label_all.txt'
    name_write = name.replace('.txt', '') + '_labeling'
    list_load = load_file(path, name)
    list_write = list()
    cnt = 0
    for sentence in list_load:
        split_sent = sentence.strip().split()
        string = ''
        for word in split_sent:
            string += word + '\t'
        cnt += len(split_sent)
        string = string.strip()
        list_write.append(string)
        list_write.append('\n')
        print string
        print '\n'
    print cnt
    # write_file(path, name_write, list_write)
