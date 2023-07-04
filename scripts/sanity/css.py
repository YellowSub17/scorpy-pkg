
import scorpy
import numpy as np


nx = 2**12
print(nx)

css_ab = []
css_a_ab = []
for i in range(5):
    x = np.random.random(nx)
    x[np.where(x<0.4)] =0
    x[np.where(x>=0.4)] =1

    # x[:int(nx/4)] =1
    xa = x[:int(nx/2)]
    xb = x[int(nx/2):]

    xaa = xa[:int(nx/4)]
    xab = xa[int(nx/4):]

    css = scorpy.utils.utils.cosinesim(xa, xb)
    css_ab.append(css)
    css = scorpy.utils.utils.cosinesim(xaa, xab)
    css_a_ab.append(css)


print(np.mean(css_ab), '+/-', np.std(css_ab))
print(np.mean(css_a_ab), '+/-', np.std(css_a_ab))
# x1 = np.ones(nx)
# x2 = np.random.random(nx)
# x3 = np.random.random(nx)


# x1[::3] = 0
# x2[::3] = 0

# css = scorpy.utils.utils.cosinesim(x1,x2)
# print(css)

# css = scorpy.utils.utils.cosinesim(x2,x3)
# print(css)

# css = scorpy.utils.utils.cosinesim(x3,x1)
# print(css)
