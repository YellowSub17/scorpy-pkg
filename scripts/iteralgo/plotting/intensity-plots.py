


import scorpy 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.close('all')


import numpy as np


tag = 'agno3-d07'

sub_tags = 'abcdefgh'



fig, axes = plt.subplots(1,1,figsize=(7.87, 2*3.93), dpi=150 )
a = scorpy.AlgoHandler(tag)



It, If, z = a.get_intensity('a', verbose=99, z='theta')

cmap = cm.jet(np.linspace(0, 1, len(z)))

a._plot_errorbar(It, If, fig=fig, axes=axes,color=z)

plt.show()

