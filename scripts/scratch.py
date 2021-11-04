

import numpy as np

import scorpy
import matplotlib.pyplot as plt
plt.close('all')





group = 'dummy'
run = 'x_x'

# group = 'hkustcont'
# run = '86301_94'



xfm = scorpy.XfmH5s(group, run)
corr = scorpy.CorrelationVol(xfm.radius, 360, 1, cos_sample=False)


h5_1 = xfm.ls_h5s()[0]

d = xfm.extract_array(h5_1)


d_unwrapped = xfm.full_unwrap(d)


plt.figure()
plt.imshow(d_unwrapped[0])



for i in d_unwrapped:


    print(i)
    corrdu = corr.correlate_fft_pol(i)

    corr.vol += np.copy(corrdu)


corr.plot_q1q2()







plt.show()



