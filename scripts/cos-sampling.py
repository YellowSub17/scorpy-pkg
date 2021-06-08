
import scorpy
from scorpy import __DATADIR
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')





# from scorpy.utils import angle_between_rect, index_x


# x = angle_between_rect( [0,0,1], [0,1,-1])
# print(x)

# ind = index_x(x, -1, 1, 10,True)
# print(ind)




cif = scorpy.CifData(f'{__DATADIR}/xtal/fcc-sf.cif')
corr = scorpy.CorrelationVol(path=f'{__DATADIR}/dbins/fcc_qcor')


corr.plot_sumax()
plt.show()
















