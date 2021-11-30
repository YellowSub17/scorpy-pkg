#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')









tag = 'apple'
# tag = 'targ_fcc_supp_ccc'
sub_tag = 'a'


y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)

plt.figure()
plt.plot(y[1:])

plt.figure()
plt.plot(range(201, len(y)), y[201:])















plt.show()
