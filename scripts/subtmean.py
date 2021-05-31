
import scorpy
import numpy as np
import matplotlib.pyplot as plt




x = scorpy.CorrelationVol(3,4,1)

x.vol = np.random.random(x.vol.shape)


x.sub_t_mean()











