__author__ = 'vdthoang'


from sklearn.cross_validation import StratifiedKFold, KFold
import numpy as np

labels = [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0]
skf = StratifiedKFold(labels, 4)
# skf = KFold(len(labels), 4, shuffle=True, random_state=0)
labels = np.array(labels)
for train, test in skf:
    print("%s %s" % (train, test))

    print labels[train], labels[test]
    print 'Finishing -----------------'
