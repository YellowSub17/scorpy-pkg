
import scorpy
import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt
plt.close('all')
import CifFile as pycif









# tag = 'hexamine-bis-benzoic-acid'
# tag = 'ausb2'
# tag = 'cuso45h2o'
# tag = 'nicotineamide'
# tag = 'anilinomethylphenol'
tag = 'agno3'
tag = 'nacl'
tag = 'aluminophosphate'
tag = 'barite'

atomic_cif = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{tag}/{tag}.cif')
atomic_cif.fill_from_vhkl( f'{scorpy.DATADIR}/xtal/{tag}/{tag}.vhkl')

atomic_cif.save(f'{scorpy.DATADIR}/xtal/{tag}/{tag}-sf.cif')

print(f'Made {tag}-sf.cif')
print(f'qmax: {atomic_cif.qmax}')







plt.show()



