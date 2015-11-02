__author__ = 'vdthoang'
from sklearn.datasets import fetch_20newsgroups
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.cross_validation import cross_val_score, KFold
from scipy.stats import sem
import numpy as np

news = fetch_20newsgroups(subset='all')
# print type(news.data), type(news.target), type(news.target_names)
# print len(news.target_names), news.target_names
#
# for value in news.target_names:
#     print value
#
# print len(news.data)
# print len(news.target)

# for value in news.target:
#     print value

# for i in range(0, len(news.data)):
#     print news.target[i]
#     print '----------------------------------------------------'
#     print news.data[i].encode('utf-8')

# print news.data[0]
# print '----------------------------------------------------'
# print '----------------------------------------------------'
# print news.target[0], news.target_names[news.target[0]]

clf_1 = Pipeline([('vect', CountVectorizer()), ('clf', MultinomialNB())])
clf_2 = Pipeline([('vect', HashingVectorizer(non_negative=True)), ('clf', MultinomialNB())])
clf_3 = Pipeline([('vect', TfidfVectorizer()), ('clf', MultinomialNB())])
# clf_4 = Pipeline([('vect', CountVectorizer()), ('clf', LogisticRegression())])
# clf_5 = Pipeline([('vect', CountVectorizer()), ('clf', DecisionTreeClassifier())])


def evaluate_cross_validation(clf, X, y, K):
    # create a k-fold croos validation iterator of k=5 folds
    cv = KFold(len(y), K, shuffle=True, random_state=0)
    # by default the score used is the one returned by score method of the estimator (accuracy)
    scores = cross_val_score(clf, X, y, cv=cv)
    print scores
    print ("Mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(scores), sem(scores))

# clfs = [clf_1, clf_2, clf_3]
# # # clfs = [clf_4]
# # # clfs = [clf_5]
# for clf in clfs:
#     evaluate_cross_validation(clf, news.data, news.target, 2)

# evaluate_cross_validation(clf_3, news.data, news.target, 2)
# clf_6 = Pipeline([('vect', TfidfVectorizer(token_pattern=ur"\b[a-z0-9_\-\.]+[a-z][a-z0->>> 9_\-\.]+\b")), ('clf', MultinomialNB())])
# evaluate_cross_validation(clf_6, news.data, news.target, 2)


string_1 = 'hello 2 i 24 am thong homework'
string_2 = 'thong 2 is testing'
string_3 = 'thong is'
list_str = [string_1, string_2, string_3]
vectorizer = CountVectorizer(token_pattern='[A-Za-z0-9]*')
data_cntVec = vectorizer.fit(list_str)
cons_ftr = data_cntVec.transform(list_str)

print data_cntVec.vocabulary_
print cons_ftr.shape
print cons_ftr.shape[0]
print cons_ftr

# for value in range(0, cons_ftr.shape[0]):
#     cons_str = cons_ftr[value]
#     print value, cons_ftr[value]

# from scipy.sparse import csc_matrix, hstack
# add_ftr_1 = '(0, 12) \t 1 \n'
# add_ftr_2 = '(1, 12) \t 0 \n'
# add_ftr_3 = '(2, 12) \t 0 \n'
# list_ = [add_ftr_1, add_ftr_2, add_ftr_3]
# csc_add_ftr = csc_matrix(list_)
# csc_ = cons_ftr.tocsc()
# print csc_

# print vectorizer.get_feature_names()
#
# for value in vectorizer.get_feature_names():
#     print value
#
# for value in data_cntVec.vocabulary_:
#     print value

cv = CountVectorizer(vocabulary=['hot', 'cold', 'old'])
cv = cv.fit_transform(['pease porridge hot hot', 'pease porridge cold hot old', 'pease porridge in the pot', 'nine days old']).toarray()
print cv


