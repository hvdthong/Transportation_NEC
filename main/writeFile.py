'''
Created on 14 Jul 2015

@author: vdthoang
'''
import os, sys
# from string import punctuation
reload(sys)
sys.setdefaultencoding('utf8')


def write_file(path, name, list_write):
    if os.path.exists(path + "/" + name + '.csv'):
        print("The file already appears in the path folder")
    else:
        file_ = file(path + "/" + name + '.csv', 'w')  
        for each in list_write:             
            # file_.write(each.encode('utf-8') + '\n')
            # print str(each.encode('utf-8'))
            file_.write(each + '\n')
            # print (each)
            # file_.write(each.decode('utf-8') + '\n')
        
        file_.close()
        

