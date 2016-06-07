__author__ = 'vdthoang'
import matplotlib.pyplot as plt
a = plt.hist([1, 2, 1], bins=[0, 1, 2, 3])
print type(a[0])
list_ = a[0]

for value in list_:
    print value
print 'hello, this is histogram'



