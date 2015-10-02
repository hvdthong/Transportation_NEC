__author__ = 'vdthoang'
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.cross_validation import cross_val_score, KFold
from sklearn.pipeline import Pipeline
from scipy.stats import sem
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

iris = datasets.load_iris()
X_iris, y_iris = iris.data, iris.target

print X_iris.shape, y_iris.shape

# for i in range(0, len(X_iris)):
#     print X_iris[i], y_iris[i]
#
# print '------------------------------'
# print '------------------------------'
# print X_iris[0], y_iris[0] # print first element

X, y = X_iris[:, :2], y_iris # get the first two elements in X
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)
print X_train.shape, y_train.shape # X_train is training data & y_train is the label of training data

scaler = preprocessing.StandardScaler().fit(X_train)  # Standardize the features
X_train_scaler = scaler.transform(X_train)
X_test_scaler = scaler.transform(X_test)

# for i in range(0, len(X_train)):
#     print X_train[i], X_train_scaler[i], y_train[i]

X_train = X_train_scaler
X_test = X_test_scaler
# print len(X_test)

# colors = ['red', 'greenyellow', 'blue']
# for i in xrange(len(colors)):
#     xs = X_train[:, 0][y_train == i]
#     ys = X_train[:, 1][y_train == i]
#     plt.scatter(xs, ys, c=colors[i])
# plt.legend(iris.target_names)
# plt.xlabel('Sepal length')
# plt.ylabel('Sepal width')
# plt.show()

clf = SGDClassifier()
clf.fit(X_train, y_train)
print clf.coef_
print clf.intercept_

# print clf.predict(scaler.transform([[4.7, 3.1]]))
# print clf.decision_function(scaler.transform([[4.7, 3.1]]))

# print clf.predict(scaler.transform([[5.7, 2.8]]))
# print clf.decision_function(scaler.transform([[5.7, 2.8]]))

# print X.shape

y_pred = clf.predict(X_test)
print 'Accuracy of clf: %f' % metrics.accuracy_score(y_test, y_pred)
# print metrics.classification_report(y_test, y_pred, target_names=iris.target_names)
# print metrics.confusion_matrix(y_test, y_pred)

# create a composite estimator made by a pipeline of the standarization and the linear model
clf = Pipeline([('scaler', preprocessing.StandardScaler()),('linear_model', SGDClassifier())])
cv = KFold(X.shape[0], 5, shuffle=True, random_state=33)
scores = cross_val_score(clf, X, y, cv=cv)
print scores
print ("Mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(scores), sem(scores))

clf = Pipeline([('scaler', preprocessing.StandardScaler()),('decision_tree', DecisionTreeClassifier())])
cv = KFold(X.shape[0], 5, shuffle=True, random_state=33)
scores = cross_val_score(clf, X, y, cv=cv)
print scores
print ("Mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(scores), sem(scores))

clf = Pipeline([('scaler', preprocessing.StandardScaler()),('logistic', LogisticRegression())])
cv = KFold(X.shape[0], 5, shuffle=True, random_state=33)
scores = cross_val_score(clf, X, y, cv=cv)
print scores
print ("Mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(scores), sem(scores))



