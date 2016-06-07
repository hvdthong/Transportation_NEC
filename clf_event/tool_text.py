__author__ = 'vdthoang'
from stemming.porter2 import stem
from nltk.corpus import stopwords
from main.loadFile import load_file
from main.writeFile import write_file


def bigrams_text(string):
    # input: a string
    # output: an original string + bigrams string

    tokens = string.split()
    first_tokens, second_tokens = tokens[:-1], tokens[1:]

    bigram_string = ''
    for i in range(0, len(first_tokens)):
        bigram_string += first_tokens[i] + '_' + second_tokens[i] + ' '
    return string + ' ' + bigram_string.strip()


def stemming_text(string):
    # input: a string
    # output: a new stemming string
    tokens = string.split()
    stem_string = ''
    for token in tokens:
        stem_string += stem(token) + ' '
    return stem_string.strip()


###########################################################
###########################################################
def remove_stopWords(string):
    # input: a string
    # output: a new string after removing stop words
    tokens = string.split()
    stopW_string = ''
    for token in tokens:
        if token not in stopwords.words('english'):
            stopW_string += token + ' '
    return stopW_string.strip()


def stemming_stopWords_text(list_, path, name):
    new_list = list()
    for i in range(0, len(list_)):
        line = list_[i]
        split_line = line.split('\t')
        event, label, text = split_line[0], split_line[1], split_line[2]
        new_text = stemming_text(remove_stopWords(text)).strip()
        new_line = event + '\t' + label + '\t' + new_text
        new_list.append(new_line)
        print i
    write_file(path, name + '_stemming_removeStop', new_list)

if __name__ == '__main__':
    # string = 'more is said than done'
    # print bigrams_text(string)
    #
    # string = 'house houses housed factionally identified'
    # print stemming_text(string)
    #
    # print remove_stopWords(string)

    # using for Sgforums
    # path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_classification_events/detectAllEvents_ver2'
    # events = ['bunch', 'crowd']
    #
    # for event in events:
    #     list_ = load_file(path, event + '.csv')
    #     stemming_stopWords_text(list_, path, event)

    # using for Facebook
    path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_event/detectAllEvents_ver2'
    events = ['suggestion', 'wait', 'complaint', 'compliment', 'skip']

    for event in events:
        list_ = load_file(path, event + '.csv')
        stemming_stopWords_text(list_, path, event)