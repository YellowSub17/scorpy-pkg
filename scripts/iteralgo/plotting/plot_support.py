

import scorpy
import matplotlib.pyplot as plt
import numpy as np





path=f'{scorpy.DATADIR}/algo/agno3-d03/sphv_agno3-d03_supp_loose.dbin'


supp = scorpy.SphericalVol(path=path)



supp.plot_slice(0, -10)

plt.show()
