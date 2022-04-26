import scorpy
import numpy as np


v = scorpy.CorrelationVol(50, 90, 2,)

v.save(f'{scorpy.DATADIR}/test.dbin')
