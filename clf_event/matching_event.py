__author__ = 'vdthoang'

from main.loadFile import load_file
from clf_event.CLF_event import load_event_x_y
from sklearn.metrics import confusion_matrix
import sys
import numpy as np
from main.writeFile import write_file
from operator import itemgetter


# make the default is 'utf-8'
reload(sys)
sys.setdefaultencoding('utf8')


def matching_eventText(X, Y, event, call):
    pred = list()
    for value in X:
        if event in value:
            pred.append('1')
        else:
            pred.append('0')

    matrix = confusion_matrix(pred, Y)
    for value in matrix:
        line = ''
        for each in value:
            line = line + str(each) + '\t'
        print line.strip()
    print '----------------'

    list_print = list()
    if call == 'PrintPredicted':
        for index in range(0, len(pred)):
            tweet, pred_value, truth_value = X[index], pred[index], Y[index]
            list_ = list()
            list_.append(index), list_.append(pred_value), list_.append(truth_value), list_.append(tweet)
            list_print.append(list_)

        list_print = sorted(list_print, key=itemgetter(0))  # sorted list based on index
        list_write = list()
        for value in list_print:
            print str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2]) + '\t' + str(value[3])
            list_write.append(str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2]) + '\t' + str(value[3]))
        write_file(path, event + '_match', list_write)


if __name__ == '__main__':
    # TWITTER
    # events = ['missing', 'delay']
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents'
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets'

    events = ['wait', 'slow', 'missing']
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver2'
    for event in events:
        list_sentences = load_file(path, event + '.csv')
        print 'Running event: ', event
        list_all = load_event_x_y(list_sentences)
        X, Y = np.array(list_all[0]), np.array(list_all[1])
        matching_eventText(X, Y, event, call='PrintPredicted')
