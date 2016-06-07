__author__ = 'vdthoang'
import matplotlib.pyplot as plt
import numpy as np

# fake up some data
spread = np.random.rand(50) * 100
center = np.ones(25) * 50
flier_high = np.random.rand(10) * 100 + 100
flier_low = np.random.rand(10) * -100
data = np.concatenate((spread, center, flier_high, flier_low), 0)

# fake up some more data
spread = np.random.rand(50) * 100
center = np.ones(25) * 40
flier_high = np.random.rand(10) * 100 + 100
flier_low = np.random.rand(10) * -100
d2 = np.concatenate((spread, center, flier_high, flier_low), 0)
data.shape = (-1, 1)
d2.shape = (-1, 1)
# data = concatenate( (data, d2), 1 )
# Making a 2-D array only works if all the columns are the
# same length.  If they are not, then use a list instead.
# This is actually more efficient because boxplot converts
# a 2-D array into a list of vectors internally anyway.
data = [data, d2, d2[::2, 0]]
# multiple box plots on one figure

print len(data), type(data)

# plt.figure()
# plt.boxplot(data)
#
# plt.show()

from sklearn.metrics import confusion_matrix
y_true = [2, 0, 2, 2, 0, 1]
y_pred = [0, 0, 2, 2, 0, 2]
print confusion_matrix(y_true, y_pred)
print confusion_matrix(y_pred, y_true)

list_matrix = confusion_matrix(y_pred, y_true)
for row in list_matrix:
    line = ''
    for value in row:
        line = line + '\t' + str(value)
    print line.strip()


import collections
s = "012"
print(collections.Counter(s).most_common(1)[0])

sentence = 'Mary had a little lamb'
print sentence.count('2')