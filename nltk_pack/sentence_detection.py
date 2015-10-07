__author__ = 'vdthoang'

from nltk.tokenize import sent_tokenize
import sys
# make the default is 'utf-8'
reload(sys)
sys.setdefaultencoding('utf8')


text = 'this is a sent tokenize test. this is sent two. is this sent three? sent 4 is cool! Now it is your turn.'
text = 'Bus 19 so crowded. Luckily bus 37 came at the right time.'
sent_tokenize_list = sent_tokenize(text)

for value in sent_tokenize_list:
    print value

print len(sent_tokenize_list)
