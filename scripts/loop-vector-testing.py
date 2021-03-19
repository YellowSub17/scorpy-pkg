import numpy as np
import scorpy
import timeit






name = '1al1'
cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif')
cor = scorpy.CorrelationVol(path=f'../data/dbins/{name}_large_qcor')
sph_base = scorpy.SphHarmHandler(cor.nq, 27, cor.qmax)


tx = timeit.timeit("x = sph_base.copy().fill_from_cif(cif)", globals=globals(), number=1)
ty = timeit.timeit("y = sph_base.copy().fill_from_cif2(cif)", globals=globals(), number=1)









