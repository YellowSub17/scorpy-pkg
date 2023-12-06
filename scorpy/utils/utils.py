import numpy as np
from scipy import special
from skimage.transform import warp_polar

import regex as re
# import sys, os

# def block_print():
    # sys.stdout = open(os.devnull, 'w')

# def enable_print():
    # sys.stdout = sys.__stdout__


import os
import contextlib


def verbose_dec(fn):

    def wrapper(*args, **kwargs):
        if 'verbose' in kwargs.keys() and kwargs['verbose']>0:
            result = fn(*args, **kwargs)
        else:
            with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
                result = fn(*args, **kwargs)
        return result

    return wrapper



def to_polar(im, rmax, cenx, ceny):
    x = warp_polar( im, center=(cenx,ceny), radius=rmax)
    return np.rot90(x, k=3)



def strerr2floaterrr(s):

    val, err = s.split('(')[0], s.split('(')[1][:-1]

    units = val.split('.')[0]
    # print(units)

    if units==val:
        err= float(err)
    else:
        ndeci = len(val.split('.')[1])
        err = float('0.'+(ndeci-1)*'0'+'1')*float(err)



    return float(val), float(err)






def concat_file(f):
    # print(f'Concantenating file: {f}')
    single_file_str = ''
    with open(f, 'r') as f:
        for line in f:
            single_file_str +=line

    return single_file_str




def grep(s, reg, fn=None):
    # print(f'greping reg: {reg}')
    found = re.findall(reg, s)
    if fn is not None:
        found = list(map(fn, found))
    return found





def rfactor(It, If):
    rf = np.sum(np.abs(It - If))/np.sum(np.abs(If))
    return rf








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

# def cosinesim(v1, v2):
    # v1f, v2f = v1.flatten(), v2.flatten()
    # sim = np.dot(np.conj(v1f / np.linalg.norm(v1f)), v2f / np.linalg.norm(v2f))
    # return sim

def cosinesim(v1, v2):
    v1f, v2f = v1.flatten(), v2.flatten()
    sim = np.dot(v1f, v2f)/ (np.linalg.norm(v1f) * np.linalg.norm(v2f))
    return sim



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


    





