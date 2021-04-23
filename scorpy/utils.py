import numpy as np
from scipy import special








# def index_x(x_val, x_max, nx):
    # return int(round((x_val/float(x_max))*(nx-1)))

def index_x(x_val,x_min, x_max, nx):
    return np.int(np.round(np.interp(x_val, (x_min, x_max), (0, nx-1))))




# def index_x_arr(x_vals, x_max, nx):
    # return np.round((x_vals/float(x_max))*(nx-1)).astype(int)

def polar_angle_between(t1,t2):
    return np.abs((t1-t2+180)%360 -180)

def angle_between(q1,q2):
    dot = np.dot(q1/np.linalg.norm(q1), q2/np.linalg.norm(q2))
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


def cosinesim(v1,v2):
    v1f, v2f = v1.flatten(), v2.flatten()
    sim = np.dot(np.conj(v1f/np.linalg.norm(v1f)), v2f/np.linalg.norm(v2f))
    return sim





def ylm_wrapper(l,m, phi,theta, comp=False):
    if comp:
        # COMPLEX BASIS
        ylm = special.sph_harm(m,l, phi , theta)
    else:
        ## REAL BASIS
        # print(l,m,phi,theta)
        if m < 0:
            ylm = (np.sqrt(2)*(-1)**m)*np.imag(special.sph_harm(np.abs(m),l, phi,theta))
        elif m > 0:
            ylm = (np.sqrt(2)*(-1)**m)*np.real(special.sph_harm(m,l, phi,theta))
        else:
            ylm = np.real(special.sph_harm(m,l, phi, theta))

    #2*sqrt(pi) ensures orthogonality
    ylm *= 2*np.sqrt(np.pi)
    return ylm



def ylm_wrapper2(l,m,phi,theta, comp=False):

    term_a = ((-1)**m)*(np.sqrt(2))
    term_b = np.sqrt( (2*l+1)/(4*np.pi) )

    fact = np.math.factorial(l-np.abs(m))/np.math.factorial(l+np.abs(m))


    leg =  special.lpmv(np.abs(m), l, np.cos(theta))

    if m<0:
        ylm = term_a*term_b*fact*leg*np.sin(np.abs(m)*phi)
    elif m>0:
        ylm = term_a*term_b*fact*leg*np.cos(m*phi)
    else:
        ylm = term_b*leg

    ylm *= 2*np.sqrt(np.pi)
    return ylm









