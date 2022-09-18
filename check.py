import numpy as np
from collections import deque

a = np.zeros((10, 10))

a[5:] = 1
a = a.T
print(a[0][9])
