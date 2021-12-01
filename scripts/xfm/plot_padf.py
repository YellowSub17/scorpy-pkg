

import scorpy
import matplotlib.pyplot as plt




v = scorpy.Vol(path=f'{scorpy.DATADIR}/mofs/hkust/hkustcont/hkustcont_500frames_filtman0_padf2_padf.dbin')
v.plot_xy(title='cont')

# v = scorpy.Vol(path=f'{scorpy.DATADIR}/mofs/hkust/hkustcont/hkustcont_500frames_filtman0_mask_correlation.dbin')
# v.plot_xy(title='cont')

v = scorpy.Vol(path=f'{scorpy.DATADIR}/mofs/hkust/hkuststdchip/hkuststdchip_500frames_filtman0_padf2_padf.dbin')
v.plot_xy(title='chip')

v = scorpy.Vol(path=f'{scorpy.DATADIR}/mofs/hkust/hkustsoak/hkustsoak_500frames_filtman0_padf2_padf.dbin')
v.plot_xy(title='soak')

plt.show()

