
import numpy as np
import matplotlib.pyplot as plt
import scorpy
plt.close('all')


nq=200
npsi=360
nl=50

qmax = 0.36992983463258367/3

cif = scorpy.CifData('../data/xtal/1al1-sf.cif', qmax)



corr1 = scorpy.CorrelationVol(nq, npsi, qmax)
corr1.fill_from_cif(cif)

blqq1 = scorpy.BlqqVol(nq, nl, qmax)
blqq1.fill_from_corr(corr1)

corr2 = scorpy.CorrelationVol(nq, npsi, qmax)
corr2.fill_from_blqq(blqq1)

sphv = scorpy.SphericalVol(nq,npsi, qmax)
sphv.fill_from_cif(cif)

q = np.unique(np.where(sphv.vol>0)[0])[0]
sphv.plot_slice(0, q)

blqq2 = scorpy.BlqqVol(nq, nl, qmax)
blqq2.fill_from_sphv(sphv)

corr3 = scorpy.CorrelationVol(nq, npsi, qmax)
corr3.fill_from_blqq(blqq2)




l = 4


# coeffs = sphv.get_coeffs(q)

# plt.figure();plt.imshow(coeffs[0])
# plt.figure();plt.imshow(coeffs[1])

# ls  = np.sum(coeffs, axis=0).sum(axis=1)
# plt.figure()
# plt.plot(ls)





# blqq1.plot_slice(2,l)
# plt.title('Blqq - corr->blqq')

# blqq2.plot_slice(2,l)
# plt.title('Blqq - sphv->blqq')


# for corr in [corr1, corr2, corr3]:
    # corr._nz -=20
    # corr._vol = corr.vol[...,10:-10]


# corr1.plot_slice(axis=0, index=q)
# plt.title('Corr - Original')

# corr2.plot_slice(axis=0, index=q)
# plt.title('Corr - corr->blqq->corr')

# corr3.plot_slice(axis=0, index=q)
# plt.title('Corr - sphv->blqq->corr')




corr1.plot_q1q2()
plt.title('Corr - Original')

corr2.plot_q1q2()
plt.title('Corr - corr->blqq->corr')

corr3.plot_q1q2()
plt.title('Corr - sphv->blqq->corr')




# corr1.plot_line(axis=0, in1=q, in2=q)
# plt.title('Corr - Original')

# corr2.plot_line(axis=0, in1=q, in2=q)
# plt.title('Corr - corr->blqq->corr')

# corr3.plot_line(axis=0, in1=q, in2=q)
# plt.title('Corr - sphv->blqq->corr')




blqq1.plot_slice(2,l)
plt.title('Blqq - corr->blqq')

blqq2.plot_slice(2,l)
plt.title('Blqq - sphv->blqq')


plt.figure()
plt.plot(blqq1.vol[:,q,l])
plt.title(f'Blqq - corr->blqq - {q},{l}')

plt.figure()
plt.plot(blqq2.vol[:,q,l])
plt.title(f'Blqq - sphv->blqq - {q},{l}')



# rel = scorpy.utils.mydiv(blqq1.vol, blqq2.vol)
# plt.figure()
# plt.plot(rel[:,q,l])

# plt.title(f'Blqq - Rel - {q},{l}')




# blqq1xy = blqq1.get_xy()
# blqq2xy = blqq2.get_xy()


# rel2 = scorpy.utils.mydiv(blqq1xy, blqq2xy)


# plt.figure()
# plt.plot(rel2[:,l])

# plt.title(f'Blqq - Rel2 - {q},{l}')







plt.show()












