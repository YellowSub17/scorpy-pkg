import numpy as np
import matplotlib.pyplot as plt



x = np.array([  [1,0],
                [0,5] ])


x_flat = x.flatten()



inds_flat = inds.flatten()

cor_t = np.zeros(x_flat.shape)



np.add.at(cor_t, inds_flat, x_flat)



plt.figure()
plt.imshow(x)
plt.title('x')
plt.figure()
plt.plot(x_flat)
plt.title('x_flat')

plt.figure()
plt.imshow(inds)
plt.title('inds')
plt.figure()
plt.plot(inds_flat)
plt.title('inds_flat')

plt.figure()
plt.title('cor')
plt.plot(cor_t)


plt.show()

