__author__ = 'vdthoang'

import time
def convertTime_allpost(string):
    string = string.replace('+08:00','')
    split_string = string.split('T')
    new_string = str(split_string[0] + ' ' + split_string[1])
    return int(time.mktime(time.strptime(new_string, '%Y-%m-%d %H:%M:%S')))

def convertTime_facebook(string):
    epoch_time = int(time.mktime(time.strptime(string, '%Y-%m-%dT%H:%M:%S+0000')))
    return epoch_time

def convertTime_twitter(string):
    epoch_time = int(time.mktime(time.strptime(string, '%b %d, %Y %H:%M:%S %p')))
    return epoch_time

def week_second():
    return (24 * 7 * 3600)

def day_second():
    return (24 * 3600)