'''
Created on 16 Jul 2015

@author: vdthoang
'''
from string import punctuation

from main.writeFile import write_file


def filter_token(string):
    #clean each token in String
    
    #print (string)
    split_str = string.split()
    
    clean_str = ''    
    for text in split_str:
    #clean if the first character of string contains the punctuation
        while (True):
            if (text[0] in punctuation):
                text = text[1:]
                
                if (len(text) == 0):
                    break
            else:
                break
        
        #clean if the final character of string contains the punctuation    
        while (True):
            if (len(text) == 0):
                    break
            
            if (text[-1] in punctuation):
                text = text[:-1]
            else:
                break
        clean_str = clean_str.strip() + ' ' + text
        
    return clean_str.strip()


def filter_data(path, name):
    #clean text, first and last character if they are punctuation in string
    
    list_write = []    
    with open(path + '/' + name) as f:
        for line in f:
            
            split_line = line.split('\t')
            print (split_line[0] + '\t' + filter_token(split_line[1]))
            list_write.append(split_line[0] + '\t' + filter_token(split_line[1]))
    
    write_file(path, 'posts_filter', list_write) #extract texts and write it on csv file
            
if __name__ == '__main__':
#     path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20150714'
#     name = 'posts_extract.csv'

    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts'
    name = 'posts_extract.csv'
    
    filter_data(path, name)
    
    