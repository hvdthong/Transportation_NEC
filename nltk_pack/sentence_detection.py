__author__ = 'vdthoang'

from nltk.tokenize import sent_tokenize

import sys
# make the default is 'utf-8'
reload(sys)
sys.setdefaultencoding('utf8')


# text = 'this is a sent tokenize test. this is sent two. is this sent three? sent 4 is cool!!! Now it is your turn.'
# text = 'Bus 19 so crowded. Luckily bus 37 came at the right time.'
# text = 'bus 30, why you so damn slow?!'
# text = '6 bus 859 and 3 bus 882 alr and no bus 858 wow kill me'
text = 'U guys should have to provide  free transport from yishun station to bishan interchange station.when there is a faulty issues. 😠😠😠😠😠'
sent_tokenize_list = sent_tokenize(text)

for value in sent_tokenize_list:
    print value
print len(sent_tokenize_list)
