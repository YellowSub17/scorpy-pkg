
import scorpy
import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt
plt.close('all')
import CifFile as pycif





sample = 'nacl'


cif = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{sample}/{sample}.cif')
cif.fill_from_vhkl( f'{scorpy.DATADIR}/xtal/{sample}/{sample}.vhkl', fill_peaks=False)
cif.save(f'{scorpy.DATADIR}/xtal/{sample}/{sample}-sf.cif')
cif.save_hkl(f'{scorpy.DATADIR}/xtal/{sample}/{sample}.hkl')

print(f'Made {sample}-sf.cif')
print(f'qmax: {cif.qmax}')






# cif1 = scorpy.CifData(f'{scorpy.DATADIR}/xtal/{sample}/{sample}-sf.cif')


# sphv = scorpy.SphericalVol(256, 180*2, 180*4, cif1.qmax)
# sphv.vol +=1


# cif2 = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{sample}/{sample}.cif')
# cif2.fill_from_sphv(sphv)





# cif1.scat_bragg[:,-1] = 0
# cif2.scat_bragg[:,-1] = 0

# cif1.save('/home/pat/Desktop/targ.cif')
# cif2.save('/home/pat/Desktop/supp.cif')












