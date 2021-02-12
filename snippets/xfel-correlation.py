
import scorpy
import matplotlib.pyplot as plt


e = scorpy.ExpGeom('../data/agipd_2304_vj_opt_v3.geom')
p = scorpy.PeakData('../data/cxi/108/peaks.txt', e)

frames = p.split_frames()

frames = frames[::100]

e.plot_panels()
plt.title('panels')

c1 = scorpy.CorrelationVol(100, 180, 1.4)

for frame in frames:
    c1.correlate(frame.qlist[:,-3:])
    frame.plot_peaks()


c1.plot_q1q2()
plt.title('xfel correl')
c1.plot_sumax()
plt.show()







