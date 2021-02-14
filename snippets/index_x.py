





import numpy as np



def index_xs(x_val, x_max, nx):
    norm = x_val/float(x_max)*(nx -1)

    return np.round(norm).astype(int)


def index_x(x_val, x_max, nx):
    return int(round((x_val/float(x_max))*(nx-1)))






iin = np.array([45,90,120, 270])
q = index_xs( iin, 360, 100)

print(q)
