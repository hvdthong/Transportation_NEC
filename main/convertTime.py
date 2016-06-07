__author__ = 'vdthoang'

import time
import datetime


def convertTime_allpost(string):
    string = string.replace('+08:00','')
    split_string = string.split('T')
    new_string = str(split_string[0] + ' ' + split_string[1])
    return int(time.mktime(time.strptime(new_string, '%Y-%m-%d %H:%M:%S')))


def convertTime_facebook(string):
    epoch_time = int(time.mktime(time.strptime(string, '%Y-%m-%dT%H:%M:%S+0000')))
    return epoch_time


def convertTime_twitter(string):
    epoch_time = int(time.mktime(time.strptime(string, '%b %d, %Y %I:%M:%S %p')))
    return epoch_time

def week_second():
    return (24 * 7 * 3600)

def day_second():
    return (24 * 3600)


def timeSpam_twitter(string):
    timespam = datetime.datetime.strptime(string, '%b %d, %Y %I:%M:%S %p').strftime('%Y-%m-%d %H:%M:%S')
    return timespam

if __name__ == '__main__':
    string = 'Aug 8, 2015 10:08:41 AM'
    print convertTime_twitter(string)

    string = 'Aug 8, 2015 10:08:41 PM'
    print timeSpam_twitter(string)

