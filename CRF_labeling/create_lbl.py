__author__ = 'vdthoang'

from main.loadFile import load_file
if __name__ == '__main__':
    # sgforums
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF'
    # name = 'Label_PeiHua.txt'
    # name = 'Label_Philips.txt'
    # name = 'Label_Thong.txt'

    # twitter
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF'
    # name = 'Label_PeiHua.txt'
    # name = 'Label_Philips.txt'
    name = 'Label_Thong.txt'

    list_load = load_file(path, name)
    for value in list_load:
        print value
        print '\n'
