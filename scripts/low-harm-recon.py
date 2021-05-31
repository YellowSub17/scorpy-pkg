import numpy as np
import scorpy
from scorpy.utils import angle_between_sph, index_x
import matplotlib.pyplot as plt
plt.close('all')
np.random.seed(0)


nq = 10
ntheta = 18
nphi = 36
lmax = 8
qmax = 1


sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)

for q_ind in range(nq):

    coeffs = np.zeros((2, sphv.nl, sphv.nl))

    cs_q = np.random.randint(0, 2)
    l_q = np.random.randint(0, 9)
    m_l = np.random.randint(0, l_q + 1)

    while cs_q == 1 and m_l == 0:
        cs_q = np.random.randint(0, 2)
        m_l = np.random.randint(0, l_q + 1)

    coeffs[cs_q, l_q, m_l] = 1
    print(q_ind, cs_q, l_q, m_l)

    sphv.set_q_coeffs(q_ind, coeffs)


corr_from_sphv = scorpy.CorrelationVol(path='../data/dbins/sphv_sh.dbin')


blqq1 = scorpy.BlqqVol(nq, sphv.nl, qmax)
blqq1.fill_from_sphv(sphv)
corr2 = scorpy.CorrelationVol(nq, nphi, qmax)
corr2.fill_from_blqq(blqq1)

blqq2 = scorpy.BlqqVol(nq, sphv.nl, qmax)
blqq2.fill_from_corr(corr_from_sphv)
corr3 = scorpy.CorrelationVol(nq, nphi, qmax)
corr3.fill_from_blqq(blqq2)


# corr2.plot_slice(2,0, extent=0)
# plt.title('sphv - blqq - corr')
# corr3.plot_slice(2,0, extent=0)
# plt.title('sphv - corr - blqq - corr')
# corr_from_sphv.plot_slice(2,0, extent=0)
# plt.title('sphv - corr')

corr2.plot_q1q2(extent=0)
plt.title('sphv - blqq - corr')
corr3.plot_q1q2(extent=0)
plt.title('sphv - corr - blqq - corr')
corr_from_sphv.plot_q1q2(extent=0)
plt.title('sphv - corr')

plt.show()


# SPHV CORRELATION
corr = scorpy.CorrelationVol(nq, nphi, qmax)

# q2_slice = sphv.vol[6,...]

pp, tt = np.meshgrid(sphv.phipts, sphv.thetapts)

for q1_ind in range(0, nq):
    q1_slice = sphv.vol[q1_ind, ...]
    print(q1_ind)

    for q2_ind in range(0, nq):
        q2_slice = sphv.vol[q2_ind, ...]

        for theta_ind in range(0, ntheta):

            for phi_ind in range(0, nphi):

                print(q1_ind, q2_ind, theta_ind, phi_ind)

                pp_rolled = np.roll(pp, (theta_ind, phi_ind), (0, 1))
                tt_rolled = np.roll(tt, (theta_ind, phi_ind), (0, 1))

                angle_between_flat = list(map(angle_between_sph, tt.flatten(), tt_rolled.flatten(), pp.flatten(), pp_rolled.flatten()))
                ite = np.ones(len(angle_between_flat))
                angle_between_ind = list(map(index_x, angle_between_flat, 0 * ite, np.pi * ite, nphi * ite))

                angle_between_rolled = np.array(angle_between_ind).reshape(ntheta, nphi)

                II = q1_slice * np.roll(q2_slice, (theta_ind, phi_ind), (0, 1)) * np.sin(tt_rolled) * np.sin(tt)

                for angle_ind, II_val in zip(angle_between_rolled.flatten(), II.flatten()):
                    corr.vol[q1_ind, q2_ind, angle_ind] += II_val


corr.save('../data/dbins/sphv_sh_sin.dbin')

# plt.figure()
# plt.imshow(II)

# plt.figure()
# plt.imshow(angle_between_rolled)
# plt.title('angle_bettween')

# plt.figure()
# plt.imshow(q1_slice)
# plt.title('q1 slice')

# plt.figure()
# plt.imshow(q2_slice)
# plt.title('q2 slice')


# plt.figure()
# plt.imshow(tt)
# plt.figure()
# plt.imshow(tt_rolled)

# plt.figure()
# plt.imshow(pp)
# plt.figure()
# plt.imshow(pp_rolled)


# plt.show()


# # plt.figure()
# # plt.imshow(q1_slice)
# # plt.title('q1_slice')
# # plt.figure()
# # plt.imshow(np.roll(q1_slice, roll_amnt, (0,1)))
# # plt.title('q1_slice rolled')

# # plt.figure()
# # plt.imshow(pp)
# # plt.title('pp')
# # plt.figure()
# # plt.imshow(np.roll(pp, roll_amnt, (0,1)))
# # plt.title('pp rolled')

# # plt.figure()
# # plt.imshow(tt)
# # plt.title('tt')
# # plt.figure()
# # plt.imshow(np.roll(tt, roll_amnt, (0,1)))
# # plt.title('tt rolled')

# # plt.figure()
# # plt.imshow(angle_between_rolled)


# # for iq1 in range(nq):
    # # for iq2 in range(nq):
        # # for it in range(ntheta):
            # # for ip in range(nphi):

                # # q1_slice_rolled = np.roll(q1_slice, (it, ip), (0,1))
                # # q2_slice_rolled = np.roll(q2_slice, (it, ip), (0,1))


# plt.show()


# # corr = scorpy.CorrelationVol(nq, nphi, qmax)

# # theta_pts

# # for q_ind1 in range(nq):
    # # q1_slice = sphv.vol[q_ind1,...]

    # # for q_ind2 in range(nq):
        # # q2_slice = sphv.vol[q_ind2,...]

        # # for t_ind1 in range(ntheta):
            # # for t_ind2 in range(ntheta):
                # # for p_ind1 in range(nphi):
                    # # for p_ind2 in range(nphi):
                        # # # print(q_ind1, q_ind2, t_ind1, t_ind2, p_ind1, p_ind2)


# # sphv2 = scorpy.SphericalVol(50, 180, 360, 1)
# # sphv2.fill_random(lmax=8)


# # blqq = scorpy.BlqqVol(sphv2.nq, sphv2.nl, sphv2.qmax)
# # blqq.fill_from_sphv(sphv2)


# # sphv2.plot_slice(0, 30, extent=None)
# # plt.title('iq=30')
# # blqq.plot_slice(2, 6, extent=None)
# # plt.title('l=6')
# # blqq.plot_slice(2, 3, extent=None)
# # plt.title('l=3')

# # blqq.plot_slice(2, 5, extent=None)
# # plt.title('l=5')


# # plt.show()


# # plt.figure()
# # plt.imshow(x.to_array()[0])
# # plt.show()


# # coeffs1 = sphv1.get_coeffs(90)
# # plt.figure()
# # plt.imshow(coeffs1[0])
# # plt.figure()
# # plt.imshow(coeffs1[1])


# # sphv2 = scorpy.SphericalVol(100, 180, 360, 1)
# # coeffs2 = sphv2.fill_random_sh(q=90, lmax=60)

# # plt.figure()
# # plt.imshow(coeffs2[0])
# # plt.figure()
# # plt.imshow(coeffs2[1])


# # plt.show()
