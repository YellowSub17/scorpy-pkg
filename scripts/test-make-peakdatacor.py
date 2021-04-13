import scorpy

import numpy  as np

import matplotlib.pyplot as plt




geo = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')

peaks = scorpy.PeakData(f'../data/cxi/102/peaks.txt', geo)

cor = scorpy.CorrelationVol(100,180, 1.4)

for frame in peaks.split_frames():
    print('correlating frame')
    if frame.qlist.shape[0] < 150:
        cor.correlate(frame.qlist[:,-3:])


