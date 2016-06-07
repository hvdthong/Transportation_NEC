__author__ = 'vdthoang'
import urllib2
from main.loadFile import load_file
from CRF_labeling.feature_crf_all import folder_files


def get_svc_html(svcs, path_write, name_write):
    for i in range(1, len(svcs)):
        svc = svcs[i].split('\t')[0]
        # response = urllib2.urlopen('http://www.sbstransit.com.sg/journeyplan/servicedetails.aspx?serviceno=' + svc)
        response = urllib2.urlopen('http://www.transitlink.com.sg/eservice/eguide/service_route.php?service=' + svc)
        html = response.read()
        f = open(path_write + '/' + name_write + svc + '.html', 'w')
        f.write(html)
        f.close()
        print svcs[i]


def extract_time_svc_html(svc, htmls):
    list_time = list()
    flag = False

    for i in range(0, len(htmls)):
        if htmls[i] == '<table border="0" cellspacing="0" width="100%">':
            list_time.append(htmls[i])
            j = i + 1
            for j in range(j, len(htmls)):
                if htmls[j] != "</table>":
                    list_time.append(htmls[j])
                else:
                    list_time.append(htmls[j])
                    flag = True
                    break
        if flag is True:
            break
    # svc = svc.replace('svc_', '').replace('.html', '')
    return extract_tag_svc_html(svc, list_time)


def extract_tag_svc_html(svc, html):
    list_tag = list()
    for i in range(1, len(html) - 1):
        if html[i] == "<tr>":
            sub_tag = list()
            j = i + 1
            for j in range(j, len(html) - 1):
                if html[j] != "</tr>":
                    sub_tag.append(html[j])
                else:
                    i = j
                    break
            list_tag.append(sub_tag)

    # if "N.html" in svc:
    #     print svc, len(list_tag)
    #     extract_night_bus(svc, list_tag)
    # elif "svc_NR" in svc:
    #     print svc, len(list_tag)
    #     extract_night_bus(svc, list_tag)
    # else:
    #     if len(list_tag) == 3:
    #         extract_noLastBusStop(svc, list_tag)

    result = ''
    if "N.html" in svc:
        # pass
        # print svc, len(list_tag)
        result = extract_night_bus(svc, list_tag)
    elif "svc_NR" in svc:
        # pass
        # print svc, len(list_tag)
        result = extract_night_bus(svc, list_tag)
    elif len(list_tag) == 3:
        result = extract_noLastBusStop(svc, list_tag)
    elif len(list_tag) == 4:
        result = extract_FirstLastBusstop(svc, list_tag)
    if result != '':
        return result
    else:
        return ''


########################################################################################################
########################################################################################################
def extract_FirstLastBusstop(svc, tags):
    # print svc
    first_tag = tags[2]
    all_days = ''
    for i in range(1, len(first_tag), 2):
        first_time = first_tag[i].replace('<td width="10%" align="center">', '').replace('</td>', '')
        last_time = first_tag[i + 1].replace('<td width="10%" align="center">', '').replace('</td>', '')
        all_days += first_time + ":" + last_time + '\t'

    last_tag = tags[3]
    for i in range(1, len(last_tag), 2):
        first_time = first_tag[i].replace('<td width="10%" align="center">', '').replace('</td>', '')
        last_time = first_tag[i + 1].replace('<td width="10%" align="center">', '').replace('</td>', '')
        all_days += first_time + ":" + last_time + '\t'
    # print all_days.strip()
    return svc + '\t' + all_days.strip()


def extract_noLastBusStop(svc, tags):
    # print svc
    tag = tags[2]
    all_days = ''
    for i in range(1, len(tag), 2):
        first_time = tag[i].replace('<td width="10%" align="center">', '').replace('</td>', '')
        last_time = tag[i + 1].replace('<td width="10%" align="center">', '').replace('</td>', '')
        all_days += first_time + ":" + last_time + '\t'
    # print all_days.strip()
    return svc + '\t' + all_days.strip()


def extract_night_bus(svc, tags):
    # print svc
    tag = tags[1]
    tag_time = tag[1].replace('<td width="60%">', "").replace('</td>', "")
    split_tag = tag_time.split('-')
    first, last = split_tag[0], split_tag[1]
    # print first.strip() + ":" + last.strip()
    return svc + '\t' + first.strip() + ":" + last.strip()


########################################################################################################
########################################################################################################
if __name__ == '__main__':
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data'
    name = 'bussvc_mytransport.csv'

    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/mytransport/html_svc'
    name_write = 'svc_'
    svcs = load_file(path, name)
    # get_svc_html(svcs, path_write, name_write)

    files = folder_files(path_write)
    for f in files:
        # print '--------------------- ' + f + '--------------------- '
        list_ = load_file(path_write, f)

        result = extract_time_svc_html(f, list_)
        if result != '':
            print result

    print len(files)
