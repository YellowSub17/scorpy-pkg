import scorpy
import numpy as np
import pyshtools as pysh



def test_input():
    n_angles = [300]
    extends  = [True, False]
    grid_types = ['DH1', 'DH2', 'GLQ']

    for n_angle in n_angles:
        for grid_type in grid_types:
            for extend in extends:

                sphvol = scorpy.SphericalVol(1, n_angle, grid_type=grid_type, extend=extend)

                lmax=sphvol.lmax


                coeffs = np.zeros( (2,lmax+1,lmax+1))

                coeffs[0,140,140] = 5

                coeffs_l6m3 = pysh.SHCoeffs.from_array(coeffs)
                expanded = coeffs_l6m3.expand(grid=grid_type,extend=extend)

                sphvol.vol[0,...] = expanded.data

