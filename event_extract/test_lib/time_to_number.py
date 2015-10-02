# -*- coding: utf-8 -*-
#!/usr/bin/env python

__author__ = 'vdthoang'

import time

# def convert_date_time(string):
#     string = string.replace('+08:00','')
#     split_string = string.split('T')
#     new_string = str(split_string[0] + ' ' + split_string[1])
#     return (int(time.mktime(time.strptime(new_string, '%Y-%m-%d %H:%M:%S'))))

#use to test the time in second when we convert from datetime

# string = '2000-01-01 12:34:00'
# print (int(time.mktime(time.strptime(string, '%Y-%m-%d %H:%M:%S'))))
# string = '2014-02-14T22:56:15+08:00'.replace('+08:00','')
# split_string = string.split('T')
# new_string = str(split_string[0] + ' ' + split_string[1])
# print (int(time.mktime(time.strptime(new_string, '%Y-%m-%d %H:%M:%S'))))
# first = int(time.mktime(time.strptime(new_string, '%Y-%m-%d %H:%M:%S')))
#
# string = '2014-02-21T22:56:15+08:00'.replace('+08:00','')
# split_string = string.split('T')
# new_string = str(split_string[0] + ' ' + split_string[1])
# print (int(time.mktime(time.strptime(new_string, '%Y-%m-%d %H:%M:%S'))))
# second = int(time.mktime(time.strptime(new_string, '%Y-%m-%d %H:%M:%S')))
#
# print (second - first)

# string = '2015-07-22T13:07:04+08:00'.replace('+08:00','')
# split_string = string.split('T')
# new_string = str(split_string[0] + ' ' + split_string[1])
# print (int(time.mktime(time.strptime(new_string, '%Y-%m-%d %H:%M:%S'))))
# first = int(time.mktime(time.strptime(new_string, '%Y-%m-%d %H:%M:%S')))
#
# string = '2014-02-14T22:56:15+08:00'.replace('+08:00','')
# split_string = string.split('T')
# new_string = str(split_string[0] + ' ' + split_string[1])
# print (int(time.mktime(time.strptime(new_string, '%Y-%m-%d %H:%M:%S'))))
# second = int(time.mktime(time.strptime(new_string, '%Y-%m-%d %H:%M:%S')))
#
# while (True):
#     if (second <= first):
#         print (str(second) + '\t' + str(second + 604800))
#         second = second + 604800
#     else:
#         break

string = 'Apr 7, 2015 10:58:54 AM'
epoch_time = int(time.mktime(time.strptime(string, '%b %d, %Y %H:%M:%S %p')))
print (epoch_time)
print (time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(epoch_time)))

string = '2015-05-08T04:00:00+0000'
epoch_time = int(time.mktime(time.strptime(string, '%Y-%m-%dT%H:%M:%S+0000')))
print (epoch_time)
print (time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(epoch_time)))

string = '2015-01-01T00:00:00+0000'
epoch_time = int(time.mktime(time.strptime(string, '%Y-%m-%dT%H:%M:%S+0000')))
print (epoch_time)
print (time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(epoch_time)))

string = '2015-07-16T00:00:00+0000'
epoch_time = int(time.mktime(time.strptime(string, '%Y-%m-%dT%H:%M:%S+0000')))
print (epoch_time)
print (time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(epoch_time)))

# string = 'Jul 13, 2015 10:08:01 PM'
# print (int(time.mktime(time.strptime(string, '%b %d, %Y %H:%M:%S %p'))))

string = 'orlove'
print string.replace(' or ', '')



print (time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(1392389775)))

string = 'Hougang Street 21'
string_2 = 'Hougang Street 51'

if (string in string_2):
    print True
else:
    print False


