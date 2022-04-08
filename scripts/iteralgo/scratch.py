



import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')






# qmax = 9
# nq = 256
# npsi = 360*32
# nl = 180


# tag = 'x'


# cif1 = scorpy.CifData(f'{scorpy.DATADIR}/algo/x/x_targ-sf.cif')




# cif2 = scorpy.CifData(f'{scorpy.DATADIR}/algo/x/x_supp-sf.cif')



# cif1.scat_bragg[:,-1] = 0
# cif2.scat_bragg[:,-1] = 0

# cif1.save('/home/pat/Desktop/targ.cif')

# cif2.save('/home/pat/Desktop/supp.cif')




# a = scorpy.AlgoHandler(tag=tag, nq=nq, qmax=qmax, npsi=npsi, nl=nl)


# a.make_target(f'{scorpy.DATADIR}/xtal/agno3/agno3-sf.cif', verbose=99)
# a.make_support(f'{scorpy.DATADIR}/xtal/agno3/agno3.cif', verbose=99)
# a.make_data(verbose=99)


# recipe_path = f'{scorpy.DATADIR}/algo/RECIPES/x.txt'

# a.run_recon('y', recipe_path, verbose=99)







tag='nacl'


cif = scorpy.CifData(f'{scorpy.DATADIR}/algo/{tag}/{tag}_targ-sf.cif')
cif.save_hkl(f'{scorpy.DATADIR}/shelx/{tag}_targ.hkl')

sphv_targ = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
sphv_f = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/testing/sphv_{tag}_testing_final.dbin')
sphv_supp = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')

sphv_f.integrate_peaks(mask_vol=sphv_targ, dpix=2)
sphv_f.vol /= sphv_f.vol.sum()












cif.fill_from_sphv(sphv_f)
cif.save_hkl(f'{scorpy.DATADIR}/shelx/{tag}_algo.hkl')










