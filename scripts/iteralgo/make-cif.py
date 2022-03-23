
import scorpy
import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt
plt.close('all')
import CifFile as pycif






# cif = scorpy.CifData(
    # a_mag= 6.12 , b_mag= 10.7 , c_mag= 5.97 ,
    # alpha= 82.27 ,  beta= 107.43 , gamma= 102.67 , spg='P -1')






tag = 'hexamine-bis-benzoic-acid'
tag = 'ausb2'
tag = 'cuso45h2o'
tag = 'nicotineamide'
tag = 'anilinomethylphenol'
tag = 'agno3'

cif = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{tag}.cif')
cif.fill_from_vhkl( f'{scorpy.DATADIR}/xtal/{tag}.vhkl')

cif.save(f'{scorpy.DATADIR}/xtal/{tag}-sf.cif')



print(f'Made {tag}-sf.cif')
print(f'qmax: {cif.qmax}')







# nq = 100
# ntheta = 180
# nphi = 360

# rotk=None
# rottheta=0


# cif1 = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{tag}-sf.cif', rotk = rotk, rottheta=rottheta)
# sphv1 = scorpy.SphericalVol(nq, ntheta, nphi, cif1.qmax)
# sphv1.fill_from_cif(cif1)


# rotk = np.array( [0, 0, 1])
# rottheta = np.radians(5)


# cif2 = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{tag}-sf.cif', rotk = rotk, rottheta=rottheta)
# sphv2 = scorpy.SphericalVol(nq, ntheta, nphi, cif2.qmax)
# sphv2.fill_from_cif(cif2)



# qloc = np.unique(sphv2.ls_pts(inds=True)[:,0])
# print(qloc)

# qq = 98




# fig, axes = plt.subplots(1,2)
# sphv1.plot_slice(0, qq, fig=fig, axes=axes[0], log=True)
# sphv2.plot_slice(0, qq, fig=fig, axes=axes[1], log=True)




# cif3 = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{tag}.cif', rotk=rotk, rottheta=rottheta )

# cif3.fill_from_sphv(sphv2)










plt.show()



