__author__ = 'vdthoang'
from main.loadFile import load_file
from main.writeFile import write_file


def index_sent(list_):
    index = list()
    for i in range(1, len(list_)):
        split_sent = list_[i].split('\t')
        index_sent = split_sent[0]
        if index_sent not in index:
            index.append(index_sent)

    return index


def combine_text_event(path_write, list_text, list_event, name_write):
    print len(list_text), len(list_event)
    list_all = list()
    for i in range(0, len(list_text)):
        combine = list_text[i] + '\t' + list_event[i]
        list_all.append(combine)

    write_file(path_write, name_write, list_all)


def event_list(path_write, list_data, list_index, name_write):
    list_text = list()
    for index in list_index:
        text = ''
        for line in list_data:
            split_line = line.split('\t')
            if int(index) == int(split_line[0]):
                text += ' ' + split_line[1]

        # print index, text
        list_text.append(text.strip())

    list_event = list()
    for index in list_index:
        event, flag = '', False
        for line in list_data:
            split_line = line.split('\t')
            if int(index) == int(split_line[0]):
                if len(split_line) >= 2:
                    flag = True
                    for j in range(2, len(split_line)):
                        event += split_line[j] + ';'
                else:
                    flag = False

        if flag is True:
            list_event.append(event)
        else:
            list_event.append('Null')
        # print index, event
    combine_text_event(path_write, list_text, list_event, name_write)

if __name__ == '__main__':
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event/labelingStudent'
    # name = 'EventsLabelingTask_completed.txt'
    #
    # list_data = load_file(path, name)
    # list_index = index_sent(list_data)
    #
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event'
    # name_write = 'EventsLabelingTask_completed'
    # event_list(path_write, list_data[1:], list_index, name_write)

    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event/labelingStudent'
    name = 'EventsLabelingTask_completed_redo.txt'

    list_data = load_file(path, name)
    list_index = index_sent(list_data)

    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event'
    name_write = 'EventsLabelingTask_completed_redo'
    event_list(path_write, list_data[1:], list_index, name_write)


