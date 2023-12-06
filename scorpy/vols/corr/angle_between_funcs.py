


import numpy as np






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


