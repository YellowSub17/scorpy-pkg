#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')






a = scorpy.AlgoHandler('triclinic')





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

a.bond_distance_xy_plot('a')












plt.show()














