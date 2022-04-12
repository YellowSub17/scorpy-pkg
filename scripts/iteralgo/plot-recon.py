#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')






a = scorpy.AlgoHandler('triclinic')



a.prep_shelxl('a')

# for i in range(1, 200, 25):
    # a.It_vs_Ia('a', count=i)
a.It_vs_Ia('a')










plt.show()














