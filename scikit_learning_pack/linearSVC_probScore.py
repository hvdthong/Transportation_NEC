__author__ = 'vdthoang'
from sklearn import datasets
from sklearn import preprocessing
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split
import numpy as np


iris = datasets.load_iris()
X_iris, y_iris = iris.data, iris.target

print X_iris.shape, y_iris.shape

X, y = X_iris[:, :2], y_iris  # get the first two elements in X

# X_new, y_new = list(), list()
# for index in range(0, len(y_iris)):
#     if y_iris[index] != 2:
#         X_new.append(X[index]), y_new.append(y[index])
#
# X, y = np.array(X_new), np.array(y_new)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)
print X_train.shape, y_train.shape  # X_train is training data & y_train is the label of training data

scaler = preprocessing.StandardScaler().fit(X_train)  # Standardize the features
X_train_scaler = scaler.transform(X_train)
X_test_scaler = scaler.transform(X_test)

# for i in range(0, len(X_train)):
#     print X_train[i], X_train_scaler[i], y_train[i]

X_train = X_train_scaler
X_test = X_test_scaler

clf = LinearSVC()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

y_pred_score = clf.decision_function(X_test)
print len(y_pred)
print clf.coef_
print clf.intercept_
for value in y_pred:
    print value

for value in y_pred_score:
    print value