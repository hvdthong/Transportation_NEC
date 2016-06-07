__author__ = 'vdthoang'

from scipy.sparse import *
A = csr_matrix([[1, 2], [3, 4]])
B = csr_matrix([[5], [6]])

print type(A), type(B)
print hstack([A,B]).toarray()
