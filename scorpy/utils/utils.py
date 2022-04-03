import numpy as np
from scipy import special
from skimage.transform import warp_polar

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
            fn(*args, **kwargs)
        else:
            with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
                fn(*args, **kwargs)

    return wrapper



def to_polar(im, rmax, cenx, ceny):
    x = warp_polar( im, center=(cenx,ceny), radius=rmax)
    return np.rot90(x, k=3)




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


def angle_between_pol(t1, t2):
    '''
    Calculate angluar difference between two polar angles.

    Arguments:
        t1 (): Angle 1 [degrees]
        t2 (): Angle 2 [degrees]

    Returns:
        psi (): Difference between t1 and t2, in degrees between 0 and 180
    '''
    psi = np.abs((t1 - t2 + 180) % 360 - 180)
    return psi

    # dot = np.cos(np.radians(psi))
    # return dot


def angle_between_rect(q1, q2):
    '''
    Calculate angle between two vectors.

    Arguments:
        q1 (): Vector 1
        q2 (): Vector 2

    Returns:
        psi (): Angle between q1 and q2 [radians]
    '''
    dot = np.dot(q1 / np.linalg.norm(q1), q2 / np.linalg.norm(q2))

    if dot > 1:
        dot = 1.0
    elif dot < -1:
        dot = -1.0

    return dot

    # psi = np.arccos(dot)
    # return psi


def angle_between_sph(theta1, theta2, phi1, phi2):
    '''Angle between two vectors defined by spherical corrdinates.

    Arguments:
        theta1 (): inclination angle of first vector [radians]
        theta2 (): inclination angle of second vector [radians]
        phi1 (): azimuthal angle of first vector [radians]
        phi2 (): azimuthal angle of second vector [radians]

    Returns:
        psi (): angle between vectors [radians]
    '''
    w1 = np.array([np.cos(phi1) * np.sin(theta1),
                   np.sin(phi1) * np.sin(theta1),
                   np.cos(theta1)])

    w2 = np.array([np.cos(phi2) * np.sin(theta2),
                   np.sin(phi2) * np.sin(theta2),
                   np.cos(theta2)])

    return angle_between_rect(w1, w2)


def cosinesim(v1, v2):
    v1f, v2f = v1.flatten(), v2.flatten()
    sim = np.dot(np.conj(v1f / np.linalg.norm(v1f)), v2f / np.linalg.norm(v2f))
    return sim



def convert_rect2sph(xyz):
    r = np.linalg.norm(xyz, axis=1)
    theta = np.arctan2(np.linalg.norm(xyz[:, :2], axis=1), xyz[:, 2])  # 0 -> pi (NS)
    phi = np.arctan2(xyz[:,1], xyz[:,0])
    phi[np.where(phi < 0)] = phi[np.where(phi < 0)] + 2 * np.pi  # 0 -> 2pi (EW)
    return np.array([r, theta, phi]).T




# def fsc(v1,v2):

    # ned =  np.sum(v1 * v2, axis = -1).sum(axis=-1)
    # donk = np.sqrt( np.sum(v1**2, axis= -1).sum(axis=-1) *  np.sum(v2**2, axis= -1).sum(axis=-1)   )

    # fsc = ned/donk
    # fsc = np.nan_to_num(fsc, copy=True, nan=0.0, posinf=None, neginf=None)

    # return fsc

