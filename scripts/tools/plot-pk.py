#!/bin/bash/env python3
'''
plot-pkda.py

Plots the first frame of peaks in a PeakData file (.h5 or .txt)
Useage:
    plot-pkda.py [path]

    path:   Path to the pk data (txt or h5).
            Path is relative to scorpy.env.__DATADIR

'''






import scorpy
import matplotlib.pyplot as plt
import sys

if len(sys.argv) == 1:
    exit()

elif len(sys.argv) == 2:
    pk_path = f'{scorpy.env.__DATADIR}/{sys.argv[1]}'


pk = scorpy.PeakData(pk_path)
pk.split_frames()[0].plot_peaks(cmap='hot')
pk.geo.plot_panels()

plt.show()
