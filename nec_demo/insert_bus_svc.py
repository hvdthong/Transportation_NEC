__author__ = 'vdthoang'
from main.loadFile import load_file

def businfo(list_bussvc):
    svcs, starts, ends = list(), list(), list()
    for i in range(1, len(list_bussvc)):
        split_info = list_bussvc[i].split('\t')
        svc, start_end = split_info[0], split_info[4]
        split_start_end = start_end.split('-')

        if len(split_start_end) > 1:
            start, end = split_start_end[0], split_start_end[1]
        else:
            start, end = split_start_end[0], split_start_end[0]
        print svc + '\t' + start + '\t' + end


if __name__ == '__main__':
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name = 'bus_services.csv'

    list_bussvc = load_file(path, name)
    businfo(list_bussvc)
