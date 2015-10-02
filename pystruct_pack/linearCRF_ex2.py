__author__ = 'vdthoang'
from pystruct.datasets import load_letters
from pystruct.models import ChainCRF, GraphCRF
from pystruct.learners import FrankWolfeSSVM
from pystruct.learners import NSlackSSVM
from time import time

import numpy as np
letters = load_letters()

features, y, folds = letters['data'], letters['labels'], letters['folds']
features, y = np.array(features), np.array(y)

print 'Shape of features:', features.shape
list_y = []
for i in range(0, len(features)):
    # print len(features[i]), len(y[i])
    # for each in features[i]:
    #     print len(each)
    # break
    list_y.append(len(y[i]))
print 'Shape of targets:', y.shape
print 'Max length:', max(list_y)

features_train, features_test = features[folds == 1], features[folds != 1]
y_train, y_test = y[folds == 1], y[folds != 1]

f_t = features_train
X_train = [(features_i, np.vstack([np.arange(f_t.shape[0] - 1), np.arange(1, f_t.shape[0])])) for features_i in f_t]
print 'Loading X_train'
f_test = features_test
X_test = [(features_i, np.vstack([np.arange(f_t.shape[0] - 1), np.arange(1, f_t.shape[0])])) for features_i in f_test]
print 'Loading X_test'

start = time()
model = GraphCRF(directed=True, inference_method="max-product")
ssvm = FrankWolfeSSVM(model=model, C=.1, max_iter=10)
ssvm.fit(X_train, y_train)
#
print 'accuracy of GraphCRF %f:' % ssvm.score(X_test, y_test), ' time spend: %f' % (time()-start)
