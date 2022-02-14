import numpy as np
from scipy import special
from skimage.transform import warp_polar

import sys, os

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def to_polar(im, rmax, cenx, ceny):
    x = warp_polar( im, center=(cenx,ceny), radius=rmax)
    return np.rot90(x, k=3)


def harmonic_list(nl, lmin=0,  inc_odds=True):

    if inc_odds:
        lskip = 1
    else:
        lskip = 2

    harms = []
    for l in range(lmin, nl, lskip):
        for _, m in zip(range(2*l +1), range(-l, l+1)):
            harms.append((l, m))

    return harms


def convert_r2q(r, z, lam):
    k = np.pi*2/lam
    theta = np.arctan2(r, z)
    return 2*k*np.sin(theta/2)

def convert_q2r(q, z, lam):
    k = np.pi*2/lam
    arcs = np.arcsin(q/(2*k))
    return np.tan(2*arcs)*z


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
    # return psi

    dot = np.cos(np.radians(psi))
    return dot


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
    # TODO docstring
    v1f, v2f = v1.flatten(), v2.flatten()
    sim = np.dot(np.conj(v1f / np.linalg.norm(v1f)), v2f / np.linalg.norm(v2f))
    return sim



# multiplicty matrices
# https://www.cryst.ehu.es/cryst/get_point_genpos.html

# space group/pointgroup list
# http://pmsl.planet.sci.kobe-u.ac.jp/~seto/?page_id=37&lang=en
HM_NUMBER_DICT = {
    'I 2 2 2': 123,
    'P 1': 1,
    'P 21 21 21': 115,
    'P 21 21 2': 112,
    'P 21 3': 492,
    'P 2 3': 489,
    'I 41 3 2': 510,
    'I 21 3': 493,
    'P 31 2 1': 441,
    'P 32 2 1': 443,
    'I 1 2 1': 11,
    "P 41 21 2": 369,
    "P 43 21 2": 373,
    "P 41 2 2": 368,
    "P 1 21 1": 6,
    "I 41 2 2": 375,
    "P 42 21 2": 371,
    "P 41": 350,
    "P 61 2 2": 472,
    "C 1 2 1": 9,
    "I 4": 353,
    "P 65 2 2": 473,
    "P 43": 352,
    "F D 3 M": 499,
    "P 63": 467,
}



def identity():
    multiplicity = 1
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    total_sym_mat[0, ...] = np.eye(3, 3)
    return total_sym_mat



def friedel():
    multiplicity = 2
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    total_sym_mat[0, ...] = np.eye(3, 3)
    total_sym_mat[1, ...] = -1 * np.eye(3, 3)
    return total_sym_mat


def two_over_m():
    # Number of equivalent points
    multiplicity = 4
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array(
        [[-1, 0, 0], [0, 1, 0], [0, 0, -1]])  # 2 fold rot on y
    total_sym_mat[2, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 3
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat


def mmm():
    # Number of equivalent points
    multiplicity = 8
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 2 fold rot on z
    total_sym_mat[2, ...] = np.array(
        [[-1, 0, 0], [0, 1, 0], [0, 0, -1]])  # 2 fold rot on y
    total_sym_mat[3, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 4
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat


def four_over_m():
    # Number of equivalent points
    multiplicity = 8
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 2 fold rot on z
    total_sym_mat[2, ...] = np.array(
        [[0, -1, 0], [1, 0, 0], [0, 0, 1]])  # 4 fold rot on z
    total_sym_mat[3, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    # number of operations that have been filld
    ops_ind = 4
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat


def four_over_mmm():
    # Number of equivalent points
    multiplicity = 16
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 2 fold rot on z
    total_sym_mat[2, ...] = np.array(
        [[-1, 0, 0], [0, 1, 0], [0, 0, -1]])  # 2 fold rot on y
    total_sym_mat[3, ...] = np.array(
        [[0, -1, 0], [1, 0, 0], [0, 0, 1]])  # 4 fold rot on z
    total_sym_mat[4, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 5
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat


def three_bar():
    # Number of equivalent points
    multiplicity = 6
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array(
        [[0, -1, 0], [1, -1, 0], [0, 0, 1]])  # 3 fold rot on z
    total_sym_mat[2, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 3
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat


def three_bar_m():
    # Number of equivalent points
    multiplicity = 12
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array(
        [[0, -1, 0], [1, -1, 0], [0, 0, 1]])  # 3 fold rot on z
    total_sym_mat[2, ...] = np.array(
        [[0, -1, 0], [-1, 0, 0], [0, 0, -1]])  # 2 fold rot on (1-10)
    total_sym_mat[3, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 4
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat


def six_over_m():
    # Number of equivalent points
    multiplicity = 12
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 2 fold rot on z
    total_sym_mat[2, ...] = np.array(
        [[0, -1, 0], [1, -1, 0], [0, 0, 1]])  # 3 fold rot on z
    total_sym_mat[3, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 4
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat


def six_over_mmm():
    # Number of equivalent points
    multiplicity = 24
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 2 fold rot on z
    total_sym_mat[2, ...] = np.array(
        [[0, -1, 0], [1, -1, 0], [0, 0, 1]])  # 3 fold rot on z
    total_sym_mat[3, ...] = np.array(
        [[0, 1, 0], [1, 0, 0], [0, 0, -1]])  # 2 fold rot on (1,1,0)
    total_sym_mat[4, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 5
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat


def m_three():
    # Number of equivalent points
    multiplicity = 24
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 2 fold rot on z
    total_sym_mat[2, ...] = np.array(
        [[-1, 0, 0], [0, 1, 0], [0, 0, -1]])  # 2 fold rot on y
    total_sym_mat[3, ...] = np.array(
        [[0, 0, 1], [1, 0, 0], [0, 1, 0]])     # 3 fold rot on (1,1,1)
    total_sym_mat[4, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 5
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat


def m_three_m():
    # Number of equivalent points
    multiplicity = 48
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 2 fold rot on z
    total_sym_mat[2, ...] = np.array(
        [[-1, 0, 0], [0, 1, 0], [0, 0, -1]])  # 2 fold rot on y
    total_sym_mat[3, ...] = np.array(
        [[0, 0, 1], [1, 0, 0], [0, 1, 0]])     # 3 fold rot on (1,1,1)
    total_sym_mat[4, ...] = np.array(
        [[0, 1, 0], [1, 0, 0], [0, 0, -1]])  # 2 fold rot on (1,1,0)
    total_sym_mat[5, ...] = np.array(
        [[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 6
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat


def loop_generators(total_sym_mat, multiplicity, ops_ind):
    # while the last sym op in total_sym_op is empty (meaning there are still more sym ops to find...)
    while ops_ind < multiplicity:
        # loop through and get two operations
        for i in range(ops_ind):
            for j in range(ops_ind):
                # multiply the operations
                new_sym_mat = np.matmul(
                    total_sym_mat[i, ...], total_sym_mat[j, ...])
                # Assume this is a new operation
                is_new_sym = True
                # loop through the syms ops that we have found
                for sym_mat in total_sym_mat[:ops_ind, ...]:
                    # check if we have already found this sym op
                    if np.array_equal(sym_mat, new_sym_mat):
                        # if we have, stop seaching for through the others and comparing them
                        is_new_sym = False
                        break
                # if the newly calculated operation is unlike the others we previously found
                if is_new_sym:
                    # insert it into the total sym operations matrix
                    total_sym_mat[ops_ind, ...] = new_sym_mat
                    # increment the number of found operations for the while loop
                    ops_ind += 1
    return total_sym_mat


def apply_sym(reflections, spg_code):
    # Look up the space group number of the cell

    if spg_code in HM_NUMBER_DICT.keys():
        HM_number = HM_NUMBER_DICT[spg_code]
    else:
        HM_number = -1

    if HM_number == 1 or HM_number == 2:
        total_sym_mat = friedel()
    elif HM_number >= 3 and HM_number <= 107:
        total_sym_mat = two_over_m()
    elif HM_number >= 108 and HM_number <= 348:
        total_sym_mat = mmm()
    elif HM_number >= 349 and HM_number <= 365:
        total_sym_mat = four_over_m()
    elif HM_number >= 366 and HM_number <= 429:
        total_sym_mat = four_over_mmm()
    elif HM_number >= 430 and HM_number <= 437:
        total_sym_mat = three_bar()
    elif HM_number >= 438 and HM_number <= 461:
        total_sym_mat = three_bar_m()
    elif HM_number >= 462 and HM_number <= 470:
        total_sym_mat = six_over_m()
    elif HM_number >= 471 and HM_number <= 488:
        total_sym_mat = six_over_mmm()
    elif HM_number >= 489 and HM_number <= 502:
        total_sym_mat = m_three()
    elif HM_number >= 503 and HM_number <= 530:
        total_sym_mat = m_three_m()
    else:
        print('WARNING: NO SYMETERY APPLIED')
        print(f'spg: {spg_code}, pg: {HM_number}')
        total_sym_mat = identity()

    new_reflections = np.zeros((len(total_sym_mat) * len(reflections), 4))

    for i, orig_reflection in enumerate(reflections):
        for j, sym_op in enumerate(total_sym_mat):
            new_reflection = np.matmul(sym_op, orig_reflection[:3].T)
            new_reflections[len(reflections) * j + i, :3] = new_reflection
            new_reflections[len(reflections) * j + i, 3] = orig_reflection[3]

    # remove 000 reflections
    loc_000 = np.all(new_reflections[:, :3] == 0, axis=1)
    new_reflections = new_reflections[~loc_000]
    # get unique reflections
    new_reflections = np.unique(new_reflections, axis=0)

    return new_reflections
