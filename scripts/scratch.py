import numpy as np




indices = [1,3,5,2,1,5,3]
Is =       [1,1,1,1,1,1,1]


y1 = np.zeros(10)
for index, I in zip(indices, Is):
    y1[index] +=I


y1 = np.zeros(10)



print(y1)
