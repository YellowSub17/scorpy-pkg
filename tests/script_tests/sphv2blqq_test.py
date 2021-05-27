

import numpy as np
np.random.seed(0)
import scorpy
import matplotlib.pyplot as plt
plt.close('all')


def test_zeros():
    '''
    filling a blqq vol from a 0 intensity sphv should leave unchanged
    '''
    nq = 5
    ntheta = 18
    nphi = 36
    sphv = scorpy.SphericalVol(nq, ntheta, nphi)
    blqq = scorpy.BlqqVol(nq, sphv.nl)
    blqq.fill_from_sphv(sphv)

    np.testing.assert_array_equal(blqq.vol , np.zeros(blqq.vol.shape))





if __name__ == '__main__':

    nq = 100
    ntheta = 36
    nphi = 72
    lmax = 17

    n_sph = 1

    linterest = 4
    sphv = scorpy.SphericalVol(nq, ntheta, nphi)
    blqq = scorpy.BlqqVol(nq, sphv.nl)

    harms = []


    for q_ind in range(nq):
        coeffs = np.zeros( (2, sphv.nl, sphv.nl))
        for i in range(n_sph):
            cs = np.random.randint(0,2)
            l = np.random.randint(0,lmax+1)
            m = np.random.randint(0, l+1)
            if cs==1 and m==0:
                cs=0
            sph = cs, l, m

            while coeffs[sph] ==1 or (cs==1 and m==0):
                cs = np.random.randint(0,2)
                l = np.random.randint(0,lmax+1)
                m = np.random.randint(0, l+1)
                if cs==1 and m==0:
                    cs=0
                sph = cs, l, m
            coeffs[sph] = 1

            if l==linterest:
                print('####', q_ind, cs,l,m)
            # else:
                # print(q_ind, cs,l,m)



        sphv.set_q_coeffs(q_ind, coeffs)
        harms.append( (q_ind, cs, l, m) )

    sphv.plot_slice(0, 10)
    plt.title('sphv')

    blqq.fill_from_sphv(sphv)

    blqq.plot_slice(2,linterest, extent=None)
    plt.title(f'l={linterest}')

    blqq.plot_slice(2,10, extent=None)
    plt.title('')

    for q_ind, cs, l, m in harms:
        np.testing.assert_allclose(blqq.vol[q_ind, q_ind, l],1)


    for q_ind1, cs1, l1, m1 in harms:
        for q_ind2, cs2, l2, m2 in harms:

            if q_ind1 == q_ind2:
                continue

            if l1==l2 and m1==m2 and cs1==cs2:
                print(q_ind1, cs1, l1, m1)
                print(q_ind2, cs2, l2, m2)
                np.testing.assert_allclose(blqq.vol[q_ind1, q_ind2, l1],1)
                np.testing.assert_allclose(blqq.vol[q_ind2, q_ind1, l2],1)

    plt.show()











    # for i in range(nq):
        # coeffs = np.zeros( (2, sphv.nl, sphv.nl) )

        # cs = 0
        # l = 177
        # m = 25
        # coeffs[cs, l ,m] = 1

        # cs = 1
        # l = 17
        # m = 10
        # coeffs[cs, l ,m] = 1

        # cs = 1
        # l = 17
        # m = 10
        # coeffs[cs, l ,m] = 1

        # sphv.set_q_coeffs(i, coeffs)

    # blqq.fill_from_sphv(sphv)
    # blqq.plot_q1q2()
    # plt.show()

#     im = blqq.get_xy()[:, :-20]
    # plt.figure()
    # plt.imshow(im)
    # plt.show()


