
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

cif1 = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{tag}.cif')
cif1.fill_from_vhkl( f'{scorpy.DATADIR}/xtal/{tag}.vhkl')

cif1.save(f'{scorpy.DATADIR}/xtal/{tag}-sf.cif')



print(f'Made {tag}-sf.cif')
print(f'qmax: {cif1.qmax}')








