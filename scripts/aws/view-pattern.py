import scorpy
import numpy as np
import matplotlib.pyplot as plt



cif = scorpy.CifData('/home/ec2-user/corr/data/xtal/193l-sf.cif')
q_inte_r = min(cif.ast_mag, cif.bst_mag, cif.cst_mag)


geom_code = '19MPz040'

pdb_code ='193l'
xtal_size = '500nm'

super_chunk = 'x1'
chunk=212
frame = 220
for xtal_size in ['500nm']:

    fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
    plt.title(f'{xtal_size} orig')

    npz_fname =  f'/home/ec2-user/corr/data/frames/{xtal_size}-{geom_code}-{super_chunk}/{chunk}/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-{chunk}-{frame}.npz'
    pk = scorpy.PeakData(npz_fname, f'/home/ec2-user/corr/data/geom/19MPz040.geom')

    r_inte_r = pk.convert_q2r(q_inte_r)/2
    # print(r_inte_r)

    pk.plot_peaks(fig=fig, ax=axes[0])
    pk.plot_peakr(r_inte_r, fig=fig, ax=axes[0])

    inte = pk.integrate_peaks(r_inte_r)
    pk.calc_scat(inte[:,0:3], inte[:,-1])

    pk.plot_peaks(fig=fig, ax=axes[1])
    plt.title(f'{xtal_size}')
    pk.plot_qring(0.4)




plt.show()












