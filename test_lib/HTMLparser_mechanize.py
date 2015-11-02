__author__ = 'vdthoang'

# import mechanize
# br = mechanize.Browser()
# br.open('https://t.co/NBhpVtoMmt')
#
# # follow second link with element text matching regular expression
# response1 = br.follow_link(text_regex=r"cheese\s*shop", nr=1)
# assert br.viewing_html()
# print br.title()
# print response1.geturl()
# print response1.info()  # headers
# print response1.read()  # body

import requests
r = requests.get('https://t.co/NBhpVtoMmt')
import bs4
html = bs4.BeautifulSoup(r.text, 'lxml')
print html.title.text.strip()
