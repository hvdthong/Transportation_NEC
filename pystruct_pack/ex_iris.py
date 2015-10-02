__author__ = 'vdthoang'
from time import time
import numpy as np

from sklearn.datasets import load_iris
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn import metrics

from pystruct.models import GraphCRF
from pystruct.learners import NSlackSSVM

iris = load_iris()
X, y = iris.data, iris.target

# make each example into a tuple of a single feature vector and an empty edge
# list
X_ = [(np.atleast_2d(x), np.empty((0, 2), dtype=np.int)) for x in X]
Y = y.reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(X_, Y)

pbl = GraphCRF(inference_method='unary')
svm = NSlackSSVM(pbl, C=100)


start = time()
svm.fit(X_train, y_train)
time_svm = time() - start
y_pred = np.vstack(svm.predict(X_test))
print("Score with pystruct crf svm: %f (took %f seconds)" % (np.mean(y_pred == y_test), time_svm))

# clf = SGDClassifier()
# clf.fit(X_train, y_train)
# y_pred = clf.predict(X_test)
# print 'Score with SGDClassifier: %f' %(metrics.accuracy_score(y_test, y_pred))

x = '14567'
y = '12354'
z = map(''.join, zip(x, y))
print z
t = '10001'
m = map(''.join, zip(z, t))
print m


