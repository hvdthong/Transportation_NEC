'''
Created on 22 Jul 2015

@author: vdthoang
'''
def load_file(path, name):
    list_ = []
    with open(path + '/' + name) as f:
        for line in f:
            list_.append(line.strip())
            # list_.append(line.decode('utf-8').strip())
    return list_