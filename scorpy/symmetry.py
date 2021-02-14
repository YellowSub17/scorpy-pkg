import numpy as np


##multiplicty matrices
# https://www.cryst.ehu.es/cryst/get_point_genpos.html

## space group/pointgroup list
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
    "P 1 21 1":6,
    "I 41 2 2": 375,
    "P 42 21 2": 371,
    "P 41": 350,
    "P 61 2 2": 472,
    "C 1 2 1": 9,
    "I 4":353,
    "P 65 2 2": 473,
    "P 43": 352,
    "F D 3 M": 499
    }


def identity():
    multiplicity = 2
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    total_sym_mat[0,...] = np.eye(3,3)
    total_sym_mat[1,...] = -1*np.eye(3,3)
    return total_sym_mat



def two_over_m():
    # Number of equivalent points
    multiplicity = 4
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]]) #2 fold rot on y
    total_sym_mat[2, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 3
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat



def mmm():
    # Number of equivalent points
    multiplicity = 8
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 2 fold rot on z
    total_sym_mat[2, ...] = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]]) #2 fold rot on y
    total_sym_mat[3, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 4
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat



def four_over_m():
    # Number of equivalent points
    multiplicity = 8
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 2 fold rot on z
    total_sym_mat[2, ...] = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])  # 4 fold rot on z
    total_sym_mat[3, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    #number of operations that have been filld
    ops_ind = 4
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat



def four_over_mmm():
    # Number of equivalent points
    multiplicity = 16
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 2 fold rot on z
    total_sym_mat[2, ...] = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]]) #2 fold rot on y
    total_sym_mat[3, ...] = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])  # 4 fold rot on z
    total_sym_mat[4, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 5
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat



def three_bar():
    # Number of equivalent points
    multiplicity = 6
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array([[0, -1, 0], [1, -1, 0], [0, 0, 1]])  #  3 fold rot on z
    total_sym_mat[2, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 3
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat



def three_bar_m():
    # Number of equivalent points
    multiplicity = 12
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array([[0, -1, 0], [1, -1, 0], [0, 0, 1]])  #  3 fold rot on z
    total_sym_mat[2, ...] = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]])  #2 fold rot on (1-10)
    total_sym_mat[3, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 4
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat



def six_over_m():
    # Number of equivalent points
    multiplicity = 12
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 2 fold rot on z
    total_sym_mat[2, ...] = np.array([[0, -1, 0], [1, -1, 0], [0, 0, 1]])  #  3 fold rot on z
    total_sym_mat[3, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 4
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat



def six_over_mmm():
    # Number of equivalent points
    multiplicity = 24
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 2 fold rot on z
    total_sym_mat[2, ...] = np.array([[0, -1, 0], [1, -1, 0], [0, 0, 1]])  #  3 fold rot on z
    total_sym_mat[3, ...] = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])    #2 fold rot on (1,1,0)
    total_sym_mat[4, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 5
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat



def m_three():
    # Number of equivalent points
    multiplicity = 24
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 2 fold rot on z
    total_sym_mat[2, ...] = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]]) #2 fold rot on y
    total_sym_mat[3, ...] = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])     # 3 fold rot on (1,1,1)
    total_sym_mat[4, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 5
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat



def m_three_m():
    # Number of equivalent points
    multiplicity = 48
    # init array of sym ops (each op is a 3x3 array, and there are multiplicity of them
    total_sym_mat = np.zeros((multiplicity, 3, 3))
    # input the basic generators into total array
    total_sym_mat[0, ...] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # identity
    total_sym_mat[1, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])  # 2 fold rot on z
    total_sym_mat[2, ...] = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]]) #2 fold rot on y
    total_sym_mat[3, ...] = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])     # 3 fold rot on (1,1,1)
    total_sym_mat[4, ...] = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])    #2 fold rot on (1,1,0)
    total_sym_mat[5, ...] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])  # inversion
    ops_ind = 6
    loop_generators(total_sym_mat, multiplicity, ops_ind)
    return total_sym_mat



def loop_generators(total_sym_mat,multiplicity, ops_ind):
    #while the last sym op in total_sym_op is empty (meaning there are still more sym ops to find...)
    while ops_ind < multiplicity:
        #loop through and get two operations
        for i in range(ops_ind):
            for j in range(ops_ind):
                #multiply the operations
                new_sym_mat = np.matmul(total_sym_mat[i, ...], total_sym_mat[j, ...])
                # Assume this is a new operation
                is_new_sym = True
                # loop through the syms ops that we have found
                for sym_mat in total_sym_mat[:ops_ind, ...]:
                    #check if we have already found this sym op
                    if np.array_equal(sym_mat, new_sym_mat):
                        #if we have, stop seaching for through the others and comparing them
                        is_new_sym = False
                        break
                #if the newly calculated operation is unlike the others we previously found
                if is_new_sym:
                    #insert it into the total sym operations matrix
                    total_sym_mat[ops_ind, ...] = new_sym_mat
                    #increment the number of found operations for the while loop
                    ops_ind += 1
    return total_sym_mat


def apply_sym(reflections, spg_code):
    # Look up the space group number of the cell
    HM_number = HM_NUMBER_DICT[spg_code]
    if HM_number == 1 or HM_number == 2:
        total_sym_mat = identity()
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

    new_reflections = np.zeros( (len(total_sym_mat) * len(reflections), 4) )

    for i, orig_reflection in enumerate(reflections):
        for j,sym_op in enumerate(total_sym_mat):
            new_reflection = np.matmul(sym_op, orig_reflection[:3].T)
            new_reflections[len(reflections)*j + i,:3] = new_reflection
            new_reflections[len(reflections)*j + i, 3] = orig_reflection[3]

    #remove 000 reflections
    loc_000 = np.all(new_reflections[:,:3]==0,axis=1)
    new_reflections = new_reflections[~loc_000]
    #get unique reflections 
    new_reflections = np.unique(new_reflections, axis=0)

    return new_reflections






