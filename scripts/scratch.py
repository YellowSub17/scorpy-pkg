

import numpy as np

import scorpy
import matplotlib.pyplot as plt
plt.close('all')
import time





group = 'dummy'
run = 'x_x'


xfm = scorpy.XfmH5s(group, run)
corr = scorpy.CorrelationVol(xfm.radius, 360, 1, cos_sample=False)


d = xfm.extract_array(xfm.ls_h5s()[0])
d_unwrapped = xfm.full_unwrap(d)

plt.figure()
plt.imshow(d[0])

plt.figure()
plt.imshow(d_unwrapped[0])


t = time.time()
for i, di in enumerate(d_unwrapped):
    print(i)
    corrdu = corr.correlate_fft_pol(di)
    print()

    corr.vol += corrdu

tf = time.time() - t
print('time taken', tf)

corr.plot_q1q2(title='q1q2')
corr.plot_slice(0, 100, title='iq=100')
corr.plot_slice(2, 20, title='itheta=20')





# xfm = scorpy.XfmH5s(group, run)
# corr2 = scorpy.CorrelationVol(xfm.radius, 360, 1, cos_sample=False)


# d = xfm.extract_array(xfm.ls_h5s()[0])
# d_unwrapped = xfm.full_unwrap(d)


####
#### Do not run, will crash computer if you don't have enough RAM
# # # t = time.time()
# # # corrdus = list(map(corr2.correlate_fft_pol, d_unwrapped))
# # # tf = time.time() - t
# # # print('time taken', tf)









plt.show()



