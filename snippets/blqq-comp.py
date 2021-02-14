

from scorpy import BlqqVol, SphericalHandler, CorrelationVol, CifData










cif = CifData('../data/xtal/1al1-sf.cif')

qti = cif.scattering[::100,:]

correl = CorrelationVol(100,180,cif.qmax)
correl.correlate(qti)


# sph = SphericalHandler(100,32, cif.qmax)

blqq1 = BlqqVol(100,32,cif.qmax)
blqq1.fill_from_corr(correl)






# blqq2 = BlqqVol(100,32,cif.qmax)
# blqq2.fill_from_sph(sph)








