__author__ = 'vdthoang'
from pystruct.datasets import load_letters

import numpy as np
from numpy.testing import assert_array_equal, assert_equal
from nose.tools import assert_raises
from pystruct.models import ChainCRF
from pystruct.learners import FrankWolfeSSVM

# letters = load_letters()
# print letter
# X, y, folds = letters['data'], letters['labels'], letters['folds']
# print len(X)
# print X[0], len(X[0])
# print X[1], len(X[1])

rnd = np.random.RandomState(0)
x = rnd.normal(size=(13, 5))
print x
y = rnd.randint(3, size=13)
print y
# crf = ChainCRF(n_states=3, n_features=5)
# # no-op
# crf.initialize([x], [y])
#
# #test initialization works
# crf = ChainCRF()
# crf.initialize([x], [y])
# assert_equal(crf.n_states, 3)
# assert_equal(crf.n_features, 5)
#
# crf = ChainCRF(n_states=2)
# assert_raises(ValueError, crf.initialize, X=[x], Y=[y])
# print 'pass'
list_x, list_y = [], []
list_x.append(x)
list_x.append(x)
list_y.append(y)
list_y.append(y)

crf = ChainCRF()
ssvm = FrankWolfeSSVM(model=crf, C=.1, max_iter=10)
ssvm.fit(np.array(list_x), np.array(list_y))

print np.array(list_x)

x_test = rnd.normal(size=(11, 5))
list_x_test = []
list_x_test.append(x_test)
print ssvm.predict(np.array(list_x_test))

pred = ssvm.predict(np.array(list_x_test))
for value in pred:
    print value

# list_1 = [1, 2 ,3]
# list_2 = [4, 0 ,2]
# list_all = []
# list_all.append(list_1)
# list_all.append(list_2)
# print np.array(list_all)