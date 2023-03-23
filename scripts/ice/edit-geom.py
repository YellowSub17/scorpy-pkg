import numpy as np
import scorpy
import os
import h5py


import matplotlib.pyplot as plt
plt.close('all')




pk = scorpy.PeakData(datapath=f'x',
                    geompath='/media/pat/datadrive/ice/sim/geoms/agipdv2_original.geom')



pk.write_geom('/media/pat/datadrive/ice/sim/geoms/agipd_v2.geom')





