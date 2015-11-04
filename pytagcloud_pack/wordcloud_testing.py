__author__ = 'vdthoang'
from os import path
import image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from pytagcloud_pack.image_bsv import grey_color_func
from main.loadFile import load_file

# text = 'stop at from to singapore towards road around and like no bustp puasa those between frhmd'
# text = '960 960 176 176 176 962 962'

# text = str(960) + ' ' + str('960') + ' ' + str('76')
# Generate a word cloud image
# wordcloud = WordCloud().generate(str(text))

# text_freq=[('Bunch',1), ('jam', 1), ('delay', 1)]
# wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
# plt.axis("off")
# plt.imshow(wordcloud)
# plt.show()

# wordcloud = WordCloud(background_color="white", max_words=100, margin=10, max_font_size=40, min_font_size=40).generate_from_text(text)
# plt.imshow(wordcloud)
# plt.axis("off")
# # plt.savefig('img/Events.jpg', dpi=1000)
# plt.show()

# path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/twitter/labeling_CRF/crf_features'
# name = 'all_token_bef_bussvc.txt'
# name = 'all_token_bef_road.txt'
# name = 'all_token_bef_busstop.txt'

# path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/sgforums/20152207_singaporebuses_all_posts/labeling_CRF/crf_features'
# name = 'all_token_bef_bussvc.txt'
# name = 'all_token_bef_road.txt'
# name = 'all_token_bef_busstop.txt'
# split_name = name.split('.')
# name_write = split_name[0]
# list_text = load_file(path, name)

path = 'D:/Project/Transportation_SMU-NEC_collaboration/Data/facebook/BusNews/labeling_CRF/crf_features'
# name = 'all_token_bef_bussvc.csv'
# name = 'all_token_bef_road.csv'
name = 'all_token_bef_busstop.csv'
list_text = load_file(path, name)


text = ''
length = len(list_text)
for value in list_text:
    for i in range(length):
        text += value + ' '
    length -= 1
text = text.strip()

# take relative word frequencies into account, lower max_font_size
wordcloud = WordCloud(max_words=100, margin=10, background_color='white', stopwords=list()).generate_from_text(text)
plt.axis("off")
plt.imshow(wordcloud.recolor(random_state=3))
plt.show()
# plt.savefig(path + '/' + name_write + '.jpg', dpi=500)



