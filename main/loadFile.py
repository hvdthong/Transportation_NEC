'''
Created on 22 Jul 2015

@author: vdthoang
'''
def load_file(path, name):
    list_ = list()
    with open(path + '/' + name) as f:
        for line in f:
            list_.append(line.strip().decode('utf-8-sig').encode('utf-8', 'ignore'))
            # list_.append(line.decode('utf-8').strip())
    return list_