#!/usr/bin/env python3
'''
blqq-comp.py

Calculate the blqq matrix with various methods and compare the results.
'''



import scorpy
import matplotlib.pyplot as plt
import numpy as np


plt.close('all')



def cosinesim(v1,v2):
    v1f, v2f = v1.flatten(), v2.flatten()
    sim = np.dot(np.conj(v1f/np.linalg.norm(v1f)), v2f/np.linalg.norm(v2f))
    return sim

cor = scorpy.CorrelationVol(path='../data/dbins/1al1_qcor')
cif = scorpy.CifData('../data/xtal/1al1-sf.cif',qmax=cor.qmax)

comp = False

blqq_base =scorpy.BlqqVol(cor.nq, 17, cor.qmax, comp=comp)
sphharm_base = scorpy.SphHarmHandler(cor.nq, 17, cor.qmax, comp=comp)
iv_base = scorpy.SphInten(cor.nq, 2**5, cor.qmax)





blqq1 = blqq_base.copy()
blqq1.fill_from_corr(cor)
lam1, u1 = blqq1.get_eig(herm=True)
lam1a, u1a = blqq1.get_eig(herm=False)


sph2 = sphharm_base.copy()
sph2.fill_from_cif(cif)
blqq2 = blqq_base.copy()
blqq2.fill_from_sph(sph2)
lam2, u2 = blqq2.get_eig(herm=True)
lam2a, u2a = blqq2.get_eig(herm=False)

iv3 = iv_base.copy()
iv3.fill_from_cif(cif)
sph3 = sphharm_base.copy()
sph3.fill_from_ivol(iv3)
blqq3 = blqq_base.copy()
blqq3.fill_from_sph(sph3)
lam3, u3 = blqq3.get_eig(herm=True)
lam3a, u3a = blqq3.get_eig(herm=False)



# blqq1.convolve()
# blqq2.convolve()
# blqq3.convolve()



# ls = [0, 8, 10,16]
# for l in ls:
    # blqq1.plot_slice(2, l)
    # plt.title(f'bl1: cif -> cor -> blqq (l={l})')

    # blqq2.plot_slice(2, l)
    # plt.title(f'bl2: cif -> sph -> blqq (l={l})')

    # blqq3.plot_slice(2, l)
    # plt.title(f'bl3: cif -> ivol -> sph -> blqq (l={l})')

# print(f'Cosine Sim (1-2): {cosinesim(blqq1.vol, blqq2.vol)}\n')
# print(f'Cosine Sim (1-3): {cosinesim(blqq1.vol, blqq3.vol)}\n')
# print(f'Cosine Sim (2-3): {cosinesim(blqq2.vol, blqq3.vol)}\n')



# l = 8

# plt.figure()
# plt.imshow(np.log10(np.abs(lam1)+1), aspect='auto')
# plt.colorbar()
# plt.title('blqq1 lamda: cif -> cor -> blqq')
# plt.xlabel('L')
# plt.ylabel('nq')

# plt.figure()
# plt.imshow(np.log10(np.abs(lam2)+1), aspect='auto')
# plt.colorbar()
# plt.title('blqq2 lamda: cif -> sph -> blqq')
# plt.xlabel('L')
# plt.ylabel('nq')

# plt.figure()
# plt.imshow(np.log10(np.abs(lam3)+1), aspect='auto')
# plt.colorbar()
# plt.title('blqq3 lamda: cif -> ivol -> sph -> blqq')
# plt.xlabel('L')
# plt.ylabel('nq')





l = 8
inner=6
nqs = np.arange(inner, cor.nq-inner)
plt.figure()
if inner==0:
    plt.plot(nqs,lam1[:,l])
else:
    plt.plot(nqs,lam1[inner:-inner,l])
plt.ylabel('Eigenvalue')
plt.xlabel('nq')
plt.title('blqq1 lamda: cif -> cor -> blqq')

plt.figure()
if inner==0:
    plt.plot(nqs,lam2[:,l])
else:
    plt.plot(nqs,lam2[inner:-inner,l])
plt.ylabel('Eigenvalue')
plt.xlabel('nq')
plt.title('blqq2 lamda: cif -> sph -> blqq')

plt.figure()
if inner==0:
    plt.plot(nqs,lam3[:,l])
else:
    plt.plot(nqs,lam3[inner:-inner,l])
plt.ylabel('Eigenvalue')
plt.xlabel('nq')
plt.title('blqq3 lamda: cif -> ivol -> sph -> blqq')



plt.show()







# blqq3 = scorpy.BlqqVol(nq,nl,qmax)

# for l in range(0, nl, 2):
    # lam1 = lam[:,l]
    # u1 = u[...,l]

    # x = np.matmul(u1, np.diag(lam1))
    # blqq3.vol[...,l] = np.matmul(x, np.linalg.inv(u1))




# blqq1.plot_slice(2,6)
# plt.title('Correlation Blqq')
# blqq2.plot_slice(2,6)
# plt.title('Spherical Harmonics Blqq')
# blqq3.plot_slice(2,6)
# plt.title('Corr. Eigen Recon Blqq')












# plt.show()







