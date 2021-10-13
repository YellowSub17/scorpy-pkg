
import matplotlib.pyplot as plt
import scorpy





pk = scorpy.PeakData(f'{scorpy.DATADIR}/h5/out.h5')




plt.figure()
pk.geo.plot_panels()
pk.plot_peaks(cmap='hot')
plt.colorbar()

plt.show()




