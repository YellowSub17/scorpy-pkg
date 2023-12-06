
import numpy as np

from skimage.transform import warp_polar

def index_x(x_val, x_min, x_max, nx, wrap=False):
    '''Find the index of a value in an array between a maximum and minimum value.

    Arguments:
        x_val (): Value to be indexed
        x_min (): Minimum value in the range to index
        x_max (): Maximum value in the range to index
        nx (int): Number of bins in the range to index
        wrap (bool): If True, values in the last index will be placed in the 0th index.

    Returns:
        x_out (int): Index that x_val should be place within the range.
    '''

    dx = (x_max - x_min) / nx
    x_val = round(x_val, 14)


    if not wrap:
        x_out = (x_val - x_min) / dx
        if x_val == x_max:
            x_out = nx - 1
    else:
        if x_val <= x_min + dx / 2 or x_val >= x_max - dx / 2:
            x_out = 0

        else:
            x_out = index_x(x_val, x_min + dx / 2, x_max - dx / 2, nx - 1) + 1

    return int(x_out)



def convert_rect2sph(xyz):
    '''
    convert an (x,y,z) point to (r, theta, phi)
    '''
    r = np.linalg.norm(xyz, axis=1)
    theta = np.arctan2(np.linalg.norm(xyz[:, :2], axis=1), xyz[:, 2])  # 0 -> pi (NS)
    phi = np.arctan2(xyz[:,1], xyz[:,0])
    phi[np.where(phi < 0)] = phi[np.where(phi < 0)] + 2 * np.pi  # 0 -> 2pi (EW)
    return np.array([r, theta, phi]).T



def convert_rect2pol(xy):
    '''
    convert an (x,y) point to (r, phi)
    '''
    r = np.linalg.norm(xy, axis=1)

    phi = np.arctan2(xy[:, 1], xy[:, 0]) # angular polar coordinate of pixel
    phi[np.where(phi < 0)] = phi[np.where(phi < 0)] + 2*np.pi #angle measures from 0 to 2pi radians

    return np.array([r, phi]).T





def convert_pol2rect(rphi):
    pass

def convert_sph2rect(rtp):
    pass



def to_polar(im, rmax, cenx, ceny):
    x = warp_polar( im, center=(cenx,ceny), radius=rmax)
    return np.rot90(x, k=3)



