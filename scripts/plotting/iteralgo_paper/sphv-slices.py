

import scorpy
import matplotlib.pyplot as plt
import numpy as np






supp = scorpy.SphericalVol(5, 10, 20, 1)

for i in range(3):

    fig, axes = plt.subplots(1,1,figsize=(2/2.54, 2/2.54), dpi=300, frameon=False )
    supp.vol = np.random.random(supp.vol.shape)
    supp.plot_slice(0, 1, xticks=[], yticks=[], cb=False, fig=fig, axes=axes)
    plt.tight_layout()
    # fig.savefig(f'/home/pat/Documents/cloudstor/phd/writing/iteralgopaper/figs/py/random_inten{i}.png')


cif = scorpy.CifData(path='/media/pat/datadrive/xtal/agno3-d05/agno3-d05-sf.cif', rotk=[1,1,1], rottheta=10)

supp = scorpy.SphericalVol(20, 20, 40,cif.qmax)


supp.fill_from_cif(cif)

for i in range(1,4):



    fig, axes = plt.subplots(1,1,figsize=(2/2.54, 2/2.54), dpi=300, frameon=False )
    supp.plot_slice(0, i, xticks=[], yticks=[], cb=False, fig=fig, axes=axes)
    plt.tight_layout()
    # fig.savefig(f'/home/pat/Documents/phd/writing/iteralgopaper/figs/py/target_q{i}.png')






plt.show()

