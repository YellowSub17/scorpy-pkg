


import scorpy
import healpy as hp
import matplotlib.pyplot as plt

# from scorpy.spharm import SphericalIntenVol


cif = scorpy.CifData('../data/xtal/1al1-sf.cif')

inten = scorpy.SphericalInten()


inten.fill_from_cif(cif)












