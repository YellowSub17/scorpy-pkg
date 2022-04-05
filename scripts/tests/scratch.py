



import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')






a = scorpy.AlgoHandler('x', qmax=9.01, rotk=None, rottheta=np.radians(0))

print('making target')
a.make_target(f'{scorpy.DATADIR}/xtal/agno3/agno3-sf.cif')
print('making supper')
x = a.make_support(f'{scorpy.DATADIR}/xtal/agno3/agno3.cif')







# fig, axes = plt.subplots(1,2)

# cif = scorpy.CifData(f'{scorpy.DATADIR}/test-data/test-sf.cif', fill_peaks=True, rotk=[1,1,1], rottheta=np.radians(30))
# cif.scat_bragg[:,-1] =1
# cif.scat_rect[:,-1] =1
# cif.scat_sph[:,-1] =1
# corr = scorpy.CorrelationVol(qmax=cif.qmax)
# corr.fill_from_cif(cif)
# corr.plot_q1q2(fig=fig,axes=axes[0])




# cif = scorpy.CifData(f'{scorpy.DATADIR}/test-data/test-sf.cif', fill_peaks=True, rotk=[0,1,1], rottheta=np.radians(60))
# cif.scat_bragg[:,-1] =1
# cif.scat_rect[:,-1] =1
# cif.scat_sph[:,-1] =1
# corr = scorpy.CorrelationVol(qmax=cif.qmax)
# corr.fill_from_cif(cif)
# corr.plot_q1q2(fig=fig,axes=axes[1])

# plt.show()





