import scorpy
import numpy as np
import matplotlib.pyplot as plt



cif = scorpy.CifData('/home/ec2-user/corr/data/xtal/193l-sf.cif')
q_inte_r = min(cif.ast_mag, cif.bst_mag, cif.cst_mag)



pdb_code ='193l'
xtal_size = '80nm'

super_chunk = ''
chunk=0
frame = 3

ns  = 1

# for bw in ['10', '01', '001', '0']:
    # geom_code = f'19MPz040bw{bw}'
    # fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
    # plt.title(f'{xtal_size} orig')

    # npz_fname =  f'/home/ec2-user/corr/data/frames/bw-tests/{pdb_code}-{xtal_size}-{geom_code}-ns{ns}-{frame}.npz'
    # pk = scorpy.PeakData(npz_fname, f'/home/ec2-user/corr/data/geom/{geom_code}.geom')

    # r_inte_r = pk.convert_q2r(q_inte_r)/2

    # pk.plot_peaks(fig=fig, ax=axes[0])
    # pk.plot_peakr(r_inte_r, fig=fig, ax=axes[0])

    # inte = pk.integrate_peaks(r_inte_r)
    # pk.calc_scat(inte[:,0:3], inte[:,-1])

    # pk.plot_peaks(fig=fig, ax=axes[1])
    # plt.title(f'bw {bw}')
    # pk.plot_qring(0.4)


# for frame in [0, 1, 2, 3, 4,]:
    # geom_code = f'19MPz040bw001'
    # fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
    # plt.title(f'{xtal_size} orig')

    # npz_fname =  f'/home/ec2-user/corr/data/frames/bw-tests/{pdb_code}-{xtal_size}-{geom_code}-ns{ns}-{frame}.npz'
    # pk = scorpy.PeakData(npz_fname, f'/home/ec2-user/corr/data/geom/{geom_code}.geom')

    # r_inte_r = pk.convert_q2r(q_inte_r)/2

    # pk.plot_peaks(fig=fig, ax=axes[0])
    # pk.plot_peakr(r_inte_r, fig=fig, ax=axes[0])

    # inte = pk.integrate_peaks(r_inte_r)
    # pk.calc_scat(inte[:,0:3], inte[:,-1])

    # pk.plot_peaks(fig=fig, ax=axes[1])
    # plt.title(f'frame {frame}')
    # pk.plot_qring(0.4)



frame = 0
for ns in [1, 3, 5, 8, 16, 32]:
    geom_code = f'19MPz040bw001'
    fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
    plt.title(f'{xtal_size} orig')

    npz_fname =  f'/home/ec2-user/corr/data/frames/bw-tests/{pdb_code}-{xtal_size}-{geom_code}-ns{ns}-{frame}.npz'
    pk = scorpy.PeakData(npz_fname, f'/home/ec2-user/corr/data/geom/{geom_code}.geom')

    r_inte_r = pk.convert_q2r(q_inte_r)/2

    pk.plot_peaks(fig=fig, ax=axes[0])
    pk.plot_peakr(r_inte_r, fig=fig, ax=axes[0])

    inte = pk.integrate_peaks(r_inte_r)
    pk.calc_scat(inte[:,0:3], inte[:,-1])

    pk.plot_peaks(fig=fig, ax=axes[1])
    plt.title(f'ns {ns}')
    pk.plot_qring(0.4)






plt.show()












