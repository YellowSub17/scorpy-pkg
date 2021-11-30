import scorpy
import numpy as np
np.random.seed(0)

import CifFile as pycif


sym = 'ccc'






base_cif = pycif.ReadCif(f'{scorpy.DATADIR}/cifs/{sym}-sf.cif')
vk = base_cif.visible_keys[0]
nref = len(base_cif[vk]['_refln.intensity_meas'])

inten = np.array(base_cif[vk]['_refln.intensity_meas']).astype(np.float32)
new_inten = list(inten*np.random.random(nref))

base_cif[vk]['_refln.intensity_meas'] = new_inten

cont = base_cif.WriteOut()



file = open(f'{scorpy.DATADIR}/cifs/{sym}-rand-sf.cif', 'w')
file.write(cont)
file.close()







