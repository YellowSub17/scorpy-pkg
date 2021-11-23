

import scorpy
import numpy as np
import timeit

x = scorpy.SphericalVol(200, 180, 360, 1)
x.vol = np.random.random(x.vol.shape)
x.save('x.dbin')
x.save('x.npy')

n = 1000
t1 = timeit.timeit('y = scorpy.SphericalVol(path="x.dbin")', globals=globals(),number=n )
t2 = timeit.timeit('y = scorpy.SphericalVol(path="x.npy")', globals=globals(),number=n )

print(t1/n)
print(t2/n)











