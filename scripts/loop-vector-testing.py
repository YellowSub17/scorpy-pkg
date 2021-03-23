import numpy as np
import scorpy
import timeit






name = '1al1'
cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif')
cor = scorpy.CorrelationVol(path=f'../data/dbins/{name}_large_qcor')


sph_base = scorpy.SphHarmHandler(cor.nq, 37, cor.qmax)
iv_base = scorpy.SphInten(cor.nq, 2**5, cor.qmax)


sph_cif = sph_base.copy().fill_from_cif2(cif)
iv_sph = iv_base.copy().fill_from_sph(sph_cif)

# y1, y2 = sph_base.copy().fill_from_ivol2(iv_sph)
# x = sph_base.copy().fill_from_ivol(iv_sph)
# y = sph_base.copy().fill_from_ivol2(iv_sph)

# tx1 = timeit.timeit("x = sph_base.copy().fill_from_ivol(iv_sph)", globals=globals(), number=1)
# ty1 = timeit.timeit("y = sph_base.copy().fill_from_ivol2(iv_sph)", globals=globals(), number=1)





tx2 = timeit.timeit("x = sph_base.copy().fill_from_cif(cif)", globals=globals(), number=1)
ty2 = timeit.timeit("y = sph_base.copy().fill_from_cif2(cif)", globals=globals(), number=1)









