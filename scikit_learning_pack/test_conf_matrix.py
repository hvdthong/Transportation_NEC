__author__ = 'vdthoang'

from sklearn.metrics import confusion_matrix

y_true = [2, 0, 2, 2, 0, 1]
y_pred = [0, 0, 1, 1, 0, 1]
print confusion_matrix(y_true, y_pred)
print confusion_matrix(y_pred, y_true)
