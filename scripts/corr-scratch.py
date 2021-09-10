import scorpy
import numpy as np
import matplotlib.pyplot as plt




cif = scorpy.CifData(f'{scorpy.env.__DATADIR}/cifs/fcc-sf.cif', qmax=40)

c1 = scorpy.CorrelationVol(100, 180, cif.qmax, cos_sample=True)
c2 = scorpy.CorrelationVol(100, 180, cif.qmax, cos_sample=False)




