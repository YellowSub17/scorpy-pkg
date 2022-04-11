



import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')






qmax = 12.5
nq = 100
npsi = 360*32
nl = 180






# a = scorpy.AlgoHandler(tag='x', nq=nq, qmax=qmax, npsi=npsi, nl=nl)
# a.make_target(f'{scorpy.DATADIR}/xtal/nacl/nacl-sf.cif', verbose=99)
# a.make_support(f'{scorpy.DATADIR}/xtal/nacl/nacl.cif', verbose=99)
# a.make_data(verbose=99)



# sphv_supp = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/x/sphv_x_supp.dbin')
# sphv_targ = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/x/sphv_x_targ.dbin')

# plt.figure()
# plt.plot(sphv_supp.vol.sum(axis=-1).sum(axis=-1))

# plt.figure()
# plt.plot(sphv_targ.vol.sum(axis=-1).sum(axis=-1))

# sphv_supp.plot_slice(0, -1)





# a = scorpy.AlgoHandler(tag='x')
# a.run_recon('y', f'{scorpy.DATADIR}/algo/RECIPES/x.txt')



a = scorpy.AlgoHandler(tag='x')








# tag='nacl'


# cif = scorpy.CifData(f'{scorpy.DATADIR}/algo/{tag}/{tag}_targ-sf.cif')
# cif.save_hkl(f'{scorpy.DATADIR}/shelx/{tag}_targ.hkl')

# sphv_targ = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
# sphv_f = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/testing/sphv_{tag}_testing_final.dbin')
# sphv_supp = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')

# sphv_f.integrate_peaks(mask_vol=sphv_targ, dpix=2)
# sphv_f.vol /= sphv_f.vol.sum()












# cif.fill_from_sphv(sphv_f)
# cif.save_hkl(f'{scorpy.DATADIR}/shelx/{tag}_algo.hkl')









plt.show()

