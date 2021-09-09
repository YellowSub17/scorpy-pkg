

import numpy as np





x0 = np.zeros( (10,10))
x0[0,0] = 1

x1 = np.zeros( (10,10))
x1[1,1] = 1
x1[2,2] = 1
x1[3,3] = 1





l0, u0 = np.linalg.eigh(x0)
l1, u1 = np.linalg.eigh(x1)




y1 = np.matmul( np.matmul( u1, np.diag(l1)), np.linalg.inv(u1))
y0 = np.matmul( np.matmul( u0, np.diag(l0)), np.linalg.inv(u0))





