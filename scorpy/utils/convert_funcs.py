
import numpy as np

from skimage.transform import warp_polar
import numba



@numba.njit()
def index_x_wrap(x_val, x_min, x_max, nx):
    dx2 = (x_max - x_min) / (2*nx)
    x_out2 =(x_val-x_min)/(dx2)
    x_out = ( int(0.5*(x_out2+1)) %6)
    return int(x_out)



@numba.njit()
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


# def index_xs_wrap(x_vals, x_min, x_max, nx):
    # dx2 = (x_max -x_min)/ (2*nx)
    # x_out2 =(x_vals-x_min)/(dx2)

    # x_out =  (x_out2+1)*0.5
    # x_out = x_out.astype(int)%6
    # return x_out.astype(int)







def convert_sqr2trianddiag(sqr):

    tri_flat = np.tril(sqr, k=-1).flatten()
    loc = np.where(np.tril(np.ones(sqr.shape),k=-1).flatten() !=0)
    tri_flat = tri_flat[loc]
    diag = np.diag(sqr)

    return tri_flat, diag



def convert_rect2pol(xy):
    '''
    convert an (x,y) point to (r, phi)
    '''
    r = np.linalg.norm(xy, axis=1)

    phi = np.arctan2(xy[:, 1], xy[:, 0]) # angular polar coordinate of pixel
    phi[np.where(phi < 0)] = phi[np.where(phi < 0)] + 2*np.pi #angle measures from 0 to 2pi radians

    return np.array([r, phi]).T






def convert_pol2rect(rphi):
    assert False, 'NOT IMPLEMENTED'



def convert_rect2sph(xyz):
    '''
    convert an (x,y,z) point to (r, theta, phi)
    '''
    r = np.linalg.norm(xyz, axis=1)
    theta = np.arctan2(np.linalg.norm(xyz[:, :2], axis=1), xyz[:, 2])  # 0 -> pi (NS)
    phi = np.arctan2(xyz[:,1], xyz[:,0])
    phi[np.where(phi < 0)] = phi[np.where(phi < 0)] + 2 * np.pi  # 0 -> 2pi (EW)
    return np.array([r, theta, phi]).T


def convert_sph2rect(rtp):

    sinp = np.sin(rtp[:,2])
    cosp = np.cos(rtp[:,2])
    cost = np.cos(rtp[:,1])
    sint = np.sin(rtp[:,1])

    x = rtp[:,0]*sint*cosp
    y = rtp[:,0]*sint*sinp
    z = rtp[:,0]*cost
    
    return np.array([x,y,z]).T



def to_polar(im, rmax, cenx, ceny):
    x = warp_polar( im, center=(cenx,ceny), radius=rmax)
    return np.rot90(x, k=3)



# def index_x(x_val, x_min, x_max, nx, wrap=False):
    # '''Find the index of a value in an array between a maximum and minimum value.

    # Arguments:
        # x_val (): Value to be indexed
        # x_min (): Minimum value in the range to index
        # x_max (): Maximum value in the range to index
        # nx (int): Number of bins in the range to index
        # wrap (bool): If True, values in the last index will be placed in the 0th index.

    # Returns:
        # x_out (int): Index that x_val should be place within the range.
    # '''

    # dx = (x_max - x_min) / nx
    # x_val = round(x_val, 14)


    # if not wrap:
        # x_out = (x_val - x_min) / dx
        # if x_val == x_max:
            # x_out = nx - 1
    # else:
        # if x_val <= x_min + dx / 2 or x_val >= x_max - dx / 2:
            # x_out = 0

        # else:
            # x_out = index_x(x_val, x_min + dx / 2, x_max - dx / 2, nx - 1) + 1

    # return int(x_out)
