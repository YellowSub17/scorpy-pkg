
import scorpy
import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt
plt.close('all')
import CifFile as pycif





sample = 'tetracyclinehydrochloride'




cif = scorpy.CifData(f'{scorpy.DATADIR}/xtal/{sample}/{sample}.cif')
cif.fill_from_vhkl(f'{scorpy.DATADIR}/xtal/{sample}/{sample}.vhkl', fill_peaks=False)
cif.save(f'{scorpy.DATADIR}/xtal/{sample}/{sample}-sf.cif')


print(cif.qmax)














