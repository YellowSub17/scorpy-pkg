

import numpy as np
import scorpy
import matplotlib.pyplot as plt



nr = 50
npsi = 180


rmax = 10
nl = 90






padf2 = scorpy.PadfVol(nr, npsi, rmax, nl)
padf2.fill_from_corr(f'{scorpy.env.__DATADIR}/dbins/fcc2_corr')


padf1 = scorpy.PadfVol(nr, npsi, rmax, nl)
padf1.fill_from_corr(f'{scorpy.env.__DATADIR}/dbins/fcc1_corr')

padf3 = scorpy.PadfVol(nr, npsi, rmax, nl)
padf3.fill_from_corr(f'{scorpy.env.__DATADIR}/dbins/fcc3_corr')




