import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')


a = scorpy.CorrelationVol(10, 10, 1)


a.vol[0,0,0] = 1

b = a.copy()


b.vol[1,1,1] = 1





# # Parameters
# nq= 100
# ntheta = 180
# nphi = 360
# nl = 90
# qmax = 108

# qq = 49

# # SET UP DATA
# cif = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax = qmax)
# # cif.scat_sph[:,-1] *= 2
# # cif.scat_sph[:,-1] *= np.random.random(len(cif.scat_sph[:,-1]))
# # cif.scat_sph[:,-1] = np.abs(cif.scat_sph[:,-1])**2


# # SET UP TARGET HARMONICS
# sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
# sphv_targ.fill_from_cif(cif)
# sphv_targ.plot_slice(0,qq, title='Target')

# # SET UP MASK
# sphv_mask = sphv_targ.copy()
# sphv_mask.make_mask()
# sphv_mask.plot_slice(0,qq, title='Mask')



# iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
# iqlm_targ.fill_from_sphv(sphv_targ)

# # SET UP BLQQ
# blqq_data = scorpy.BlqqVol(nq, nl, qmax)
# blqq_data.fill_from_iqlm(iqlm_targ)






# # SET UP ALGORITHM
# # a_sphv = scorpy.AlgoHandler(blqq_data, sphv_mask, iter_obj='sphv')
# # a_iqlm = scorpy.AlgoHandler(blqq_data, sphv_mask, iter_obj='iqlm')


# iter_obj = 'iqlm'


# a_tt = scorpy.AlgoHandler(blqq_data, sphv_mask, iter_obj=iter_obj,
                            # lossy_sphv=True, lossy_iqlm=True)

# a_ff = scorpy.AlgoHandler(blqq_data, sphv_mask, iter_obj=iter_obj,
                            # lossy_sphv=False, lossy_iqlm=False)

# a_tf = scorpy.AlgoHandler(blqq_data, sphv_mask, iter_obj=iter_obj,
                            # lossy_sphv=True, lossy_iqlm=False)

# a_ft = scorpy.AlgoHandler(blqq_data, sphv_mask, iter_obj=iter_obj,
                            # lossy_sphv=False, lossy_iqlm=True)

# for i in range(5):
    # print(i)

    # a_tt.ER()
    # a_ff.ER()
    # a_tf.ER()
    # a_ft.ER()



# plt.show()


















