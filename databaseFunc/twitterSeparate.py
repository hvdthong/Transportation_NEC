from main.loadFile import load_file
from main.writeFile import write_file
__author__ = 'vdthoang'


def twitter_seperate_file(path, name, number):
    list_load = load_file(path, name)
    chunks = [list_load[x:x+number] for x in xrange(0, len(list_load), number)]

    for index in range(0, len(chunks)):
        write_file(path, name.replace('.csv', '') + '_' + str(index + 1), chunks[index])

if __name__ == '__main__':
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter'
    name = 'tweet_2015_filtering.csv'
    number = 32000 #total size of tweets is: 156971, we separate in to 5 different files
    twitter_seperate_file(path, name, number)
