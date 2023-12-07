



import numpy as np
import math

import numba





def angle_between_pol(t1, t2):
    psi = np.abs((t1 - t2 + np.pi) % (np.pi*2) - np.pi)
    return psi


def angle_between_pol_cos(t1, t2):
    psi = np.abs((t1 - t2 + np.pi) % (np.pi*2) - np.pi)
    return np.cos(psi)




def angle_between_rect(q1, q2):
    dot = np.dot(q1 / np.linalg.norm(q1), q2 / np.linalg.norm(q2))
    if dot > 1:
        dot = 1.0
    elif dot < -1:
        dot = -1.0
    psi = np.arccos(dot)
    return psi

def angle_between_rect_cos(q1, q2):
    dot = np.dot(q1 / np.linalg.norm(q1), q2 / np.linalg.norm(q2))
    if dot > 1:
        dot = 1.0
    elif dot < -1:
        dot = -1.0
    return dot

@numba.njit
def angle_between_rect_cos_x(x1, x2, x3, y1, y2, y3):
    magx = math.sqrt( x1**2 + x2**2 + x3**2 )
    magy = math.sqrt( y1**2 + y2**2 + y3**2 )

    dot = x1*y1 + x2*y2 + x3*y3
    dot *= 1/(magx*magy)

    if dot >1:
        dot=1.0
    if dot < -1:
        dot= -1.0
    return dot


@numba.njit
def angle_between_rect_x(x1, x2, x3, y1, y2, y3):
    magx = math.sqrt( x1**2 + x2**2 + x3**2 )
    magy = math.sqrt( y1**2 + y2**2 + y3**2 )

    dot = x1*y1 + x2*y2 + x3*y3
    dot *= 1/(magx*magy)

    if dot >1:
        dot=1.0
    if dot < -1:
        dot= -1.0

    a = math.acos(dot)
    return a






def angle_between_sph(theta1, theta2, phi1, phi2):
    w1 = np.array([np.cos(phi1) * np.sin(theta1),
                   np.sin(phi1) * np.sin(theta1),
                   np.cos(theta1)])

    w2 = np.array([np.cos(phi2) * np.sin(theta2),
                   np.sin(phi2) * np.sin(theta2),
                   np.cos(theta2)])

    return angle_between_rect(w1, w2)


def angle_between_sph_cos(theta1, theta2, phi1, phi2):
    w1 = np.array([np.cos(phi1) * np.sin(theta1),
                   np.sin(phi1) * np.sin(theta1),
                   np.cos(theta1)])

    w2 = np.array([np.cos(phi2) * np.sin(theta2),
                   np.sin(phi2) * np.sin(theta2),
                   np.cos(theta2)])

    return angle_between_rect_cos(w1, w2)


