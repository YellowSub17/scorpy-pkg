
import numpy as np




def index_x_wrap(x_val, x_min, x_max, nx):
    dx2 = (x_max - x_min) / (2*nx)
    x_out2 =(x_val-x_min)/(dx2)
    x_out = ( int(0.5*(x_out2+1)) %6)
    return int(x_out)



def index_x_nowrap(x_val, x_min, x_max, nx):
    x_val = max(x_min, x_val)
    x_val = min(x_max-1e-14, x_val)
    x_val = round(x_val, 15)
    dx = (x_max - x_min) / nx
    x_out = (x_val -x_min)/dx
    return int(x_out)


def index_xs(x_vals, x_min, x_max, nx, wrap=False):
    if wrap:

        dx2 = (x_max -x_min)/ (2*nx)
        x_out2 =(x_vals-x_min)/(dx2)

        x_out =  (x_out2+1)*0.5
        x_out = x_out.astype(int)%nx
        return x_out.astype(int)

    else:

        x_vals =np.maximum(x_vals, x_min)
        x_vals =np.minimum(x_vals, x_max-1e-14)

        x_vals = np.round(x_vals, 15)
        dx = (x_max - x_min) / nx
        x_out = (x_vals - x_min)/dx
        return x_out.astype(int)







def convert_rect2sph(xyz):
    '''
    convert an (x,y,z) point to (r, theta, phi)
    '''
    r = np.linalg.norm(xyz, axis=1)
    theta = np.arctan2(np.linalg.norm(xyz[:, :2], axis=1), xyz[:, 2])  # 0 -> pi (NS)
    phi = np.arctan2(xyz[:,1], xyz[:,0])
    phi[np.where(phi < 0)] = phi[np.where(phi < 0)] + 2 * np.pi  # 0 -> 2pi (EW)
    return np.array([r, theta, phi]).T


