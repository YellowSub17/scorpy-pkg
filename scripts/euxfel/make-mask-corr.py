
import scorpy
import numpy as np

import matplotlib.pyplot as plt
import h5py 





qmax=1.44

pk_mask = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/radial_mask_iwr.h5',qmax=qmax, mask_flag=True)


im = pk_mask.make_im()


plt.figure()
plt.imshow(im)
plt.show()

# mask_h5 = f'{scorpy.DATADIR}/cxi/radial_mask_iwr.h5'

# h5 = h5py.File(mask_h5, 'r')

# data = np.array(h5['data']['data'])

# h5.close()



# run_corr(f'{mask_data_folder}radial_mask_iwr', mask_data_folder, 'radial_mask_iwr_qcor_qmax',
              # nq, ntheta,  wavelength=geo.wavelength, res= geo.res,
              # clen=geo.clen, qmax=qmax)







