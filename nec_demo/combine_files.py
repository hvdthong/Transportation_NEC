__author__ = 'vdthoang'


from main.loadFile import load_file
from main.writeFile import write_file


def combine_mult_file(path, name, enum):
    list_files = list()

    for index in range(1, (enum + 1)):
        file = load_file(path, name + '_' + str(index) + '.csv')
        # file = load_file(path, name + str(index) + '.csv')
        list_files = list_files + file
        print index, len(file)
    print len(list_files)
    write_file(path, name, list_files)

if __name__ == '__main__':
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/twitter'
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/sgforums/crf_features'
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/facebook/crf_features'
    # name = 'ftr_reg_match_road'
    name = 'ftr_reg_match_busstop'
    enum = 11
    combine_mult_file(path, name, enum)
