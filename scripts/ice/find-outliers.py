

import scorpy
import numpy as np
import matplotlib.pyplot as plt



size = '1000nm'
geom ='19MPz18'




corr_means = np.load(f'/media/pat/datadrive/ice/sim/corr/19MPz18/means/hex-ice-{size}-qmin15-{geom}-qcor-means.npy')
corr_sq_means =np.load(f'/media/pat/datadrive/ice/sim/corr/19MPz18/means/hex-ice-{size}-qmin15-{geom}-qcor-sq-means.npy') 


plt.figure()
plt.imshow(corr_means)

plt.figure()
plt.imshow(corr_sq_means)




xs = np.sqrt(  corr_means**2 - corr_sq_means   )

plt.figure()
plt.imshow(xs)




plt.figure()
plt.hist(np.log10(xs.flatten()), bins=500)

plt.show()



