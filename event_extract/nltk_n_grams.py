__author__ = 'vdthoang'
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from nltk import FreqDist

sentence = 'this is a foo bar sentences and i want to ngramize it this this'
# n = 3
# list_grams = ngrams(sentence.split(), n)
#
# for grams in list_grams:
#     string = ''
#     for value in grams:
#         string = string + ' ' + value
#     print (string.strip())

fdist = FreqDist()
tokens = word_tokenize(str(sentence))
fdist.update(tokens)

for value in fdist.most_common():
    print value

i = 11
for i in range(0, 10):
    i = i + 2
    print 'testing'

text = 'Mount Batten Rd Haig Rd Sims Ave'
split_text = text.split('Rd')
for value in split_text:
    print value
