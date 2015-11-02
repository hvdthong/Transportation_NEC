__author__ = 'vdthoang'
from pystruct.datasets import load_letters
from pystruct.models import ChainCRF, GraphCRF
from pystruct.learners import FrankWolfeSSVM
from pystruct.learners import NSlackSSVM
from time import time

import numpy as np
letters = load_letters()

X, y, folds = letters['data'], letters['labels'], letters['folds']
# print type(X[0])
# print type(X)
#
# print type(y[0])
# print type(y)

# for value in X:
#     print value
#     print len(value)
#     break

X, y = np.array(X), np.array(y)
X_train, X_test = X[folds == 1], X[folds != 1]
y_train, y_test = y[folds == 1], y[folds != 1]

print X
print y

# list_y_value = []
# for i in range(0, len(X_train)):
#     print len(X_train[i]), len(y_train[i])
#
#     print y_train[i]
#     for value in y_train[i]:
#         if value not in list_y_value:
#             list_y_value.append(value)
#
# print list_y_value
# print sorted(list_y_value)
# print len(list_y_value)


# for value in X:
#     print value.shape
#
# print X_train.shape
# print y_train.shape
#
# print type(X_train)

# for value in y_train:
#     print value
#
# for i in range(0, len(X_train)):
#     if i == 15:
#         print X_train[i], len(X_train[i])
#         for f in X_train[i]:
#             print len(f)
#             break
#         print y_train[i], len(X_train[i])
#     # break
#

start = time()

model = ChainCRF(inference_method='max-product', directed=True)
ssvm = FrankWolfeSSVM(model=model, C=1.0, max_iter=10)

ssvm.fit(X_train, y_train)

print 'accuracy of linear-crf %f:' % ssvm.score(X_test, y_test), ' time spend: %f' %(time()-start)