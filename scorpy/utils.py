import numpy as np





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

