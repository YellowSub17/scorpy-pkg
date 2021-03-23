import numpy as np
import scorpy
import matplotlib.pyplot as plt





plt.close('all')

cif = scorpy.CifData('../data/xtal/homebrew-sf.cif')

qmax = cif.qmax+0.1*cif.qmax
nq=100
ntheta=360
nl = 46

cor1 = scorpy.CorrelationVol(nq=nq, ntheta=ntheta, qmax=qmax)
cor1.correlate(cif.scattering)



bl1 = scorpy.BlqqVol(nq, nl, qmax)
bl1.fill_from_corr(cor1)

bl1l, bl1u = bl1.get_eig(herm=False)


sph1 = scorpy.SphHarmHandler(nq, nl, qmax)
sph1.fill_from_cif(cif)

bl2 = scorpy.BlqqVol(nq,nl,qmax)
bl2.fill_from_sph(sph1)
bl2l, bl2u = bl2.get_eig(herm=False)

bl_rel = bl2.copy()
bl_rel.vol[np.where(bl1.vol !=0)] /= bl1.vol[np.where(bl1.vol !=0)]


res = np.zeros(bl_rel.nl)
sf = np.zeros(bl_rel.nl)

for l in range(bl_rel.nl):
    if l%2==1:
        res[l]=1
        continue
    qq = bl_rel.vol[...,l]
    loc = np.where(qq !=0)
    if np.all(qq[loc] == qq[loc][0]):
        res[l] = 1

    sf[l]=np.mean(qq[loc])/(2*l+1)
    sf[l]=np.mean(qq[loc])#/(2*l+1)

# plt.figure()
# plt.plot(sf)
# plt.xlabel('l')


if np.all(res):
    print('all bl_rel[...,l] a sf')
    # plt.title('bl_rel[...,l]sf')


else:
    print('WARNING bl_rel not sf')
    # plt.title('!!!!bl_rel[...,l]sf')





# cor1.plot_sumax()
# plt.title('correlation (sum)')
# cor1.plot_q1q2()
# plt.title('correlation (q1q2)')




# cor1.plot_slice(2,0)
# plt.title('cor theta=0')
# cor1.plot_slice(2,-1)
# plt.title('cor theta=180')

l = 6

# bl1.plot_slice(2,l)
# plt.title(f'blqq1 from cor (l={l})')
# plt.xlabel('q1')
# plt.ylabel('q1')

# bl2.plot_slice(2,l)
# plt.title(f'blqq2 from sph (l={l})')
# plt.xlabel('q1')
# plt.ylabel('q1')

# bl_rel.plot_slice(2,l)
# plt.title(f'blqq rel (blqq2/blqq1) (l={l})')
# plt.xlabel('q1')
# plt.ylabel('q1')



# plt.figure()
# plt.imshow(bl1l)
# plt.title('bl from cor eig vals')
# plt.xlabel('L')
# plt.ylabel('n')
# plt.figure()
# plt.imshow(bl2l)
# plt.title('bl from sph eig vals')
# plt.xlabel('L')
# plt.ylabel('n')


# plt.figure()
# plt.title(f'bl from cor eig vect (l={l})')
# plt.imshow(bl1u[:,:,l])
# plt.xlabel('n')
# plt.ylabel('q')


# plt.figure()
# plt.title(f'bl from sph eig vect (l={l})')
# plt.imshow(bl2u[:,:,l])
# plt.xlabel('n')
# plt.ylabel('q')



# plt.figure()
# plt.title(f'bl from cor eig vals (l={l})')
# plt.plot(bl1l[:,l])
# plt.xlabel('n')
# plt.ylabel('eigenvalue')

# plt.figure()
# plt.title(f'bl from sph eig vals (l={l})')
# plt.plot(bl2l[:,l])
# plt.xlabel('n')
# plt.ylabel('eigenvalue')


nq=0
plt.figure()
plt.title(f'bl from cor eig val (l={l}, q={nq})')
plt.plot(bl1l[nq,:], label='bl1l')
plt.xlabel('l')
plt.ylabel('eigenvalue')

plt.figure()
plt.title(f'bl from sph eig val (l={l}, q={nq})')
plt.plot(bl2l[nq,:], label='bl2l')
plt.xlabel('l')
plt.ylabel('eigenvalue')


# bl1lsf = np.zeros(bl1l.shape)
# bl1lsf[np.where(bl1l!=0)] = 1/bl1l[np.where(bl1l!=0)]
# ls = np.arange(0, bl2.nl)
# for l in range(1, bl2.nl,2):
    # ls[l]=0
# plt.figure()
# plt.title(f'TARGET SF for cor bl')
# plt.plot(bl1lsf[nq,:], label='bl1l')
# plt.xlabel('l')
# plt.ylabel('eigenvalue')

# plt.figure()
# plt.title(f'SF*cor bl')
# plt.plot(bl1l[nq,:]/(2*ls+1)**2, label='bl1l')
# plt.xlabel('l')
# plt.ylabel('eigenvalue')





ls = np.arange(0, bl2.nl)
plt.figure()
plt.title(f'bl from sph eig val (l={l}, q=0) / ( sum((2I)^2) * (2*l+1) )')
plt.plot(bl2l[0,:]*(1/(2*ls+1))*(1/(2*np.sum(cor1.get_xy()[:,0]))))
plt.xlabel('l')
plt.ylabel('eigenvalue')





plt.show()
