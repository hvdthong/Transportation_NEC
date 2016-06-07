__author__ = 'vdthoang'

from skll import kappa
from main.loadFile import load_file
from clf_event.load_lbl_event import loading_event, statis_lbl


def get_data(data_student, data_RE):
    list_all, list_student, list_RE = list(), list(), list()
    list_text = list()

    for value in data_RE:
        split_value = value.split('\t')
        list_text.append(split_value[0])

    for index in range(0, len(data_student)):
        split_index = data_student[index].split('\t')
        text = split_index[0]

        if text in list_text:
            index_part = list_text.index(text)

            list_student.append(data_student[index])
            list_RE.append(data_RE[index_part])

    list_all.append(list_student), list_all.append(list_RE)
    return list_all


def check_label_event(event, sents, command):
    list_label = list()

    if command == 'student':
        for sent in sents:
            flag = False
            split_sent = sent.strip().lower().split('\t')

            if len(split_sent) > 1:
                for i in range(1, len(split_sent)):
                    multiple_events = split_sent[i].split(';')
                    for each_event in multiple_events:
                        split_each_event = each_event.split(':')
                        if event == 'wait_slow':
                            if ('wait' == split_each_event[0].strip()) or ('slow' == split_each_event[0].strip()):
                                flag = True
                        else:
                            if event == split_each_event[0].strip():
                                flag = True

                if flag is True:
                    list_label.append(1)
                else:
                    list_label.append(0)
            else:
                list_label.append(0)

    elif command == 'RE':
        for sent in sents:
            flag = False
            split_sent = sent.lower().split('\t')

            if len(split_sent) > 1:
                for i in range(1, len(split_sent)):
                    split_label = split_sent[i].split(':')
                    if event == split_label[0]:
                        flag = True

                if flag is True:
                    list_label.append(1)
                else:
                    list_label.append(0)
            else:
                list_label.append(0)
    return list_label


def kappa_score(events, data_student, data_RE):

    for event in events:
        label_student = check_label_event(event, data_student, 'student')
        label_RE = check_label_event(event, data_RE, 'RE')

        print event + '\t' + str(kappa(label_RE, label_student))


if __name__ == '__main__':
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event'
    name_RE = 'Philips_twitter_labeledComplete_ver2.txt'
    name_student = 'EventsLabelingTask_completed.txt'

    load_RE = load_file(path, name_RE)
    load_data = get_data(load_file(path, name_student), load_RE)

    list_student_event = loading_event(load_data[0], len(load_data[0]), command='new_label')
    list_RE_event = loading_event(load_data[1], len(load_data[1]), command='')

    RE_events = statis_lbl(list_RE_event)
    RE_student = statis_lbl(list_student_event)

    events = list()
    for event in RE_events:
        if event not in events:
            events.append(event)
    for event in RE_student:
        if event not in events:
            events.append(event)
    events = sorted(events)
    kappa_score(events, load_data[0], load_data[1])
