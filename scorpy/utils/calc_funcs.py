


import numpy as np


def rfactor(It, If):
    """Calculate the crystalographic R-factor between target and final (recovered) intensities.

        Parameters
        ----------
        It : np.ndarray
            Target intensities
        If : np.ndarray
            Final intensities

        Returns
        -------
        float
           R factor for the intensities
        """

    rf = np.sum(np.abs(It - If))/np.sum(np.abs(If))
    return rf



def saldin_theta(q, k):
    return np.pi/2 - np.arcsin(q/(2*k))




def cosinesim(v1, v2):
    v1f, v2f = v1.flatten(), v2.flatten()
    sim = np.dot(v1f, v2f)/ (np.linalg.norm(v1f) * np.linalg.norm(v2f))
    return sim

