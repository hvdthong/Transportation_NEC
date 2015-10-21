__author__ = 'vdthoang'
from main.loadFile import load_file


def clean_quote(string):
    string = string.replace('"', '')
    return string


def statis_lbl(list_event):
    events = list()
    for value in list_event:
        split_value = value.lower().split(':')
        if split_value[0] not in events:
            events.append(split_value[0])

    events = sorted(events)
    for event in events:
        cnt = 0
        for value in list_event:
            split_value = value.lower().split(':')
            if event == split_value[0]:
                cnt += 1
        print event + '\t' + str(cnt)


def loading_event(list_lbl, number):
    list_ = list()
    cnt = 1
    for value in list_lbl:
        split_value = value.split('\t')
        if len(split_value) > 1:
            labeling = split_value[1:]
            for each in labeling:
                list_.append(clean_quote(each.strip()))
                # print number, clean_quote(each.strip()), split_value[0]
        cnt += 1
        if cnt == number:
            break
    print len(list_)
    return list_


if __name__ == '__main__':
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event'
    name_ = 'Philips_twitter_labeled3000.txt'

    list_lbl = load_file(path_, name_)
    list_event = loading_event(list_lbl, 3000)
    statis_lbl(list_event)
