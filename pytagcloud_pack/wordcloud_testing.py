__author__ = 'vdthoang'
from os import path
import image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from pytagcloud_pack.image_bsv import grey_color_func

text = 'Bunch Jam Crowd Delay Kill Breakdown Aircon Accident'
# text = '960 960 176 176 176 962 962'

# text = str(960) + ' ' + str('960') + ' ' + str('76')
# Generate a word cloud image
# wordcloud = WordCloud().generate(str(text))

# text_freq=[('Bunch',1), ('jam', 1), ('delay', 1)]
# wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
# plt.axis("off")
# plt.imshow(wordcloud)
# plt.show()

# take relative word frequencies into account, lower max_font_size
wordcloud = WordCloud(max_words=100, margin=10).generate_from_text(text)
plt.axis("off")
plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3))
plt.show()
# plt.savefig('Events.jpg', dpi=500)

# wordcloud = WordCloud(background_color="white", max_words=100, margin=10, max_font_size=40, min_font_size=40).generate_from_text(text)
# plt.imshow(wordcloud)
# plt.axis("off")
# # plt.savefig('img/Events.jpg', dpi=1000)
# plt.show()