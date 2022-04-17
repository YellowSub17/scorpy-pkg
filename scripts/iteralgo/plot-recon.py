#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')






# a = scorpy.AlgoHandler('triclinic')
# a.prep_shelxl('a')
# a.prep_shelxl('a', count=1)



# a = scorpy.AlgoHandler('tetracyclinehydrochloride')
# a.prep_shelxl('a')
# a.prep_shelxl('a', count=0)
# a.prep_shelxl('a', count=1)







# a = scorpy.AlgoHandler('tetracyclinehydrochloride')

# sphv_init = scorpy.SphericalVol(path=f'{a.path}/a/sphv_{a.tag}_a_init.dbin')
# sphv_suppt =  scorpy.SphericalVol(path=f'{a.path}/sphv_{a.tag}_supp_tight.dbin')


# sphv_init.plot_slice(0, -1)
# sphv_suppt.plot_slice(0, -1)
# sphv_init.integrate_peaks(mask_vol=sphv_suppt, dpix = a.dxsupp)
# sphv_init.plot_slice(0, -1)

# cif = scorpy.CifData(f'{a.path}/{a.tag}_targ-sf.cif', rotk=a.rotk, rottheta=a.rottheta)
# cif.fill_from_sphv(sphv_init)
# print(cif.scat_bragg)
# cif.save_hkl(f'{a.path}/a/hkls/{a.tag}_a_count_0.hkl')






a = scorpy.AlgoHandler('tetracyclinehydrochloride')
a.intensity_xy_plot('a')
a.bond_distance_xy_plot('a', col='b')
a.bond_distance_xy_plot('a', count=0, col='r', new_fig=False)

# sphv_final = scorpy.SphericalVol(path=f'{a.path}/a/sphv_{a.tag}_a_final.dbin')
# sphv_final.plot_slice(0, 148)






# counts = [1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,50,100,150,200,250,300,400,500,600,700]
# for count in counts:
    # print(count)
    # a.It_vs_Ia('a', count=count)
    # plt.savefig(f'/home/pat/Desktop/plots/{count}.png')
    # plt.close('all')




# a.shelxl('a', count=1)
# a.shelxl('a', count=500)
# a.shelxl('a', count=700)




# a.prep_shelxl('a')

# a.bond_distance_xy_plot('a')












plt.show()














