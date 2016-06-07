__author__ = 'vdthoang'
from datetime import datetime


firstTime = '00:54:40'
secondTime = '01:55:35'
thirdTime = '05:00:00'

time_fmt = '%H:%M:%S'
firstTime = datetime.strptime(firstTime, time_fmt)
secondTime = datetime.strptime(secondTime, time_fmt)
thirdTime = datetime.strptime(thirdTime, time_fmt)

if secondTime <= firstTime or secondTime >= thirdTime:
    print True