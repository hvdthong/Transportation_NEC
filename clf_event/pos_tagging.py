__author__ = 'vdthoang'


from main.loadFile import load_file
from sklearn.metrics import confusion_matrix


def count_pos(tags):
    list_tag = list()
    for tag in tags:
        split_tag = tag.split('\t')
        for each in split_tag:
            if each not in list_tag:
                list_tag.append(each)
    return list_tag


def convert_POS(sents_pos):
    list_all, sents, tags = list(), list(), list()
    sent, tag = '', ''
    for value in sents_pos:
        split_value = value.split('\t')
        if len(split_value) > 1:
            sent += '\t' + split_value[0]
            tag += '\t' + split_value[1]
        else:
            sents.append(sent.strip()), tags.append(tag.strip())
            sent, tag = '', ''

    list_all.append(sents), list_all.append(tags)
    return list_all


#############################################################################################
#############################################################################################
# def contain_speech(sent, tag, speech):
#     flag = False
#     for value in tag:
#         split_value = value.strip().split('\t')
#         for each in split_value:
#             if each == speech:
#                 flag = True
#                 return flag
#     return flag


def contain_interjection(sent, tag):
    flag = False
    for value in tag:
        split_value = value.strip().split('\t')

        for each in split_value:
            if '!' == each:
                flag = True
                return flag
    return flag


def interjection(sents_tags, sents_event):
    tags = sents_tags[1]  # get all the part_of_speech
    list_gt, list_inter = list(), list()

    for tag in tags:
        flag = False
        value_tag = tag.strip().split('\t')
        for value in value_tag:
            if '!' == value:
                flag = True

        if flag is True:
            list_inter.append(1)
        else:
            list_inter.append(0)

    for index in range(0, len(sents_event)):
        split_line = sents_event[index].split('\t')
        label = split_line[1]
        list_gt.append(int(label))

        flag = False
        tag = tags[index]
        value_tag = tag.strip().split('\t')
        for value in value_tag:
            if '!' == value:
                flag = True

        if (flag is True) and (int(label) == 1):
            print split_line[0] + '\t' + split_line[2]

    matrix = confusion_matrix(list_inter, list_gt)
    for value in matrix:
        line = ''
        for each in value:
            line = line + str(each) + '\t'
        print line.strip()
    print '----------------'


#############################################################################################
#############################################################################################
# Before token "bus" in tweets, check whether this token has the adj, verb or adverb
# note that we only consider 5 tokens before anchor token
def bef_bus(index_token, tag, command):
    split_tag = tag.split('\t')
    # if (index_token - 5) > 0:
    #     tags_token = split_tag[(index_token - 5):index_token]
    # else:
    #     tags_token = split_tag[0:index_token]

    tags_token = split_tag[0:index_token]

    if command == 'adj':
        if 'A' in tags_token:
            return True
        else:
            return False
    elif command == 'adverb':
        if 'R' in tags_token:
            return True
        else:
            return False
    elif command == 'verb':
        if 'V' in tags_token:
            return True
        else:
            return False


def bef_token_bus(sent, tag, command):
    split_sent = sent.split('\t')

    flag = False
    for index in range(0, len(split_sent)):
        token = split_sent[index]
        if 'bus' in token:
            flag = bef_bus(index, tag, command)
        if flag is True:
            break
    return flag


def bef_POS(sents_tags, sents_event, command):
    # check the part-of-speech whether the previous token is adj, adverb or verb
    sents, tags = sents_tags[0], sents_tags[1]
    list_gt, list_befPOS = list(), list()

    for index in range(0, len(sents_event)):
        sent, tag = sents[index], tags[index]
        flag = bef_token_bus(sent, tag, command)

        # get the label for ground truth
        split_line = sents_event[index].split('\t')
        label = split_line[1]
        list_gt.append(int(label))

        # get the label for before part-of-speech
        if flag is True:
            list_befPOS.append(1)
        else:
            list_befPOS.append(0)

        if (flag is True) and (int(label) == 1):
            print sent
            print tag

    matrix = confusion_matrix(list_befPOS, list_gt)
    for value in matrix:
        line = ''
        for each in value:
            line = line + str(each) + '\t'
        print line.strip()
    print '----------------'


#############################################################################################
def aft_bus(index_token, tag, command):
    split_tag = tag.split('\t')
    # if (index_token - 5) > 0:
    #     tags_token = split_tag[(index_token - 5):index_token]
    # else:
    #     tags_token = split_tag[0:index_token]

    tags_token = split_tag[index_token:(len(split_tag) - 1)]

    if command == 'adj':
        if 'A' in tags_token:
            return True
        else:
            return False
    elif command == 'adverb':
        if 'R' in tags_token:
            return True
        else:
            return False
    elif command == 'verb':
        if 'V' in tags_token:
            return True
        else:
            return False


def aft_token_bus(sent, tag, command):
    split_sent = sent.split('\t')

    flag = False
    for index in range(0, len(split_sent)):
        token = split_sent[index]
        if 'bus' in token:
            flag = aft_bus(index, tag, command)
        if flag is True:
            break
    return flag


def aft_POS(sents_tags, sents_event, command):
    # check the part-of-speech whether the previous token is adj, adverb or verb
    sents, tags = sents_tags[0], sents_tags[1]
    list_gt, list_aftPOS = list(), list()

    for index in range(0, len(sents_event)):
        sent, tag = sents[index], tags[index]
        flag = aft_token_bus(sent, tag, command)

        # get the label for ground truth
        split_line = sents_event[index].split('\t')
        label = split_line[1]
        list_gt.append(int(label))

        # get the label for before part-of-speech
        if flag is True:
            list_aftPOS.append(1)
            # print sent
            # print tag
        else:
            list_aftPOS.append(0)

        if (flag is True) and (int(label) == 1):
            print sent
            print tag

    matrix = confusion_matrix(list_aftPOS, list_gt)
    for value in matrix:
        line = ''
        for each in value:
            line = line + str(each) + '\t'
        print line.strip()
    print '----------------'


#############################################################################################
#############################################################################################
if __name__ == '__main__':
    path_pos = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event'
    name_pos = 'EventsLabelingTask_completed_part_of_speech.txt'
    tags = load_file(path_pos, name_pos)
    sents_tags = convert_POS(tags)

    events = ['wait', 'missing', 'skip', 'slow', 'accident', 'crowd']
    path_event = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver3'

    for event in events:
        print 'Event --- ' + event
        list_sentences = load_file(path_event, event + '.csv')
        # interjection(sents_tags, list_sentences)
        # bef_POS(sents_tags, list_sentences, command='adj')
        bef_POS(sents_tags, list_sentences, command='adverb')
        # bef_POS(sents_tags, list_sentences, command='verb')

        # aft_POS(sents_tags, list_sentences, command='adj')
        # aft_POS(sents_tags, list_sentences, command='adverb')
        # aft_POS(sents_tags, list_sentences, command='verb')

    # list_tag = sorted(count_pos(sents_tags[1]))
    # for value in list_tag:
    #     print value
    # print len(list_tag)
