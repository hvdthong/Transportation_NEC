__author__ = 'vdthoang'
import gensim
from scipy import spatial

sentences = [['I', 'like', 'deep', 'learning'], ['I', 'Deep', 'NLP'], ['I', 'enjoy', 'flying']]
model = gensim.models.Word2Vec(sentences, size=3, window=2, min_count=1, workers=4)
# model.save_word2vec_format('text.model.bin', binary=True)
# print model.most_similar(['like'])
# print model.vocab

# print model.save('word2vec_ex')
print model.most_similar(['deep'])
# for word in model.index2word:
#     print word
# for vector in model.syn0norm:
#     print vector

for i in range(0, len(model.index2word)):
    print model.index2word[i], model.syn0norm[i]

print '----------'
v1 = model.syn0norm[5]
print v1
v2 = model.syn0norm[6]
print v2

result = 1 - spatial.distance.cosine(v1, v2)
print result