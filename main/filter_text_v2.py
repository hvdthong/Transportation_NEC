'''
Created on 21 Jul 2015

@author: vdthoang
'''
# this will be used to filter the text to extract bus service number for each post on sgforums
from main.writeFile import write_file

def replace_multiple(string, list_punc):
    for punc in list_punc:
        if (punc in string):
            string = string.replace(punc, ' ')
    return string

def clean_text_busService(string, char_punc_remove):
    split_str = string.split()
    
    new_str = ''
    for token in split_str:
        if ('http' not in token):
            #new_str = new_str + ' ' + token.translate(' ', ''.join(char_punc_remove)).strip()
            new_str = new_str + ' ' + replace_multiple(token, char_punc_remove)
        else:
            new_str = new_str + ' ' + token
    return new_str.strip()

def filter_text_busService(path, name, char_punc_remove):
    #clean text to extract bus services number
    
    list_write = []
    with open(path + '/' + name) as f:
        for line in f:
            if (name == 'posts_filter.csv'):
                split_line = line.split('\t')
                print (split_line[0] + '\t' + clean_text_busService(split_line[1], char_punc_remove))
                list_write.append(split_line[0] + '\t' + clean_text_busService(split_line[1], char_punc_remove))
            else:
                split_line = line.split('\t')
                print (split_line[0] + '\t' + split_line[1] + '\t' + clean_text_busService(split_line[2], char_punc_remove))
                list_write.append(split_line[0] + '\t' + split_line[1] + '\t' + clean_text_busService(split_line[2], char_punc_remove))
    
    #write_file(path, 'posts_filter_1279_v2', list_write) #extract texts and write it on csv file
    write_file(path, 'posts_filter_v2', list_write) #extract texts and write it on csv file
    
if __name__ == '__main__':
#     path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20150714'
#     name = 'posts_filter_1279.csv'

    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts'
    name = 'posts_filter.csv'
    char_punc_remove = [':','(',')','[',']', ',']
    
    filter_text_busService(path, name, char_punc_remove)
    
#     string = 'Originally posted by carbikebus Future Bus Packages Jurong Port Depot(550 lots Tuas West Ter:192,193,203,204 Joo Koon Ith:185,251,253,254,255,257,502/A Boon Lay Ith:150,154,174/e,179,181,182/M,194,199,240 241,242,243G/W,246,249,252,253,405,406 Bulim Depot(550 lots Tengah Ith:205,206,207,208,600 Bt Batok Ith:77,106/e,173,177,189,941,945 947,990,991 Jurong East Ith:41,49,66,78,79,97/e,98/M,143/M,144 183,333,334,335 Upper Bukit Timah Depot(550 lots Choa Chu Kang Int:172,188/e,190,300,301,302,307,927,928 983,985 Bt Panjang Ith:75,176,180,184,700,701,920,922,970 972,975 Woodlands Reg Int:178,187,925/A JB Sentral Ter:160,170X Larkin Ter:170 Mandai Depot(550 lots Woodlands Reg Int:856,858,900/A,901,902,903,904,911 912,913,926,960,961,962,963/e,964,965,966,967,968,969 Woodlands North Ith:908,952,953,954,955 JB Sentral Ter:950 Larkin Ter:870 Sungei Seletar Depot(500 lots Sembawang Int:859/A/B,878,882,980,981 Yishun Ith:800,803,804,806,808,811,812,850,851 852,853,854/e,855,857,860,861 Where got Service 144 203 204 205 206 207 208 406 600 701 808 878 908 928 951 952 953 954 955 967 968 and 991 They are not introuduced yet'
#     string = 'Ith:185,251,253,254,255,257,502/A'
#     string = 'Originally posted by carbikebus My wild guess for Joo Koon 185,251,254,255,257,502 and a new JIS Boon Lay will have at least 2 more new service,1 JIS covering the missing link and a medium haul trunk svc.Tuas probably will have a new svc cover Jurong Pier Rd actually 185 and 502 are the obvious ones since currently they originate from bus depot'
#     print (clean_text_busService(string, char_punc_remove))