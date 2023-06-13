import scorpy
import numpy as np
import matplotlib.pyplot as plt



cif = scorpy.CifData('/home/ec2-user/corr/data/xtal/193l-sf.cif')
print('ast, bst, cst: ', cif.ast_mag, cif.bst_mag, cif.cst_mag)
q_inte_r = min(cif.ast_mag, cif.bst_mag, cif.cst_mag)
# q_inte_r = 0.07999981292563772




# for qmax, geomz in zip([1.5], ['040']):

geomz = '040'


for x in range(4):

    fig, axes = plt.subplots(1,2, sharex=True, sharey=True)


    npz_fname =  f'/home/ec2-user/corr/data/frames/193l-500nm-19MPz{geomz}-test-{x}.npz'
    pk = scorpy.PeakData(npz_fname, f'/home/ec2-user/corr/data/geom/19MPz{geomz}.geom')

    r_inte_r = pk.convert_q2r(q_inte_r)/2
    print(r_inte_r)

    pk.plot_peaks(fig=fig, ax=axes[0])
    plt.title(f'{x} orig')
    pk.plot_peakr(r_inte_r, fig=fig, ax=axes[0])

    inte = pk.integrate_peaks(r_inte_r)
    pk.calc_scat(inte[:,0:3], inte[:,-1])

    pk.plot_peaks(fig=fig, ax=axes[1])
    plt.title(f'{x} inte')
    pk.plot_qring(0.4)




plt.show()












