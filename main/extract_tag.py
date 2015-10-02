'''
Created on 15 Jul 2015

@author: vdthoang
'''
from bs4 import BeautifulSoup

from main.writeFile import write_file


def extract_tags(html):
    #this function used to extract multiple text in html file, note that we only extract the text between two tags
    soup = BeautifulSoup(html, 'html.parser')
    
    listText = []
    for tag in soup.findAll(True):
#         print (tag.name + '\t' + str(len(soup.findAll(tag.name))))
        length_tag = len(soup.findAll(tag.name))
        for i in range(0, length_tag):
            text = ''
            try:
                for hit in soup.findAll(tag.name)[i].next:
                    text = text + hit
            except TypeError:
#                 print ("wrong html detects")
                break
#             print text
            if (text not in listText):
                listText.append(text)
    
    str_text = ''
    for each in listText:
        str_text = str_text + ' ' + each.strip()
    return str_text.strip() 
    
def extract_tags_sgForum(path, name):
    #used to read sgForum data and then extract the text in these data
    
    list_write = []
    with open(path + '/' + name) as f:
        i = 0
        for line in f:            
#             print (line)
            split_line = line.split('\t')
            post_id = split_line[2]
            summary = split_line[8]
#             print (split_line[2] + '\t' + split_line[8]) 
#             print (post_id + '\t' + summary)
            print (str(i) + '\t' + post_id + '\t' + extract_tags(summary))
            if (i >= 1):                
                list_write.append(post_id + '\t' + extract_tags(summary))            
#             if (i == 2):                
#                 break
            i = i + 1
    
    write_file(path, 'posts_extract', list_write) #extract texts and write it on csv file
         
    
if __name__ == '__main__':
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20150714'
    name = 'posts.csv'
    extract_tags_sgForum(path, name)