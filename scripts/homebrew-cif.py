import numpy as np
import scorpy
import matplotlib.pyplot as plt
import scipy





plt.close('all')


#open homebrew cif file
cif = scorpy.CifData('../data/xtal/homebrew-sf.cif')

#arguments
qmax = cif.qmax+0.1*cif.qmax
nq=20
ntheta=360*4
nl = 37
iq=-1
il=6


#create correlation volume
cor1 = scorpy.CorrelationVol(nq=nq, ntheta=ntheta, qmax=qmax)
#correlate
cor1.correlate(cif.scattering)

cor1.vol[...,-1]=0

cor1.plot_q1q2()
plt.title('cor q1q2')

cor1.plot_sumax()
plt.title('cor sumax')


#create spherical harmonic handler
sph1 = scorpy.SphHarmHandler(nq, nl, qmax)
#calculate spherical harmonics from cif
sph1.fill_from_cif(cif)

#BL1: Blqq volume from the correlation data
bl1 = scorpy.BlqqVol(nq, nl, qmax)
bl1.fill_from_corr(cor1)
bl1l, bl1u = bl1.get_eig(herm=True)

#BL2: Blqq volume from the spherical harmonics
bl2 = scorpy.BlqqVol(nq,nl,qmax)
bl2.fill_from_sph(sph1)
bl2l, bl2u = bl2.get_eig(herm=True)



plt.figure()
plt.title(f'Eigenvalues of Blqq from Correlation')
plt.imshow(bl1l, label='bl1l')
plt.xlabel('l')
plt.ylabel('q')

plt.figure()
plt.title(f'Eigenvalues of Blqq from Spherical Harmonics')
plt.imshow(bl2l, label='bl1l')
plt.xlabel('l')
plt.ylabel('q')


plt.figure()
plt.title(f'Eigenvalues of Blqq from Spherical Harmonics (iq={iq})')
plt.plot(bl2l[iq,:], label='bl2l')
plt.xlabel('l')
plt.ylabel('eigenvalue')

bl2lsf = 1/(2*np.arange(0, bl2.nl)+1)*1/(2*np.sum(cor1.get_xy()[:,0]))
plt.figure()
plt.title(f'Eigenvalues of Blqq from Spherical Harmonics *SF (iq={iq})')
plt.plot(bl2lsf*bl2l[iq,:])
plt.xlabel('l')
plt.ylabel('eigenvalue')



plt.figure()
plt.title(f'Eigenvalues of Blqq from Correlation (iq={iq})')
plt.plot(bl1l[iq,:], label='bl1l')
plt.xlabel('l')
plt.ylabel('eigenvalue')



bl1l_sf_target = np.zeros(bl1.nl)
bl1l_sf_target[::2] = 1/bl1l[iq, ::2]

x = np.arange(0, bl1.nl, 2)
y = bl1l_sf_target[::2]

fit, cov_fit =  scipy.optimize.curve_fit(lambda x,a,b,c: a/(b*x+c), x,y)
fit2, cov_fit2 =  scipy.optimize.curve_fit(lambda x,a,b,c: a*np.exp(b*x)+c, x,y)

xfit = np.linspace(0, bl1.nl, 100)

plt.figure()
plt.title(f'Target SF for Eigenvalues of Blqq from Correlation (iq={iq})')
plt.plot(bl1l_sf_target, label='Target SF')
plt.plot(x,y, label='Fit Data')
plt.plot(xfit, fit[0]/(fit[1]*xfit +fit[2]), label='Fit')
plt.xlabel('l')
plt.ylabel('sf')
plt.legend()




bl1l_sf = fit[0]/(fit[1]*np.arange(0, bl1.nl) +fit[2]) 

# bl1l_sf = fit2[0]*np.exp(fit2[1]*np.arange(0, bl1.nl))+fit2[2]

# bl1l_sf = 1/(2*np.arange(0, bl1.nl)+1)

plt.figure()
plt.title(f'Eigenvalues of Blqq from Correlation *SF (iq={iq})')
# plt.plot(bl1l_sf[:45]*bl1l[iq,:45])
plt.plot(bl1l_sf*bl1l[iq,:])
plt.xlabel('l')
plt.ylabel('eigenvalue')




plt.show()
