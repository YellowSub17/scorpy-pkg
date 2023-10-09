import scorpy
import numpy as np
import matplotlib.pyplot as plt



cif = scorpy.CifData('/home/ec2-user/corr/data/xtal/193l-sf.cif')
q_inte_r = min(cif.ast_mag, cif.bst_mag, cif.cst_mag)



pdb_code ='193l'
xtal_size = '100nm'
geom_code = f'19MPz040'

super_chunk = 'x0'
chunk=0
frame = 3

ns  = 1

for frame in [0, 1, 2, 3, 4,]:
    fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
    plt.title(f'{xtal_size} orig')

    npz_fname =  f'/home/ec2-user/corr/data/frames/{xtal_size}-{geom_code}-{super_chunk}/{chunk}/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-{chunk}-{frame}.npz'
    pk = scorpy.PeakData(npz_fname, f'/home/ec2-user/corr/data/geom/{geom_code}.geom')

    r_inte_r = pk.convert_q2r(q_inte_r)/2

    pk.plot_peaks(fig=fig, ax=axes[0])
    pk.plot_peakr(r_inte_r, fig=fig, ax=axes[0])

    inte = pk.integrate_peaks(r_inte_r)
    pk.calc_scat(inte[:,0:3], inte[:,-1])

    pk.plot_peaks(fig=fig, ax=axes[1])
    plt.title(f'frame {frame}')
    pk.plot_qring(0.4)




plt.show()












