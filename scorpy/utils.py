import numpy as np
from scipy import special









def index_x(x_val,x_min, x_max, nx):
    return np.int(np.round(np.interp(x_val, (x_min, x_max), (0, nx-1))))



def angle_between_pol(t1,t2):
    return np.abs((t1-t2+180)%360 -180)

def angle_between_rect(q1,q2):
    dot = np.dot(q1/np.linalg.norm(q1), q2/np.linalg.norm(q2))
    if dot > 1:
        dot=1.0
    elif dot < -1:
        dot = -1.0

    return np.arccos(dot)

def angle_between_sph(theta1,theta2,phi1,phi2):

    sinterm = np.sin(theta1)*np.sin(theta2)
    costerm = np.cos(theta1)*np.cos(theta2)*np.cos(phi2-phi1)

    addterm = sinterm+costerm

    if addterm>1:
        addterm=1
    elif addterm < -1:
        addterm =-1


    return np.round(np.arccos(addterm),14)



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







