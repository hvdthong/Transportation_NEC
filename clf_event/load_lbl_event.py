__author__ = 'vdthoang'
from main.loadFile import load_file
from main.writeFile import write_file


def clean_quote(string):
    string = string.replace('"', '')
    return string


def loading_event_ver2(list_lbl):
    events = list()
    for value in list_lbl:
        split_value = value.strip().split('\t')
        for index in range(1, len(split_value)):
            label = split_value[index]

            # note that this is events
            if len(label) > 0:
                split_label = label.split(';')  # split if we have many events
                for value_label in split_label:
                    if len(value_label) > 0:
                        split_value_label = value_label.strip().lower().split(':')
                        if split_value_label[0].strip() not in events:
                            events.append(split_value_label[0])
    events = sorted(events)
    for event in events:
        cnt = 0
        for sent in list_lbl:
            flag = False
            split_value = sent.strip().split('\t')
            for index in range(1, len(split_value)):
                label = split_value[index]

                # note that this is events
                if len(label) > 0:
                    split_label = label.split(';')  # split if we have many events
                    for value_label in split_label:
                        if len(value_label) > 0:
                            split_value_label = value_label.strip().lower().split(':')
                            if split_value_label[0].strip() == event:
                                flag = True
            if flag is True:
                cnt += 1
        print event + '\t' + str(cnt)


def statis_lbl(list_event):
    events = list()
    for value in list_event:
        split_value = value.lower().split(':')
        if split_value[0].strip() not in events:
            events.append(split_value[0])

    events = sorted(events)
    for event in events:
        cnt = 0
        for value in list_event:
            split_value = value.lower().split(':')
            if event == split_value[0].strip():
                cnt += 1
        print event + '\t' + str(cnt)
    return events


def loading_event(list_lbl, number, command):
    list_ = list()
    cnt = 1
    if command == 'new_label':
        for value in list_lbl:
            split_value = value.strip().split('\t')
            for index in range(1, len(split_value)):
                label = split_value[index]

                # note that this is events
                if len(label) > 0:
                    split_label = label.split(';')  # split if we have many events
                    for each in split_label:
                        if len(each) > 0:
                            list_.append(clean_quote(each.strip()))
    else:
        for value in list_lbl:
            split_value = value.strip().split('\t')
            if len(split_value) > 1:
                labeling = split_value[1:]
                for each in labeling:
                    if len(each) > 0:
                        list_.append(clean_quote(each.strip()))
                    # print number, clean_quote(each.strip()), split_value[0]

            cnt += 1
            if cnt == number:
                break
    print len(list_)
    return list_


########################################################################################################
########################################################################################################
def get_sentence(list_sents, number):
    # get the number of sentences
    list_get = list()
    cnt = 1
    for sent in list_sents:
        list_get.append(sent)
        if cnt == number:
            break
        else:
            cnt += 1
    return list_get


def give_lable_sents(sents, event, command):
    list_label = list()

    if command == 'new_label':
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
                    list_label.append(event + '\t' + '1' + '\t' + split_sent[0].lower())
                else:
                    list_label.append(event + '\t' + '0' + '\t' + split_sent[0].lower())
            else:
                list_label.append(event + '\t' + '0' + '\t' + split_sent[0].lower())
    else:
        for sent in sents:
            flag = False
            split_sent = sent.lower().split('\t')

            if len(split_sent) > 1:
                for i in range(1, len(split_sent)):
                    split_label = split_sent[i].split(':')
                    if event == split_label[0]:
                        flag = True

                if flag is True:
                    list_label.append(event + '\t' + '1' + '\t' + split_sent[0].lower())
                else:
                    list_label.append(event + '\t' + '0' + '\t' + split_sent[0].lower())
            else:
                list_label.append(event + '\t' + '0' + '\t' + split_sent[0].lower())
    return list_label


def create_lbl_detectEvent(path_, list_lbl, events, number, command):
    list_sents = get_sentence(list_lbl, number)
    for event in events:
        list_lbl_event = give_lable_sents(list_sents, event, command)
        write_file(path_, event, list_lbl_event)


########################################################################################################
########################################################################################################
def give_label_sents_groupEvent(sents, event, name, command):
    list_label = list()

    if command == 'new_label':
        for sent in sents:
            flag = False
            split_sent = sent.lower().split('\t')

            if len(split_sent) > 1:
                for i in range(1, len(split_sent)):
                    multiple_events = split_sent[i].split(';')
                    for each_event in multiple_events:
                        split_each_event = each_event.split(':')
                        if split_each_event[0].strip() in event:
                            flag = True

                if flag is True:
                    list_label.append(name + '\t' + '1' + '\t' + split_sent[0].lower())
                else:
                    list_label.append(name + '\t' + '0' + '\t' + split_sent[0].lower())
            else:
                list_label.append(name + '\t' + '0' + '\t' + split_sent[0].lower())
    else:
        for sent in sents:
            flag = False
            split_sent = sent.lower().split('\t')

            if len(split_sent) > 1:
                for i in range(1, len(split_sent)):
                    split_label = split_sent[i].split(':')
                    if split_label[0] in event:
                        flag = True

                if flag is True:
                    list_label.append(name + '\t' + '1' + '\t' + split_sent[0].lower())
                else:
                    list_label.append(name + '\t' + '0' + '\t' + split_sent[0].lower())
            else:
                list_label.append(name + '\t' + '0' + '\t' + split_sent[0].lower())
    return list_label


def groupedEvents(path_, list_lbl, events, names, number, command):
    list_sents = get_sentence(list_lbl, number)
    for index in range(0, len(events)):
        event, name = events[index], names[index]
        list_lbl_event = give_label_sents_groupEvent(list_sents, event, name, command)
        write_file(path_, name, list_lbl_event)
        print name, len(list_lbl_event)


########################################################################################################
########################################################################################################
def give_label_sent_ftrSgforums(list_sents, event):
    list_label = list()
    for sent in list_sents:
        flag = False
        split_sent = sent.strip().lower().split('\t')

        if event in split_sent[0].lower():
            new_sent = split_sent[0].lower() + ' matching_' + event
        else:
            new_sent = split_sent[0].lower()

        if len(split_sent) > 1:
            for i in range(1, len(split_sent)):
                multiple_events = split_sent[i].split(';')
                for each_event in multiple_events:
                    split_each_event = each_event.split(':')
                    if event == split_each_event[0].strip():
                        flag = True
                        break
            if flag is True:
                list_label.append(event + '\t' + '1' + '\t' + new_sent)
            else:
                list_label.append(event + '\t' + '0' + '\t' + new_sent)
        else:
            list_label.append(event + '\t' + '0' + '\t' + new_sent)
    return list_label


def create_lbl_detectEvent_ftrSgforums(path_, list_lbl, events, number):
    list_sents = get_sentence(list_lbl, number)
    for event in events:
        list_lbl_event = give_label_sent_ftrSgforums(list_sents, event)
        write_file(path_, event + '_ftrMatch', list_lbl_event)

########################################################################################################
########################################################################################################
import numpy as np

def histogram_labeled(load_data):
    list_cnt_events = list()
    for sent in load_data:
        split_sent = sent.strip().lower().split('\t')
        if len(split_sent) > 1:
            events = list()
            for i in range(1, len(split_sent)):
                multiple_events = split_sent[i].split(';')
                for each_event in multiple_events:
                    split_each_event = each_event.split(':')
                    if split_each_event[0] not in events:
                        events.append(split_each_event[0])

            list_cnt_events.append(len(events))
        else:
            list_cnt_events.append(0)

    print max(list_cnt_events), len(list_cnt_events)
    list_bin = list()
    for index in range(0, max(list_cnt_events)):
        list_bin.append(index)
    hist = np.histogram(list_cnt_events, bins=max(list_cnt_events) + 1)
    print hist[0]

########################################################################################################
########################################################################################################
if __name__ == '__main__':
    # TWITTER
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event'
    # name_ = 'Philips_twitter_labeledComplete_ver2.txt'

    # loading the distribution of each events
    # list_lbl = load_file(path_, name_)
    # list_event = loading_event(list_lbl, len(list_lbl))
    # statis_lbl(list_event)

    # using to create a label for running classification
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents'
    # events = ['missing', 'delay']
    # create_lbl_detectEvent(path_write, list_lbl, events, number=3000)

    # # using to create a label for running classification
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets'
    # name_ = 'Philips_twitter_labeledComplete.txt'
    # list_lbl = load_file(path_, name_)
    # events = ['missing', 'delay']
    # create_lbl_detectEvent(path_write, list_lbl, events, number=len(list_lbl))

    # # using to create a label for running classification
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver2'
    # name_ = 'Philips_twitter_labeledComplete_ver2.txt'
    # list_lbl = load_file(path_, name_)
    # # events = ['missing', 'wait', 'slow']
    # # create_lbl_detectEvent(path_write, list_lbl, events, number=len(list_lbl))
    # ########################################################################################################
    # event_busstop = ['wait', 'queue', 'bunch', 'skip', 'late', 'delay']
    # event_transist = ['breakdown', 'crowd', 'missing', 'slow', 'jam', 'accident']
    #
    # list_event = loading_event(list_lbl, len(list_lbl))
    # new_events = list()
    #
    # # first is the list of events for bus stop, second is the list of events for transist
    # new_events.append(event_busstop), new_events.append(event_transist)
    # name_events = ['busstop', 'transist']
    #
    # # just to see the statistical events list
    # print statis_lbl(list_event)
    # print len(event_busstop) + len(event_transist), event_busstop, event_transist
    # print new_events
    # groupedEvents(path_write, list_lbl, new_events, name_events, len(list_lbl))

    ########################################################################################################
    ########################################################################################################
    # using to create a label for running classification
    # using for new labeling 'EventsLabelingTask_completed.txt'
    # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver3'
    # name_ = 'EventsLabelingTask_completed.txt'
    # list_lbl = load_file(path_, name_)
    #
    # # list_event = loading_event(list_lbl, len(list_lbl), command='new_label')  # use for new labeling by the student
    # # for event in list_event:
    # #     print event
    # # statis_lbl(list_event)
    #
    # # list_event = loading_event_ver2(list_lbl)  # use for 'new_label'
    # # events = ['wait', 'missing', 'skip', 'slow', 'accident', 'crowd']
    # # events = ['wait_slow']
    # # create_lbl_detectEvent(path_write, list_lbl, events, number=len(list_lbl), command='new_label')
    #
    # ########################################################################################################
    # event_busstop = ['wait', 'queue', 'bunch', 'skip']
    # event_transist = ['breakdown', 'crowd', 'missing', 'slow', 'jam', 'accident']
    #
    # # list_event = loading_event(list_lbl, len(list_lbl))
    # new_events = list()
    # #
    # # # first is the list of events for bus stop, second is the list of events for transist
    # new_events.append(event_busstop), new_events.append(event_transist)
    # name_events = ['busstop', 'transist']
    # #
    # # # just to see the statistical events list
    # # print statis_lbl(list_event)
    # # # print len(event_busstop) + len(event_transist), event_busstop, event_transist
    # # # print new_events
    # groupedEvents(path_write, list_lbl, new_events, name_events, len(list_lbl), command='new_label')

    ########################################################################################################
    ########################################################################################################
    # use to draw the histogram of labelled data in Twitter
    # name_ = 'EventsLabelingTask_completed.txt'
    # list_lbl = load_file(path_, name_)
    # histogram_labeled(list_lbl)


    ########################################################################################################
    ########################################################################################################
    ########################################################################################################
    ########################################################################################################
    # FACEBOOK
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event'
    # # name_ = 'EventsLabelingTask_completed.csv'
    name_ = 'EventsLabelingTask_completed_redo.csv'
    # #
    list_lbl = load_file(path_, name_)
    # # # list_event = loading_event(list_lbl, len(list_lbl), command='new_label')  # use for new labeling by the student
    # # # for event in list_event:
    # # #     print event
    # # # statis_lbl(list_event)
    # # #
    # # #
    # # list_event = loading_event_ver2(list_lbl)  # use for 'new_label'
    # # print list_event
    # # path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event/detectAllEvents'
    # # events = ['wait', 'complaint', 'compliment', 'skip', 'crowd']
    #
    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event/detectAllEvents_ver2'
    events = ['wait', 'complaint', 'compliment', 'skip', 'suggestion']
    # create_lbl_detectEvent(path_write, list_lbl, events, number=len(list_lbl), command='new_label')
    create_lbl_detectEvent_ftrSgforums(path_write, list_lbl, events, number=len(list_lbl))

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################
    ########################################################################################################
    # SGFORUMS
    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_classification_events'
    # # name_ = 'EventsLabelingTask_completed_3001.csv'

    # path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_classification_events'
    # name_ = 'EventsLabelingTask_completed_3001_redo.csv'
    #
    # list_lbl = load_file(path_, name_)
    # # list_event = loading_event(list_lbl, len(list_lbl), command='new_label')  # use for new labeling by the student
    # # for event in list_event:
    # #     print event
    # # statis_lbl(list_event)
    #
    # # list_event = loading_event_ver2(list_lbl)  # use for 'new_label'
    # # print list_event
    # # # path_write = path_ + '/detectAllEvents'
    # path_write = path_ + '/detectAllEvents_ver2'
    # events = ['bunch', 'crowd']
    # # create_lbl_detectEvent(path_write, list_lbl, events, number=len(list_lbl), command='new_label')
    # create_lbl_detectEvent_ftrSgforums(path_write, list_lbl, events, number=len(list_lbl))


