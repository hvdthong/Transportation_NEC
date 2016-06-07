__author__ = 'vdthoang'
from main.loadFile import load_file
from clf_event.CLF_event import load_event_x_y, clf_event_running
import numpy as np
from sklearn.svm import LinearSVC
from nec_demo.CRF_model_pred import load_demo_text
from sklearn.feature_extraction.text import CountVectorizer
from main.writeFile import write_file


def event_pred_model(event, X, Y, command):  # note that X is a list and Y is a array
    texts = load_demo_text(command)
    total_X = X + texts
    X_convert, X_pred, total_X_convert = np.array(X), np.array(texts), np.array(total_X)

    MIN_DF = 2
    vec = CountVectorizer(lowercase=True, min_df=MIN_DF)
    vec = vec.fit(total_X_convert)

    X_convert_trans, X_pred_trans = vec.transform(X_convert), vec.transform(X_pred)

    clf.fit(X_convert_trans, Y)  # training model
    y_pred = clf.predict(X_pred_trans)
    y_prob = clf.decision_function(X_pred_trans)

    max_prob, min_prob = max(y_prob), min(y_prob)
    list_write = list()
    for i in range(0, len(y_pred)):
        prob = (y_prob[i] - min_prob) / (max_prob - min_prob)
        print y_pred[i], prob, texts[i]

        # list_write.append(str(y_pred[i]) + '\t' + texts[i])
        list_write.append(str(y_pred[i]))

    if command == 'twitter':
        path_write = 'D:/Project/Transportation_SMU-NEC_collaboration/Data_demo_Dec_2015/twitter/events_pred'
        write_file(path_write, event, list_write)


if __name__ == '__main__':
    ################################################################################################
    # TWITTER
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver3'
    events = ['wait', 'missing', 'skip', 'slow', 'accident', 'crowd']

    for event in events:
        list_sentences = load_file(path, event + '.csv')
        print 'Running event: ', event
        list_all = load_event_x_y(event, list_sentences, '')
        X, Y = np.array(list_all[0]), np.array(list_all[1])
        clf = LinearSVC(C=1.0, random_state=0, class_weight='auto', max_iter=100000)
        event_pred_model(event, list_all[0], Y, command='twitter')