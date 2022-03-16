
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

cif1 = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{tag}.cif')
cif1.fill_from_vhkl( f'{scorpy.DATADIR}/xtal/{tag}.vhkl')

cif1.save(f'{scorpy.DATADIR}/xtal/{tag}-sf.cif')


corr = scorpy.CorrelationVol(qmax = cif1.qmax)

corr.fill_from_cif(cif1, verbose=2)



# cif2 = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/cuso45h2o.cif')


# cif3 = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/1al1-sf.cif')


















# cif = scorpy.CifData(
    # a_mag= 30.47 , b_mag= 59.39 , c_mag= 68.78 ,
    # alpha= 90 ,  beta= 90 , gamma= 90 , spg='x')


# sphv = scorpy.SphericalVol(100, 180, 360, 1.5)
# sphv.vol = np.random.random(sphv.vol.shape)
# cif.fill_from_sphv(sphv)


# cif.save(f'{scorpy.DATADIR}/xtal/ortho-intenr-qmax15-sf.cif')
# cif.save_hkl(f'{scorpy.DATADIR}/xtal/ortho-intenr-qmax15-sf.hkl')
# cif.save_pdb(f'{scorpy.DATADIR}/xtal/ortho-intenr-qmax15-sf.pdb')












