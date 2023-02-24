

import scorpy
import numpy as np



# vesta_sf_path = f'{scorpy.DATADIR}/ice/sim/struct/hex-ice-vesta-sf.txt'


# vesta_sfs = np.genfromtxt(vesta_sf_path, skip_header=1)


# hs, ks, ls, Is = vesta_sfs[:,0], vesta_sfs[:,1],vesta_sfs[:,2],vesta_sfs[:,6]


# Is = Is**2

# # Is /= np.max(Is) 
# # Is -= 1e-16


# crystfel_hkl_file = open(f'{scorpy.DATADIR}/ice/sim/struct/hex-ice.hkl', 'w')


# crystfel_hkl_file.write('CrystFEL reflection list version 2.0\n')
# crystfel_hkl_file.write('Symmetry: 6/mmm\n')
# crystfel_hkl_file.write('\th\tk\tl\tI\tphase\tsigma(I)\tnmeas\n')


# for h, k, l, I in zip(hs, ks, ls, Is):
    # if I > 1e-6:
        # if l>=0:
            # line = f'\t{int(h)}\t{int(k)}\t{int(l)}\t{round(I,14)}\t-\t0.0\t1\n'
            # # line = f'\t{int(h)}\t{int(k)}\t{int(l)}\t{100000}\t-\t0.0\t1\n'
            # crystfel_hkl_file.write(line)


# crystfel_hkl_file.write('End of reflections')
# crystfel_hkl_file.close()









cif = scorpy.CifData(f'{scorpy.DATADIR}/ice/sim/struct/hex-ice-sf.cif')

cif.save_crystfel_hkl(f'{scorpy.DATADIR}/ice/sim/struct/hex-ice-p1.hkl')


