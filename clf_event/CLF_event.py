__author__ = 'vdthoang'
from main.loadFile import load_file
from sklearn.cross_validation import KFold, StratifiedKFold
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
import sys
from CRF_labeling.filterText_CRF import filterTxt_CRF
import numpy as np
from main.filter_text import filter_token
import chardet
from operator import itemgetter
from main.writeFile import write_file
from clf_event.preprocessText import clean_url, remove_stopwords, clean_number
from clf_event.pos_tagging import convert_POS, contain_interjection, bef_token_bus, aft_token_bus
import math
from clf_event.tool_text import bigrams_text, remove_stopWords, stemming_text


# make the default is 'utf-8'
reload(sys)
sys.setdefaultencoding('utf8')


def load_event_x_y(event, sentences, command):
    all, X, Y = list(), list(), list()
    for sent in sentences:
        split_sent = sent.strip().split('\t')
        label = split_sent[1]  # load label
        text = split_sent[2]  # load text

        if command == 'preprocessText':
            text = clean_url(text)
        elif command == 'bigram':
            text = bigrams_text(text)
        elif command == 'stemming_stopWords':
            text = remove_stopWords(stemming_text(text))

        if event == 'slow':
            if 'slow' in text:
                text += ' slowevent'

        X.append(text), Y.append(label)
        # print text
        # X.append(filter_token(text)), Y.append(label)
    # decoded = [x.decode(chardet.detect(x)['encoding']) for x in X]
    # all.append(decoded), all.append(Y)

    if command == 'part-of-speech':
        path_pos = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event'
        name_pos = 'EventsLabelingTask_completed_part_of_speech.txt'
        pos_loading = load_file(path_pos, name_pos)
        sents_tags = convert_POS(pos_loading)

        new_sents, sents, tags = list(), sents_tags[0], sents_tags[1]

        for index in range(0, len(sents)):
            sent, tag = sents[index], tags[index]
            original_sent = X[index]

            # check if the sentence contains interjection
            flag_interjection = contain_interjection(sent, tags)
            if flag_interjection is True:
                original_sent = original_sent.strip() + ' ' + 'interjection'

            # check the before token is adj, adv or verb
            flag_bef_adj = bef_token_bus(sent, tag, 'adj')
            if flag_bef_adj is True:
                original_sent = original_sent.strip() + ' ' + 'bef_adj'
            flag_bef_adv = bef_token_bus(sent, tag, 'adverb')
            if flag_bef_adv is True:
                original_sent = original_sent.strip() + ' ' + 'bef_adv'
            flag_bef_verb = bef_token_bus(sent, tag, 'verb')
            if flag_bef_verb is True:
                original_sent = original_sent.strip() + ' ' + 'bef_verb'

            # check if the after token is adj, adv or verb
            flag_aft_adj = aft_token_bus(sent, tag, 'adj')
            if flag_aft_adj is True:
                original_sent = original_sent.strip() + ' ' + 'aft_adj'
            flag_aft_adv = aft_token_bus(sent, tag, 'adverb')
            if flag_aft_adv is True:
                original_sent = original_sent.strip() + ' ' + 'aft_adv'
            flag_aft_verb = aft_token_bus(sent, tag, 'verb')
            if flag_aft_verb is True:
                original_sent = original_sent.strip() + ' ' + 'aft_verb'
            new_sents.append(original_sent)

    if command == 'part-of-speech_all':
        path_pos = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event'
        name_pos = 'EventsLabelingTask_completed_part_of_speech.txt'
        pos_loading = load_file(path_pos, name_pos)
        sents_tags = convert_POS(pos_loading)

        new_sents, sents, tags = list(), sents_tags[0], sents_tags[1]
        for index in range(0, len(sents)):
            sent, tag = sents[index], tags[index]
            original_sent = X[index]

            new_tag_text = ''
            split_tag = tag.split('\t')
            for each in split_tag:
                new_tag_text += ' pos_' + each + '_speech'
                # new_tag_text += ' ' + each

            original_sent = original_sent.strip() + ' ' + new_tag_text.strip()
            new_sents.append(original_sent)

    if command == 'part-of-speech' or command == 'part-of-speech_all':
        all.append(new_sents), all.append(Y)
    else:
        all.append(X), all.append(Y)
    return all


def clf_event_running(path, event, name_clf, X, Y, clf, K, command, call):
    if command == 'KFold':
        cv = KFold(len(X), K, shuffle=True, random_state=0)
    elif command == 'StratifiedKFold':
        cv = StratifiedKFold(Y, K)
    else:
        print 'Need a correct command'
        quit()
    # print cv.n_folds

    list_print = list()

    for traincv, testcv in cv:
        X_train = X[traincv]
        X_test = X[testcv]
        y_train, y_test = Y[traincv], Y[testcv]

        MIN_DF = 2
        # MIN_DF = 5
        vec = CountVectorizer(lowercase=True, min_df=2)
        vec = vec.fit(X_train)

        # vec = CountVectorizer(lowercase=True)

        # vec = TfidfVectorizer(lowercase=True, min_df=2)
        # vec = TfidfVectorizer(lowercase=True, min_df=5)
        # vec = vec.fit(X)

        X_train_trans = vec.transform(X_train)
        X_test_trans = vec.transform(X_test)

        # transformer = TfidfTransformer()
        # X_train_trans, X_test_trans = transformer.fit_transform(X_train_trans), transformer.fit_transform(X_test_trans)

        clf.fit(X_train_trans, y_train)  # training model
        y_test_pred = clf.predict(X_test_trans)

        matrix = confusion_matrix(y_test_pred, y_test)
        for value in matrix:
            line = ''
            for each in value:
                line = line + str(each) + '\t'
            print line.strip()
        print '----------------'

        # cnt = 0
        # for index in testcv:
        #     pred, truth = y_test_pred[cnt], y_test[cnt]
        #
        #     # if pred != truth:
        #     print index, str(pred), str(truth), X[index]
        #     cnt += 1

        if call == 'PrintPredicted':
            cnt = 0
            for index in testcv:
                tweet, pred, truth = X[index], y_test_pred[cnt], y_test[cnt]
                list_ = list()
                list_.append(index), list_.append(pred), list_.append(truth), list_.append(tweet)
                list_print.append(list_)
                cnt += 1

        elif call == 'ProbScore':  # get the probability score
            y_test_decision, y_probScore = clf.decision_function(X_test_trans), list()
            for x in y_test_decision:
                prob = 1 / (1 + math.exp(-x))
                y_probScore.append(prob)

            cnt = 0
            for index in testcv:
                tweet, pred, truth, prob = X[index], y_test_pred[cnt], y_test[cnt], y_probScore[cnt]
                list_ = list()
                list_.append(index), list_.append(prob), list_.append(pred), list_.append(truth), list_.append(tweet)
                list_print.append(list_)
                cnt += 1

    if call == 'PrintPredicted':
        list_print = sorted(list_print, key=itemgetter(0))  # sorted list based on index
        list_write = list()
        for value in list_print:
            print str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2]) + '\t' + str(value[3])
            list_write.append(str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2]) + '\t' + str(value[3]))
        write_file(path, event + '_' + name_clf, list_write)

    elif call == 'ProbScore':
        list_print = reversed(sorted(list_print, key=itemgetter(1)))  # sorted list based on index
        list_write = list()
        for value in list_print:
            print str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2]) + '\t' + str(value[3]) + '\t' + str(value[4])
            list_write.append(str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2]) + '\t' + str(value[3]) + '\t' + str(value[4]))
        write_file(path, event + '_' + name_clf + '_probScore', list_write)

################################################################################################
################################################################################################
if __name__ == '__main__':
    # TWITTER
    # events = ['missing', 'delay']
    # events = ['delay']
    # events = ['wait', 'slow', 'missing']
    # events = ['missing', 'slow']
    # events = ['wait']
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents'
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets'
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver2'
    # events = ['busstop', 'transist']

    ################################################################################################
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event/detectAllEvents/allTweets_ver3'
    events = ['wait', 'missing', 'skip', 'slow', 'accident', 'crowd']
    # events = ['wait_slow']
    # events = ['busstop', 'transist']
    # events = ['crowd']

    # sentiment
    # events = ['wait_sentiment', 'missing_sentiment', 'skip_sentiment', 'slow_sentiment', 'accident_sentiment', 'crowd_sentiment']

    # FACEBOOK
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event/detectAllEvents'
    # events = ['wait', 'complaint', 'compliment', 'skip', 'crowd']

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event/detectAllEvents_ver2'
    # # events = ['wait', 'complaint', 'compliment', 'skip', 'suggestion']
    # # events = ['wait_ftrMatch', 'complaint_ftrMatch', 'compliment_ftrMatch', 'skip_ftrMatch', 'suggestion_ftrMatch']
    # events = ['complaint_stemming_removeStop', 'compliment_stemming_removeStop', 'skip_stemming_removeStop', 'suggestion_stemming_removeStop', 'wait_stemming_removeStop']

    # SGFORUMS
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_classification_events/detectAllEvents'
    # events = ['bunch', 'crowd']

    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_classification_events/detectAllEvents_ver2'
    # events = ['bunch', 'crowd']
    # events = ['bunch_ftrMatch', 'crowd_ftrMatch']
    # events = ['bunch_stemming_removeStop', 'crowd_stemming_removeStop']
    for event in events:
        list_sentences = load_file(path, event + '.csv')
        print 'Running event: ', event
        # list_all = load_event_x_y(event, list_sentences, command='preprocessText')
        # list_all = load_event_x_y(event, list_sentences, command='')
        # list_all = load_event_x_y(event='', list_sentences, command='part-of-speech')
        # list_all = load_event_x_y(event='', list_sentences, command='part-of-speech_all')
        # list_all = load_event_x_y(event, list_sentences, command='bigram')
        list_all = load_event_x_y(event, list_sentences, command='')

        X, Y = np.array(list_all[0]), np.array(list_all[1])
        # clf = MultinomialNB()
        # clf = LinearSVC(C=1.0, random_state=0, class_weight='auto', max_iter=100000)
        clf = LogisticRegression(max_iter=50000, solver='liblinear', tol=0.000001, class_weight='auto')

        # clf_event_running(X, Y, clf, K=5, command='KFold')
        # clf_event_running(path, event, 'LR', X, Y, clf, K=5, command='StratifiedKFold', call='PrintPredicted')
        # clf_event_running(path, event, 'LR', X, Y, clf, K=5, command='StratifiedKFold', call='ProbScore')
        clf_event_running(path, event, 'LR', X, Y, clf, K=5, command='StratifiedKFold', call='')
        # clf_event_running(path, event, 'POS', X, Y, clf, K=5, command='StratifiedKFold', call='')
        # clf_event_running(path, event, '', X, Y, clf, K=5, command='StratifiedKFold', call='')
        # clf_event_running(path, event, 'SVM_sentiment', X, Y, clf, K=5, command='StratifiedKFold', call='PrintPredicted')
