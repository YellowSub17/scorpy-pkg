#!/usr/bin/env python3
'''
corr-comp.py

Compare various correlation vols
'''



import scorpy
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np




run = 108
padf = scorpy.PadfVol(path=f"../data/dbins/cosine_sim/{run}/run{run}_padf")
padf.plot_sumax()
plt.title(f'{run} sum')
padf.plot_xy()
plt.title(f'{run} r1r2')


run = 109
padf = scorpy.PadfVol(path=f"../data/dbins/cosine_sim/{run}/run{run}_padf")
padf.plot_sumax()
plt.title(f'{run} sum')
padf.plot_xy()
plt.title(f'{run} r1r2')

plt.show()
