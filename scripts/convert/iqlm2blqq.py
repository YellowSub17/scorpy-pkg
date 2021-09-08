
import scorpy
import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt
plt.close('all')



nq = 81
ntheta = 18
nphi = 36
qmax = 1


nl = int(ntheta/2)


harms = scorpy.utils.harmonic_list(nl)



iqlm =  scorpy.IqlmHandler(nq, nl, qmax)




for q_ind in range(nq):
    lm = harms[np.random.randint(0, len(harms))]
    iqlm.add_val(q_ind, lm[0], lm[1])

    print(q_ind, lm)
    lm = harms[np.random.randint(0, len(harms))]
    iqlm.add_val(q_ind, lm[0], lm[1])
    print(q_ind, lm)







blqq = scorpy.BlqqVol(nq, nl, qmax)

blqq.fill_from_iqlm(iqlm)


blqq.plot_slice(2, 8)






plt.show()




