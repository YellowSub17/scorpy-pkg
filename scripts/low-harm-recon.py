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


sphv_fname ='sphharm_sin_sphv'
corr_fname ='sphharm_sin_qcor'

# sphv_fname ='sphharm_sphv1'
# corr_fname ='sphharm_qcor1'

sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)

print('Spherical Harmonics:')
print('q:\tl:\tm:')
# for q_ind in range(nq):

    # coeffs = np.zeros((2, sphv.nl, sphv.nl))

    # cs_q = np.random.randint(0, 2)
    # l_q = np.random.randint(0, 9)
    # m_l = np.random.randint(0, l_q + 1)

    # while cs_q == 1 and m_l == 0:
        # cs_q = np.random.randint(0, 2)
        # m_l = np.random.randint(0, l_q + 1)

    # coeffs[cs_q, l_q, m_l] = 1
    # if cs_q ==0:
        # sign = '+'
    # else:
        # sign = '-'
    # print(q_ind, l_q, sign+str(m_l), sep='\t')
    # sphv.set_q_coeffs(q_ind, coeffs)

coeffs_key =  [ ( 0, 0, 0),
                ( 1, 2, 2),
                ( 1, 2, 1),
                ( 0, 2, 0),
                ( 0, 2, 1),
                ( 0, 2, 2),
                ( 0, 0, 0),
                ( 0, 4, 4),
                ( 1, 4, 4),
                ( 0, 4, 2),]



for q_ind, (cs, l, m) in enumerate(coeffs_key):
    coeffs = np.zeros((2, sphv.nl, sphv.nl))
    coeffs[cs, l, m] = 1
    sphv.set_q_coeffs(q_ind, coeffs)
    if cs ==0:
        sign = '+'
    else:
        sign = '-'
    print(q_ind, l, sign+str(m), sep='\t')



sphv_corred = scorpy.SphericalVol(path= f'{__DATADIR}/dbins/{sphv_fname}')
assert np.all(sphv_corred.vol == sphv.vol), 'WARNING: different coeffs in spherical volumes'







#SphericalVol of singular harmonics
sphv = scorpy.SphericalVol(path= f'{__DATADIR}/dbins/{sphv_fname}')



# klnm = scorpy.KlnmHandler(5, nq)
# klnm.fill_ilm(sphv)











#BlqqVol from SphericalVol of singular harmonics
blqq1 = scorpy.BlqqVol(nq, sphv.nl, qmax)
blqq1.fill_from_sphv(sphv)


#CorrelationVol from SphericalVol of single spherical harmonics
corr1 = scorpy.CorrelationVol(path=f'{__DATADIR}/dbins/{corr_fname}.dbin')


#BlqqVol from CorrelationVol from SphericalVol of single spherical harmonics
blqq2 = scorpy.BlqqVol(nq, sphv.nl, qmax)
blqq2.fill_from_corr(corr1, inc_odds=False)


#CorrelationVol from BlqqVol from CorrelationVol from SphericalVol of single spherical harmonics
corr2 = scorpy.CorrelationVol(nq, nphi, qmax)
corr2.fill_from_blqq(blqq2, inc_odds=False)


#CorrelationVol from BlqqVol from SphericalVol of single spherical harmonics
corr3 = scorpy.CorrelationVol(nq, nphi, qmax)
corr3.fill_from_blqq(blqq1, inc_odds=False)

#BlqqVol from CorrelationVol from BlqqVol from SphericalVol of single spherical harmonics
blqq3 = scorpy.BlqqVol(nq, sphv.nl, qmax)
blqq3.fill_from_corr(corr3, inc_odds=False)

#CorrelationVol from BlqqVol from CorrelationVol from BlqqVol from SphericalVol of single spherical harmonics
corr4 = scorpy.CorrelationVol(nq, nphi, qmax)
corr4.fill_from_blqq(blqq3, inc_odds=False)



sphv.plot_slice(0, 4)
plt.title('sphv')

for i, corr in enumerate([corr1, corr2, corr3]):
    corr.plot_q1q2()
    plt.title(f'corr{i+1}')


l = 2
for i, blqq in enumerate([blqq1,blqq2, ]):
    blqq.plot_slice(2,l)
    plt.title(f'blqq{i+1}, l={l}')

plt.show()








