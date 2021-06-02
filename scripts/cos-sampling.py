
import scorpy
import numpy as np
import matplotlib.pyplot as plt




c = scorpy.CorrelationVol(100,180,1)


plt.figure()
plt.plot(c.zpts, c.zpts, label='sample pts')
plt.plot(c.zpts, np.degrees(np.arccos(np.cos(np.radians(c.psipts)))), label='acos( cos( pts ) )')
plt.legend()
plt.title('Sample Points')

plt.figure()
plt.plot(c.zpts, c.zpts - np.degrees(np.arccos(np.cos(np.radians(c.psipts)))))
plt.title('Difference')



plt.show()












