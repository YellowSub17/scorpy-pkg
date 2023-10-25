import matplotlib.pyplot as plt
plt.close('all')

import scorpy
import numpy as np



cif1 = scorpy.CifData('/media/pat/datadrive/xtal/agno3/agno3-sf.cif')


print(cif1.qmax)


print('a', np.linalg.norm(cif1.ast))
print('b', np.linalg.norm(cif1.bst))
print('c', np.linalg.norm(cif1.cst))
