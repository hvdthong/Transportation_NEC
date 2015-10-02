__author__ = 'vdthoang'
import MySQLdb
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from pytagcloud import create_tag_image, make_tags
from pytagcloud import LAYOUT_MIX, LAYOUTS, LAYOUT_HORIZONTAL, LAYOUT_MOST_HORIZONTAL
import random
import matplotlib.patches as mpatches


def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

def red_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return (182,16,36)

###########################################################################################
###########################################################################################
def img_event_svc(event, database):
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="ducthong", # your password
                      db="2015_allschemas") # name of the data base
    cur = db.cursor()

    if (database == 'Sgforums'):
        sql = "select no, count(distinct post_id) as cnt from posts_ver2_events_service where events = '" + event \
              + "' group by no order by cnt desc" ## sgforums
    elif (database == 'Twitter'):
        sql = "select no, count(distinct tweetID) as cnt from tweet_2015_ver4_events_service where events = '" + event \
              + "' group by no order by cnt desc" ## twitter
    elif (database == 'Facebook'):
        sql = "select no, count(distinct facebookID) as cnt from facebook_2015_busnews_ver2_events_service where events = '" + event \
              + "' group by no order by cnt desc" ## facebook
    print sql

    string = ''
    cur.execute(sql)
    for row in cur.fetchall():
        try:
            svc = row[0]
            cnt = row[1]

            for i in range(0, cnt):
                string = string + ' ' + svc
        except ValueError:
            return 0 ## stop the proecss

    if (len(string) == 0):
        return 0; ##dononthing
    else:
        wordcloud = WordCloud(max_words=100, margin=10).generate(string)
        plt.title(database + ':' + event, fontsize=30)
        plt.imshow(wordcloud.recolor(random_state=3))
        plt.axis("off")
        plt.savefig('img/' + database + '_' + event + '.jpg', dpi=300)

def img_popular_svc(database):
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="ducthong", # your password
                      db="2015_allschemas") # name of the data base
    cur = db.cursor()

    if (database == 'Sgforums'):
        sql = 'select no, count(distinct post_id) as cnt from posts_ver2_events_service group by no order by cnt desc'
    elif (database == 'Twitter'):
        sql = 'select no, count(distinct tweetID) as cnt from tweet_2015_ver4_events_service group by no order by cnt desc'
    elif (database == 'Facebook'):
        sql = 'select no, count(distinct facebookID) as cnt from facebook_2015_busnews_ver2_events_service group by no order by cnt desc'
    print sql

    string = ''
    cur.execute(sql)
    for row in cur.fetchall():
        svc = row[0]
        cnt = row[1]

        for i in range(0, cnt):
            string = string + ' ' + svc
    if (len(string) == 0):
        return 0; ##dononthing
    else:
        wordcloud = WordCloud(max_words=100, margin=10).generate(string)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.savefig('img/' + database + '_allevents.jpg', dpi=500)

###########################################################################################
###########################################################################################
def img_event_road(event, database):
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="ducthong", # your password
                      db="2015_allschemas") # name of the data base
    cur = db.cursor()
    if (database == 'Sgforums'):
        sql = "select road, count(distinct post_id) as cnt from posts_ver2_events_road where events = '" + event \
              + "' group by road order by cnt desc" ## sgforums
    elif (database == 'Twitter'):
        sql = "select road, count(distinct tweetID) as cnt from tweet_2015_ver4_events_road where events = '" + event \
              + "' group by road order by cnt desc" ## twitter
    elif (database == 'Facebook'):
        sql = "select road, count(distinct facebookID) as cnt from facebook_2015_busnews_ver2_events_road where events = '" + event \
              + "' group by road order by cnt desc" ## twitter
    print sql

    string = ''
    cur.execute(sql)
    for row in cur.fetchall():
        try:
            svc = row[0]
            cnt = row[1]

            svc_split = svc.split()
            svc_new = ''
            for token in svc_split:
                svc_new = svc_new + '_' + token

            svc_new = svc_new[1:]

            for i in range(0, cnt):
                string = string + ' ' + svc_new
        except ValueError:
            return 0 ## stop the proecss

    if (len(string) == 0):
        return 0; ##dononthing
    else:
        wordcloud = WordCloud(max_words=100, margin=10).generate(string)
        plt.title(database + ':' + event, fontsize=30)
        plt.imshow(wordcloud.recolor(random_state=3))
        plt.axis("off")
        plt.savefig('img/' + database + '_' + event + '_road.jpg', dpi=300)

def img_popular_road(database):
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="ducthong", # your password
                      db="2015_allschemas") # name of the data base
    cur = db.cursor()
    if (database == 'Sgforums'):
        sql = 'select road, count(distinct post_id) as cnt from posts_ver2_events_road group by road order by cnt desc'
    elif (database == 'Twitter'):
        sql = 'select road, count(distinct tweetID) as cnt from tweet_2015_ver4_events_road group by road order by cnt desc'
    elif (database == 'Facebook'):
        sql = 'select road, count(distinct facebookID) as cnt from facebook_2015_busnews_ver2_events_road group by road order by cnt desc'
    print sql

    string = ''
    cur.execute(sql)
    for row in cur.fetchall():
        try:
            svc = row[0]
            cnt = row[1]

            svc_split = svc.split()
            svc_new = ''
            for token in svc_split:
                svc_new = svc_new + '_' + token

            svc_new = svc_new[1:]

            for i in range(0, cnt):
                string = string + ' ' + svc_new
        except ValueError:
            return 0 ## stop the proecss

    if (len(string) == 0):
        return 0; ##dononthing
    else:
        wordcloud = WordCloud(max_words=100, margin=10).generate(string)
        plt.title(database + ':allevents', fontsize=30)
        plt.imshow(wordcloud.recolor(random_state=3))
        plt.axis("off")
        plt.savefig('img/' + database + '_allevents_road.jpg', dpi=300)

if __name__ == '__main__':

    events = ['accident', 'air-con', 'breakdown', 'bunch', 'crowd', 'delay', 'jam', 'kill']

    # database = 'Sgforums'
    # for event in events:
    #     img_event_svc(event, database)
    # img_popular_svc(database)
    #######################################################################################
    #######################################################################################
    # database = 'Twitter'
    # for event in events:
    #     img_event_svc(event, database)
    # img_popular_svc(database)
    #######################################################################################
    #######################################################################################
    # database = 'Facebook'
    # for event in events:
    #     img_event_svc(event, database)
    # img_popular_svc(database)

    #######################################################################################
    #######################################################################################
    #######################################################################################
    #######################################################################################
    # database = 'Sgforums'
    # for event in events:
    #     img_event_road(event, database)
    # img_popular_road(database)
    #######################################################################################
    #######################################################################################
    # database = 'Twitter'
    # for event in events:
    #     img_event_road(event, database)
    # img_popular_road(database)
    #######################################################################################
    #######################################################################################
    # database = 'Facebook'
    # for event in events:
    #     img_event_road(event, database)
    # img_popular_road(database)