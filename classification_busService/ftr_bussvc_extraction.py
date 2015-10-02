__author__ = 'vdthoang'
import MySQLdb
from main.loadFile import load_file

def type_sv(list_sv):
    ## used to separate the length of bus svc.
    ## more specifically, bus svc. will have different types: 1, 2 and >= 3 (length)

    list_type_one = []
    list_type_two = []
    list_type_three = []
    for i in range(0, len(list_sv)): ## don't read header
        split_ = list_sv[i].split('\t')
        if len(split_[0]) == 1:
            list_type_one.append(split_[0])
        elif len(split_[0]) == 2:
            list_type_two.append(split_[0])
        else:
            list_type_three.append(split_[0])

    list_type = []
    list_type.append(list_type_one)
    list_type.append(list_type_two)
    list_type.append(list_type_three)
    return list_type

######################################################################
######################################################################


def load_idText(list_type):
    ## use to load the id of text which contain bus svc.

    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="ducthong", # your password
                      db="2015_allschemas") # name of the data base
    cur = db.cursor()
    list_type_one = list_type[0] ##only get the bus svc having len(bus_svc) = 1
    list_type_two = list_type[1] ##only get the bus svc having len(bus_svc) = 2

    list_text = []
    for bus_svc in list_type_one:
    # for bus_svc in list_type_two:
        sql = "select distinct post_id from posts_ver2_busservice where no = '" \
              + bus_svc + "'" # use for sgforum
        print sql

        cur.execute(sql)
        for row in cur.fetchall():
            text = row[0]
            if text not in list_text:
                list_text.append(text)

    db.close()
    for value in list_text:
        print value

    # print len(list_text)
    return list_text

######################################################################
######################################################################


def load_TextFeature(list_type):
    ## use to load the text which contain bus svc.

    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="ducthong", # your password
                      db="2015_allschemas") # name of the data base
    cur = db.cursor()
    list_type_one = list_type[0] ##only get the bus svc having len(bus_svc) = 1
    list_type_two = list_type[1] ##only get the bus svc having len(bus_svc) = 2

    list_text = []
    for bus_svc in list_type_one:
    # for bus_svc in list_type_two:
    #     sql = "select distinct summary from posts_ver2_busservice where no = '" \
    #           + bus_svc + "' and (summary like '% " + bus_svc + " %')" # use for
        sql = "select distinct summary from posts_ver2_busservice where no = '" \
              + bus_svc + "'" # use for sgforum
        print sql

        cur.execute(sql)
        for row in cur.fetchall():
            text = row[0]
            if text not in list_text:
                list_text.append(text)

    db.close()
    # for value in list_text:
    #     print value

    # print len(list_text)
    return list_text

######################################################################
######################################################################


def load_bus_svc(load_sv):
    list_sv = []
    for i in range(1, len(load_sv)):  # remove the header of file
        split_sv = load_sv[i].split('\t')
        list_sv.append(split_sv[0])
    return list_sv


def is_int(value):
  try:
      int(value)
      return True
  except ValueError:
      return False


def range_text_index(index, length, n_ftr):
    begin_ftr = index - n_ftr
    end_ftr = index + n_ftr
    if (begin_ftr < 0):
        begin_ftr = 0
    if (end_ftr > length - 1):
        end_ftr = length - 1
    return index, begin_ftr, end_ftr


def create_svc_feature(load_sv, list_text, n_ftr):
    ## for each text, create feature list for each number in text
    ## using n-gram for each feature

    list_ftr = []
    for index in range(0, len(list_text)):
        # print text
        text = list_text[index]
        split_text = text.split()
        for i in range (0, len(split_text)):
            if ((is_int(split_text[i]) == True) and (split_text[i] in load_sv)):
                # print split_text[i], i
                range_i = range_text_index(i, len(split_text), n_ftr)
                # print split_text[i], i, range_i[1], range_i[2]

                ftr_text = ''
                for j in range(range_i[1], range_i[2] + 1):
                    ftr_text = ftr_text + ' ' + split_text[j]
                # for j in range(i + 1, range_i[2] + 1):
                #     ftr_text = ftr_text + ' ' + split_text[j]
                ftr_text = ftr_text.strip()
                # print str(index) + '\t' + split_text[i] + '\t' + ftr_text
                list_ftr.append(str(index) + '\t' + split_text[i] + '\t' + ftr_text)
        # break
    # print len(list_text)
    for value in list_text:
        print value

    for value in list_ftr:
        print value
    print len(list_ftr)
######################################################################
######################################################################


if __name__ == '__main__':
    path_sv = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name_sv = 'bus_services.csv'

    load_sv = load_bus_svc(load_file(path_sv, name_sv))
    list_sv = [item.lower() for item in load_sv]
    # list_type_sv = type_sv(load_sv)
    # list_text = load_TextFeature(list_type_sv)
    #
    # n_ftr = 10
    # create_svc_feature(load_sv, list_text, n_ftr)

    # list_type_sv = type_sv(load_sv)
    # list_idText = load_idText(list_type_sv)