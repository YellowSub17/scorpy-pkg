import numpy as np
from scipy import special




def index_xs(x_val, x_max, nx):
    norm = x_val/float(x_max)*(nx -1)
    return np.round(norm).astype(int)



def index_x(x_val, x_max, nx):
    return int(round((x_val/float(x_max))*(nx-1)))


def index_x2(x_val,x_min, x_max, nx):
    return int(round((float(x_val-x_min)/float(x_max-x_min))*(nx-1)))

def polar_angle_between(t1,t2):
    return np.abs((t1-t2+180)%360 -180)

def angle_between(q1,q2):
    dot = np.dot(q1, q2)
    if dot > 1:
        dot=1.0
    elif dot < -1:
        dot = -1.0

    return np.arccos(dot)



def norm01(arr):

    arr = np.array(arr)
    arr -=np.min(arr)
    arr /=np.max(arr)
    return arr





def ylm_wrapper(l,m, phi,theta, comp=False):
    if comp:
        # COMPLEX BASIS
        ylm = special.sph_harm(m,l, phi , theta)
    else:
        ## REAL BASIS
        if m < 0:
            ylm = (np.sqrt(2)*(-1)**m)*np.imag(special.sph_harm(np.abs(m),l, phi,theta))
        elif m > 0:
            ylm = (np.sqrt(2)*(-1)**m)*np.real(special.sph_harm(m,l, phi,theta))
        else:
            ylm = np.real(special.sph_harm(m,l, phi, theta))

    #2*sqrt(pi) ensures orthogonality
    ylm *= 2*np.sqrt(np.pi)
    return ylm









