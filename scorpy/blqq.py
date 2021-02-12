import numpy as np
np.random.seed(1)
import time
from numba.extending import overload
from numba import jit, prange


import scipy.signal as signal
import configparser as cfp
from scipy import special
import itertools

import matplotlib.pyplot as plt
from xfelcorrel import CorrelationVol, CifData, index_x
import healpy as hp








if __name__ == '__main__':
    plt.close('all')

  #   # name = 'adamsite'
    # # qq = 87
    # # rot = (90,0,0)

    # name = '1al1'
    # qq = 87
    # rot = (90,0,0)



    # cif = CifData(f'data/xtal/{name}-sf.cif')
    # bl = BlqqVol(fromfile=True, fname=f'data/dbins/blqq/{name}_bl_pin')

    # iv_goal = SphericalIntenVol(bl.nq, 2**5, cifdata=cif)

    # iv_mask = SphericalIntenVol(bl.nq, 2**5, cifdata=cif)

    # iv_mask.ivol[np.where(iv_goal.ivol != 0)] = 1



    # hp.orthview(iv_goal.ivol[qq], title='Target Intensity', rot=rot)
    # plt.savefig('data/saved_plots/target_inten.png')
    # hp.orthview(iv_mask.ivol[qq], title='Support Constraint Mask', rot=rot)
    # plt.savefig('data/saved_plots/support.png')


    # ## Get the eigen values and eigenvectors of the bl matrix
    # bl_lam, bl_u = bl.get_eigh()



    # Ilm_sph = iv_goal.calc_sph(bl.nl)

    # iv_start = Ilm_sph.calc_ivol(2**5)
    # iv_start.ivol = np.random.random(iv_start.ivol.shape)
    # hp.orthview(iv_start.ivol[qq], title='Starting Intensity', rot=rot)
    # plt.savefig('data/saved_plots/init_inten.png')


    # loop_end = -1

    # for i in range(4):

        # loop_start = time.time()
        # print(f'\n\n')
        # print(f'Loop {i}')
        # print(f'Last loop took {loop_end} seconds.')
        # print(f'\n\n')


        # ###### CORRELATION CONSTRAINT
        # ##calculate the klmn values from the Ilm values and bl eigenvectors
        # k_sph = Ilm_sph.calc_klmn(bl_u)
        # ## scale kprime values from klmn and bl eigenvalues
        # kp_sph = k_sph.calc_kprime(bl_lam)
        # ## modify the Ilm values with the bl eigenvectors kprime values
        # Ilm_p_sph = kp_sph.calc_Ilm_p(bl_u)
        # ## recompose intensity from Ilm values
        # Ip = Ilm_p_sph.calc_ivol(iv_mask.nside)



        # #### plot result of correlation constraint
        # hp.orthview(Ip.ivol[qq], title=f'iteration {i}', rot=rot)
        # plt.savefig(f'data/saved_plots/iter_{i}.png')
        # # plt.close('all')




        # ###### SUPPORT CONSTRAINT
        # ## mask q position that are not on bragg peaks
        # Ip.ivol *= iv_mask.ivol
        # ## Only consider positive magnitudes
        # Ip.ivol = np.max((Ip.ivol, np.zeros(Ip.ivol.shape)), axis=0)



        # ###### NORMALISATION CONSTRAINT
        # Ia = Ip.calc_Ialpha(bl.blvol)
        # # Ia = Ip

        # hp.orthview(Ia.ivol[qq], title=f'iteration masked {i}', rot=rot)
        # plt.savefig(f'data/saved_plots/iter_masked_{i}.png')

        # ## Decompose masked intensity into Ilm
        # Ilm_sph = Ia.calc_sph(Ilm_sph.nl)


        # loop_end = time.time() - loop_start




    # Ip.ivol[qq]  = Ip.ivol[qq]
    # ## plot final result of the masked intensity
    # hp.orthview(Ip.ivol[qq], title='final_inten', rot=rot)
    # plt.savefig(f'data/saved_plots/final_inten.png')

    # plt.show()




























    # # # MAKE BLQQ FROM CORREL + CIF
    # names = ['1al1', '1vds', '5lf5', 'CuCN', 'diamond', 'adamsite']




    # nl = 61

    # for name in names:

        # correl = CorrelationVol(fromfile=True, fname=f'data/dbins/{name}_qcor')
        # cif = CifData(f'data/xtal/{name}-sf.cif', qmax=correl.qmax)
        # iv = SphericalIntenVol(nq=correl.nq,nside=2**6, cifdata=cif)

        # print(f'{name} sph1')
        # sph1 = SphericalHandler(correl.nq, nl, correl.qmax)
        # sph1.calc_spherical_scattering(cif.spherical)
        # print(f'{name} bl1')
        # bl1 = BlqqVol(correl.nq, nl, correl.qmax)
        # bl1.fill_from_sph(sph1)
        # bl1.save_dbin(f'data/dbins/blqq/{name}_bl_Ilm')


        # print(f'{name} bl4')
        # bl4 = BlqqVol(correl.nq, nl, correl.qmax, comp=False)
        # bl4.fill_from_cvol(correl.cvol)
        # bl4.save_dbin(f'data/dbins/blqq/{name}_bl_pin')


        # print(f'{name} sph2')
        # sph2 = SphericalHandler(correl.nq, nl, correl.qmax, comp=True)
        # sph2.fill_lnm_spherical_scattering(cif.spherical)
        # print(f'{name} bl2')
        # bl2 = BlqqVol(correl.nq, nl, correl.qmax, comp=True)
        # bl2.fill_from_sph(sph2)
        # bl2.save_dbin(f'data/dbins/blqq/{name}_bl_Ilm_comp')



        # print(f'{name} sph3')
        # sph3 = SphericalHandler(correl.nq, nl, correl.qmax, comp=True)
        # sph3.fill_lnm_ivol(iv.ivol)
        # print(f'{name} bl3')
        # bl3 = BlqqVol(correl.nq, nl, correl.qmax, comp=True)
        # bl3.fill_from_sph(sph3)
        # bl3.save_dbin(f'data/dbins/blqq/{name}_bl_hp')



        # print(f'{name} sph5')
        # sph5 = sph2.convert_comp2real()
        # print(f'{name} bl5')
        # bl5 = BlqqVol(correl.nq, nl, correl.qmax, comp=False)
        # bl5.fill_from_sph(sph5)
        # bl5.save_dbin(f'data/dbins/blqq/{name}_bl_Ilm_comp2real')



        # print(f'{name} sph6')
        # sph6 = sph3.convert_comp2real()
        # print(f'{name} bl6')
        # bl6 = BlqqVol(correl.nq, nl, correl.qmax, comp=False)
        # bl6.fill_from_sph(sph6)
        # bl6.save_dbin(f'data/dbins/blqq/{name}_bl_hp_comp2real')
