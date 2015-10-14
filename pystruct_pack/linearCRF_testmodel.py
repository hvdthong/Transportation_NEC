__author__ = 'vdthoang'
import numpy as np
from pystruct.models import ChainCRF
from pystruct.learners import FrankWolfeSSVM

x = [[0,0,0,0], [0,1,0,0], [0,0,1,0], [0,1,1,0], [0,0,1,1]]
x_1 = [[0,0,0,0], [0,1,0,0], [0,0,1,0], [0,1,1,0], [0,0,0,0]]
print x
for value in x:
    print value
y = [0, 1, 1, 2, 2]
y_1 = [0, 1, 1, 2, 2]
print y

list_x, list_y = [], []
list_x.append(np.array(x))
list_x.append(np.array(x_1))
list_y.append(y)
list_y.append(y_1)

# crf = ChainCRF(inference_method='max-product')
crf = ChainCRF(inference_method='max-product', directed=False)
ssvm = FrankWolfeSSVM(model=crf, C=1.0, max_iter=100)
ssvm.fit(np.array(list_x), np.array(list_y))

test_x = np.array(list_x)
test_y = np.array(list_y)
print np.array(list_x)[0].shape[1]

x_test = [[1,0,0,0], [1,0,1,0]]
list_x_test = list()
list_x_test.append(x_test)

pred = ssvm.predict(np.array(list_x_test))
for value in pred:
    print value

list_ = list()
list_.append(0)
list_.append(1)
print list_