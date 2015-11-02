__author__ = 'vdthoang'
from main.loadFile import load_file
import bs4
import requests
import sys


reload(sys)
sys.setdefaultencoding('utf8')


def htmlTitle(url):
    r = requests.get(url)
    html = bs4.BeautifulSoup(r.text, 'lxml')
    return html.title.text.strip()


def detectUrl(text):
    split_text = text.lower().strip().split()
    text_title = ''
    for token in split_text:
        # check if token is url or not
        if token.startswith('http'):
            title = htmlTitle(token)
            text_title = text_title + ' ' + title
        else:
            text_title = text_title + ' ' + token
    return text_title.strip()


def getTitle(texts):
    # texts_Title = list()
    for i in range(2071, len(texts)):
        text, text_add = texts[i], ''
        try:
            text_add = detectUrl(text)
            print detectUrl(text)
        except UnicodeEncodeError:
            text_add = text
            print text


####################################################################################################
####################################################################################################
def getNumLink(text):
    split_text = text.lower().strip().split()
    links = list()
    for token in split_text:
        # check if token is url or not
        if token.startswith('http'):
            links.append(token)
    return len(links)


def events_list(texts):
    events = list()
    for text in texts:
        split_text = text.split('\t')
        tweet, event = split_text[0], split_text[1:]
        for each in event:
            split_each = each.split(':')
            name = split_each[0]

            if name.lower() not in events:
                events.append(name.lower())
    events = sorted(events)
    print len(events), events
    return events


def statistUrl(texts):
    events = events_list(texts)
    for event in events:
        totalLink = 0
        for text in texts:
            flag = False

            split_text = text.split('\t')
            tweet, list_event = split_text[0], split_text[1:]
            for each in list_event:
                split_each = each.split(':')
                name = split_each[0]

                if name.lower() == event:
                    flag = True
                    break
            if flag is True:
                numLink = getNumLink(tweet)
                totalLink += numLink
        print event + '\t' + str(totalLink)


if __name__ == '__main__':
    # TWITTER
    path_ = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_event'
    name_ = 'Philips_twitter_labeledComplete.txt'
    list_lbl = load_file(path_, name_)
    # getTitle(list_lbl)
    statistUrl(list_lbl)
