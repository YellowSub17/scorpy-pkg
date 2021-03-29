import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
plt.close('all')

nl = 10
ntheta = 360


tspace = np.linspace(0, 180, ntheta)

x1 = np.cos(np.linspace(0,np.pi, ntheta))
x2 = np.linspace(-1,1, ntheta)

x1=x2

plt.figure()
plt.plot(tspace, x1)


fmat1 = np.zeros( (ntheta, nl) )
fmat2 = np.zeros( (ntheta, nl) )

plt.figure()
for l in range(0, nl, 2):

    leg_poly = sp.special.legendre(l)
    fl1 = leg_poly(x1)
    # fl1 = np.polynomial.polynomial.polyval(x1, leg_poly)
    # fl1 = np.polynomial.legendre.legval(x1, np.identity(nl)[:,l])



    fl2 = sp.special.eval_legendre(l, x1)

    fmat1[:,l] = fl1
    fmat2[:,l] = fl2


    plt.subplot(121)
    plt.plot(x1,fl1, label=f'L={l}')
    plt.title('fmat1: leg -> polyval')
    plt.subplot(122)
    plt.plot(x1,fl2, label=f'L={l}')
    plt.title('fmat2: eval_legendre')


plt.figure()
plt.subplot(121)
plt.imshow(fmat1, aspect='auto')
plt.title('fmat1: leg -> polyval')
plt.xlabel('L')
plt.ylabel('theta')
plt.subplot(122)
plt.imshow(fmat2, aspect='auto')
plt.title('fmat2: eval_legendre')
plt.xlabel('L')
plt.ylabel('theta')




# plt.figure()
# plt.plot(x1)
# plt.plot(x2)

# plt.figure()
# plt.plot(x1, sp.special.eval_legendre(4, x1))
# plt.plot(x2, sp.special.eval_legendre(4, x1))






plt.show()

