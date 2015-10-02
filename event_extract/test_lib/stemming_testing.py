__author__ = 'vdthoang'
word = 'bitten'
word = 'simplified'
word = 'communities'
word = 'air-condition'
word = 'air-con'
word = 'breakdown'
word = 'bunch'
word = 'airconditional'
word = 'squeeze'
word = 'sv'
word = 'svc'
word = 'DDs'
word = 'sds'
word = 'buses'
word = 'services'

# from nltk.stem.wordnet import WordNetLemmatizer
# lmtzr = WordNetLemmatizer()
# print (lmtzr.lemmatize(word))

from nltk.stem import PorterStemmer

port = PorterStemmer()
print (port.stem(word))