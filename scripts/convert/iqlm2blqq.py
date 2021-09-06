
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')



nq = 81
ntheta = 18
nphi = 36
qmax = 1


nl = int(ntheta/2)


harms = []
for l in range(nl):
    for _, m in zip(range(2*l +1), range(-l, l+1)):
        harms.append((l, m))




iqlm =  scorpy.IqlmHandler(nq, nl, qmax)


for q_ind, harm in enumerate(harms):
    iqlm.set_val(q_ind, harm[0], harm[1])






blqq = scorpy.BlqqVol(nq, nl, qmax)

blqq.fill_from_iqlm(iqlm, inc_odds=True)

for l_ind in range(nl):
    blqq.plot_slice(2, l_ind)

plt.show()




