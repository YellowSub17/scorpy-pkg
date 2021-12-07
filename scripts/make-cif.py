import scorpy
import numpy as np
np.random.seed(1)

import CifFile as pycif


sym = 'fcc'



base_cif = pycif.ReadCif(f'{scorpy.DATADIR}/cifs/{sym}-sf.cif')
vk = base_cif.visible_keys[0]
nref = len(base_cif[vk]['_refln.intensity_meas'])

inten = np.array(base_cif[vk]['_refln.intensity_meas']).astype(np.float32)


rand_mask = np.ones(nref)
# rand_mask = np.random.random(nref)
# rand_mask[rand_mask > 0.25] = 1
# rand_mask[rand_mask <= 0.25] = 0


new_inten = list(inten*np.random.random(nref)*rand_mask)

base_cif[vk]['_refln.intensity_meas'] = new_inten

cont = base_cif.WriteOut()



file = open(f'{scorpy.DATADIR}/cifs/{sym}-rand1.cif', 'w')
file.write(cont)
file.close()







