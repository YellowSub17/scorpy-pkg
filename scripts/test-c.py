import ctypes
import scorpy


cif = scorpy.CifData('../data/xtal/1al1-sf.cif')
sph = scorpy.SphHarmHandler(100,11, cif.qmax)
sph.fill_from_cif(cif)

x = sph.fill_from_cif2(cif)
print(x)








