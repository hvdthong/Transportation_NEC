__author__ = 'vdthoang'
from datetime import date, timedelta as td

if __name__ == '__main__':
    path_code = 'D:/nec/scripts/python_scripts/extract_and_classify.py'
    data = 'twitter'
    d1 = date(2015, 1, 1)
    d2 = date(2016, 3, 31)
    config = 'd:/bussense.properties'

    list_date = list()
    delta = d2 - d1
    for i in range(delta.days + 1):
        print d1 + td(days=i)
        list_date.append(str(d1 + td(days=i)) + 'T' + '00:00:00' + ' ' + str(d1 + td(days=i)) + 'T' + '23:59:59')

    for date in list_date:
        print path_code, data, date, config
    print len(list_date)


