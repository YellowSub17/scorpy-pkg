

import scorpy





cif = scorpy.CifData(path='/home/ec2-user/corr/data/xtal/193l-sf.cif', qmax=1.5)
# cif = scorpy.CifData(
    # path
    # qmax
    # fill_peaks
    # rotk
    # rottheta
    # skip
    # atomi

cif.save_crystfel_hkl('/home/ec2-user/corr/data/xtal/193l.hkl')
