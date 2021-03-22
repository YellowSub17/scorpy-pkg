import numpy as np
import scorpy
import matplotlib.pyplot as plt







cif = scorpy.CifData('../data/xtal/homebrew-sf.cif')

qmax = cif.qmax+0.1*cif.qmax
nq=50
ntheta=86
nl = 86

cor1 = scorpy.CorrelationVol(nq=nq, ntheta=ntheta, qmax=qmax)
cor1.correlate(cif.scattering)



bl1 = scorpy.BlqqVol(nq, nl, qmax)
bl1.fill_from_corr(cor1)

bl1l, bl1u = bl1.get_eig()


sph1 = scorpy.SphHarmHandler(nq, nl, qmax)
sph1.fill_from_cif(cif)

bl2 = scorpy.BlqqVol(nq,nl,qmax)
bl2.fill_from_sph(sph1)
bl2l, bl2u = bl2.get_eig()

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


if np.all(res):
    print('all bl_rel[...,l] a sf')
    plt.figure()
    plt.title('bl_rel[...,l]sf')
    plt.plot(sf)



else:
    print('WARNING bl_rel not sf')
    plt.figure()
    plt.title('!!!!bl_rel[...,l]sf')
    plt.plot(sf)





# cor1.plot_sumax()
# plt.title('correlation (sum)')
# cor1.plot_q1q2()
# plt.title('correlation (q1q2)')




# cor1.plot_slice(2,0)
# plt.title('cor theta=0')
# cor1.plot_slice(2,-1)
# plt.title('cor theta=180')

l = 46
bl1.plot_slice(2,l)
plt.title(f'blqq1 from cor (l={l})')
bl2.plot_slice(2,l)
plt.title(f'blqq2 from sph (l={l})')

bl_rel.plot_slice(2,l)
plt.title(f'blqq rel (l={l})')



# plt.figure()
# plt.imshow(bl1l)
# plt.figure()
# plt.imshow(bl2l)

# plt.figure()
# plt.plot(bl2l[:,l])

# plt.figure()
# plt.imshow(bl2u[:,:,l])






plt.show()
