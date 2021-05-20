

import numpy as np
np.random.seed(0)
import scorpy
import matplotlib.pyplot as plt


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

    # assert np.all(blqq.vol == np.zeros(blqq.vol.shape))
    np.testing.assert_array_equal(blqq.vol , np.zeros(blqq.vol.shape))



# def test_low_sh():

    # nq = 50
    # ntheta = 360
    # nphi = 720
    # sphv = scorpy.SphericalVol(nq, ntheta, nphi)

    # nl = sphv.nl

    # blqq = scorpy.BlqqVol(nq, nl)

    # lmax = 8

    # for i in range(nq):
        # coeffs = np.zeros( (2, sphv.nl, sphv.nl) )
        # cs = np.random.randint(0,2)
        # # l = np.random.randint(1, lmax+1)
        # l = i%lmax
        # m = np.random.randint(-l, l+1)
        # coeffs[cs, l ,m] = 1
        # sphv.set_q_coeffs(i,coeffs)

    # blqq.fill_from_sphv(sphv)

    # for i in range(lmax+2):
        # blqq.plot_slice(2,i, extent=None)
        # plt.title(i)

    # blqq.plot_sumax(2, extent=None)

    # plt.title('sum')









def rand_sph(lmax):

    cs = np.random.randint(0,2)
    l = np.random.randint(0,lmax+1)
    m = np.random.randint(0, ls1+1)

    return cs, l, m







if __name__ == '__main__':

    nq = 100
    ntheta = 360
    nphi = 720
    lmax = 90

    n_sph = 1

    sphv = scorpy.SphericalVol(nq, ntheta, nphi)
    blqq = scorpy.BlqqVol(nq, sphv.nl)


    cs1 = np.random.randint(0,2, nq)
    ls1 = np.random.randint(0,lmax+1, nq)
    ms1 = list(map(np.random.randint, np.zeros(nq), ls1+1))

    cs2 = np.random.randint(0,2, nq)
    ls2 = np.random.randint(0,lmax+1, nq)
    ms2 = list(map(np.random.randint, np.zeros(nq), ls2+1))


    harmonics1 = np.array([cs1,ls1, ms1])
    harmonics2 = np.array([cs2,ls2, ms2])

    for q_ind in range(nq):
        coeffs = np.zeros( (2, sphv.nl, sphv.nl))
        coeffs[tuple(harmonics1[:,q_ind])] = 1
        # coeffs[tuple(harmonics2[:,q_ind])] =1
        print(q_ind, np.where(coeffs==1))
        sphv.set_q_coeffs(q_ind, coeffs)


    blqq.fill_from_sphv(sphv)

    blqq.plot_slice(2,0)
    blqq.plot_slice(2,1)
    blqq.plot_slice(2,10)
    blqq.plot_slice(2,140)











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


