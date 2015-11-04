__author__ = 'vdthoang'
from main.loadFile import load_file
from main.writeFile import write_file


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


def give_lable_sents(sents, event):
    list_label = list()

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


def create_lbl_detectEvent(path_, list_lbl, events, number):
    list_sents = get_sentence(list_lbl, number)
    for event in events:
        list_lbl_event = give_lable_sents(list_sents, event)
        write_file(path_, event, list_lbl_event)
        print event, len(list_lbl_event)


########################################################################################################
########################################################################################################


if __name__ == '__main__':
    # TWITTER
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event'
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
    path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver2'
    name_ = 'Philips_twitter_labeledComplete_ver2.txt'
    list_lbl = load_file(path_, name_)
    events = ['missing', 'wait', 'slow']
    create_lbl_detectEvent(path_write, list_lbl, events, number=len(list_lbl))
