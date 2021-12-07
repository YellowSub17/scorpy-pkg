#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





tag = 'fcc_inten_r1_supp_t'
qq = 128




st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')

plt.figure()
for sub_tag in ['a', 'b', 'c']:
    y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    plt.plot(y[1:])

# plt.figure()
# plt.plot(st.vol[st.vol>0])
# for sub_tag in ['a', 'b', 'c']:
    # sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
    # plt.plot(sf.vol[sf.vol>0])

st.plot_slice(0, qq, title='targ')
for sub_tag in ['a', 'b', 'c']:
    sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
    sf.plot_slice(0, qq, title=f'{sub_tag}')



# plt.figure()
# plt.plot(y[101:200])

# plt.figure()
# plt.plot(y[301:400])

# plt.figure()
# plt.plot(y[501:600])






# fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
# sf.plot_slice(0, qq, title='final', fig=fig, axes=axes[0])
# st.plot_slice(0, qq, title='targ', fig=fig, axes=axes[1])

# plt.figure()





plt.show()
