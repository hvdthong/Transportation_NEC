'''
Created on 15 Jul 2015

@author: vdthoang
'''

from bs4 import BeautifulSoup
from main.writeFile import write_file
import sys
from CRF_labeling.filterText_CRF import filter_eachTok_rmLinks

# make the default is 'utf-8'
reload(sys)
sys.setdefaultencoding('utf8')


def extract_tags(html):
    # this function used to extract multiple text in html file, note that we only extract the text between two tags
    soup = BeautifulSoup(html, 'html.parser')
    listText = list()
    print soup.text.strip()

    for tag in soup.findAll(True):
        # print (tag.name + '\t' + str(len(soup.findAll(tag.name))))
        print tag
        length_tag = len(soup.findAll(tag.name))
        for i in range(0, length_tag):
            text = ''
            try:
                for hit in soup.findAll(tag.name)[i].next:
                    text = text + hit
            except TypeError:
                # print ("wrong html detects")
                break
            # print text
            if text not in listText:
                listText.append(text)
    
    str_text = ''
    for each in listText:
        str_text = str_text + ' ' + each.strip()
    return str_text.strip() 


def extract_tags_sgForum(path, name):
    # used to read sgForum data and then extract the text in these data
    list_write = list()
    with open(path + '/' + name) as f:
        i = 0
        for line in f:
            text = extract_tags(line).replace('\t', ' ').strip()
            # print text

#             # print (line)
#             split_line = line.split('\t')
#             forum_id, topic_id, post_id, id_str = split_line[0], split_line[1], split_line[2], split_line[3]
#             link, title, author, published_date = split_line[4], split_line[5], split_line[6], split_line[7]
#             summary, updated_date, collection_date = split_line[8], split_line[9], split_line[10]
#
#             # summary = str(split_line[8])
#             # print (split_line[2] + '\t' + split_line[8])
#             # print (post_id + '\t' + summary)
#             # print (str(i) + '\t' + post_id + '\t' + extract_tags(summary))
#
#             text = extract_tags(summary).replace('\t', ' ').strip()
#             try:
#                 if len(text) > 0:
#                     filtering = filter_eachTok_rmLinks(text, '')
#                     if len(filtering) > 0:
#                         write_line = forum_id + '\t' + topic_id + '\t' + post_id + '\t' + id_str + '\t' \
#                                      + link + '\t' + title + '\t' + author + '\t' + published_date + '\t' \
#                                      + text + '\t' + updated_date + '\t' + collection_date
#                         # print write_line
#                         list_write.append(write_line.strip())
#             except UnicodeError:
#                 print 'wrong', i
#             # if (i >= 1) and (len(text) > 0):
#             #     list_write.append(post_id + '\t' + text)
#
# #             if (i == 2):
# #                 break
#             print i
#             i += 1
#             # if i % 1000 == 0:
#             #     print i

    # write_file(path, 'posts_extract', list_write)  # extract texts and write it on csv file
    
if __name__ == '__main__':
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20150714'
    # name = 'posts.csv'

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/sgforums'
    # name = 'sgforums_posts_Aug_Oct.csv'
    # extract_tags_sgForum(path, name)

    path = 'D:'
    name = 'html_long.txt'
    extract_tags_sgForum(path, name)
