
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import sys









sim_n = 2048
wavelength = 6.7018e-11*1e10
npsi= 90
part = 'p0'



rmaxs = [86/2, 86/3, 86/4, 86/5, 86/6, 86/7, 86/8]
nrs = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
nls = [12, 16, 20, 24, 28, 32, 36, 40, 44, 48]



# rmax_i = sys.argv[1]
# nr_i = sys.argv[2]
# nl_i = sys.argv[3]



# code = f'code_{rmax_i}{nr_i}{nl_i}'
# print(f'##################{code}')
# nr = nrs[int(nr_i)]
# nl = nls[int(nl_i)]
# rmax = rmaxs[int(rmax_i)]



cs = [15]
for i in range(0, 10):
    fig, axes = plt.subplots(1,2)
    for ip, part in enumerate(['p0', 'p1']):
        print(f'{i} {part}')

        corr_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim_n}/sim{sim_n}-{part}-qcor.dbin'
        padf_path = f'{scorpy.DATADIR}/dbins/cxi/padfs/sim/{sim_n}/sim{sim_n}-{part}-code_{0}{0}{i}-padf.dbin'


        padf = scorpy.PadfVol(path=padf_path,)






        # padf.plot_r1r2(fig=fig, axes=axes[ip])
        padf.plot_r1r2(vminmax=(-2.5e64, 6.0e64), fig=fig, axes=axes[ip] )

        for c in cs:
            r = c/(2*np.sin(padf.zpts/2))
            axes[ip].plot(padf.zpts, r, 'r')

        axes[ip].set_ylim([0, padf.xmax])




plt.show()















