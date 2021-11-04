

import numpy as np

import scorpy
import matplotlib.pyplot as plt
plt.close('all')
import time





group = 'dummy'
run = 'x_x'

# group = 'hkustcont'
# run = '86301_94'



xfm = scorpy.XfmH5s(group, run)
corr = scorpy.CorrelationVol(xfm.radius, 360, 1, cos_sample=False)


h5_1 = xfm.ls_h5s()[0]

d = xfm.extract_array(h5_1)

plt.figure()
plt.imshow(d[0])


d_unwrapped = xfm.full_unwrap(d)


plt.figure()
plt.imshow(d_unwrapped[0])



t = time.time()
for i in range(d_unwrapped.shape[0]):


    print(i)
    corrdu = corr.correlate_fft_pol(d_unwrapped[i])
    print()

    corr.vol += np.copy(corrdu)

tf = time.time() - t

print('time taken', tf)


corr.plot_q1q2(title='q1q2')
corr.plot_slice(0, 100, title='iq=100')
corr.plot_slice(2, 20, title='itheta=20')







plt.show()



