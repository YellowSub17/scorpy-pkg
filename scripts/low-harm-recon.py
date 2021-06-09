import numpy as np
import scorpy
from scorpy import __DATADIR
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

print('Spherical Harmonics:')
print('q:\tl:\tm:')
for q_ind in range(nq):

    coeffs = np.zeros((2, sphv.nl, sphv.nl))

    cs_q = np.random.randint(0, 2)
    l_q = np.random.randint(0, 9)
    m_l = np.random.randint(0, l_q + 1)

    while cs_q == 1 and m_l == 0:
        cs_q = np.random.randint(0, 2)
        m_l = np.random.randint(0, l_q + 1)

    coeffs[cs_q, l_q, m_l] = 1
    if cs_q ==0:
        sign = '+'
    else:
        sign = '-'
    print(q_ind, l_q, sign+str(m_l), sep='\t')

    sphv.set_q_coeffs(q_ind, coeffs)


sphv_corred = scorpy.SphericalVol(path= f'{__DATADIR}/dbins/sphharm_sphv')
assert np.all(sphv_corred.vol == sphv.vol), 'WARNING: different coeffs in spherical volumes'






#SphericalVol of singular harmonics
sphv = scorpy.SphericalVol(path= f'{__DATADIR}/dbins/sphharm_sphv')


#BlqqVol from SphericalVol of singular harmonics
blqq1= scorpy.BlqqVol(nq, sphv.nl, qmax)
blqq1.fill_from_sphv(sphv)


#CorrelationVol from SphericalVol of single spherical harmonics
corr1 = scorpy.CorrelationVol(path=f'{__DATADIR}/dbins/sphharm_qcor.dbin')


#BlqqVol from CorrelationVol from SphericalVol of single spherical harmonics
blqq2= scorpy.BlqqVol(nq, sphv.nl, qmax)
blqq2.fill_from_corr(corr1, inc_odds=False)


#CorrelationVol from BlqqVol from CorrelationVol from SphericalVol of single spherical harmonics
corr2 = scorpy.CorrelationVol(nq, nphi, qmax)
corr2.fill_from_blqq(blqq2, inc_odds=False)


#CorrelationVol from BlqqVol from SphericalVol of single spherical harmonics
corr3 = scorpy.CorrelationVol(nq, nphi, qmax)
corr3.fill_from_blqq(blqq1, inc_odds=False)




for i, corr in enumerate([corr1, corr2, corr3]):
    corr.plot_slice(2,2)
    plt.title(f'corr{i+1}')


l = 8
for i, blqq in enumerate([blqq1, blqq2]):
    blqq.plot_slice(2,l)
    plt.title(f'blqq{i+1}, l={l}')

plt.show()




















# blqq_from_sphv = scorpy.BlqqVol(nq, sphv.nl, qmax)
# blqq_from_sphv.fill_from_sphv(sphv)
# corr_from_blqq_from_sphv = scorpy.CorrelationVol(nq, nphi, qmax)
# corr_from_blqq_from_sphv.fill_from_blqq(blqq_from_sphv)

# blqq_from_corr_from_sphv = scorpy.BlqqVol(nq, sphv.nl, qmax)
# blqq_from_corr_from_sphv.fill_from_corr(corr_from_sphv)
# corr_from_blqq_from_corr_from_sphv = scorpy.CorrelationVol(nq, nphi, qmax)
# corr3.fill_from_blqq(blqq2)


# corr2.plot_slice(2,0, extent=0)
# plt.title('sphv - blqq - corr')
# corr3.plot_slice(2,0, extent=0)
# plt.title('sphv - corr - blqq - corr')
# corr_from_sphv.plot_slice(2,0, extent=0)
# plt.title('sphv - corr')

# corr2.plot_q1q2(extent=0)
# plt.title('sphv - blqq - corr')
# corr3.plot_q1q2(extent=0)
# plt.title('sphv - corr - blqq - corr')
# corr_from_sphv.plot_q1q2(extent=0)
# plt.title('sphv - corr')

# plt.show()



