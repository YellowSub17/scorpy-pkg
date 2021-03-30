

from .vol import Vol
import numpy as np
from scipy import special
import matplotlib.pyplot as plt
import pyshtools as pysh



class SphericalVol(Vol):
    '''
    Representation of a spherical coordinate volume.

    Arguments:
        nq (int): number of scattering magnitude bins.
        n_angle: number of angluar bins
        qmax (float): scattering magnitude limit [1/A].
        grid_type: type of sampling grid. See https://shtools.oca.eu/shtools/public/grid-formats.html for info
        path (str): path to dbin (and log) if being created from memory.
    '''


    def __init__(self, nq=100, n_angle=180, qmax=1, grid_type='GLQ', extend=False,  path=None, comp=False):
        assert n_angle%2==0, 'n_angle must be even'

        if grid_type=='DH1':
            if extend:
                N_lat = n_angle +1
                N_long = n_angle +1
                self.lmax = int(n_angle/2) -1
            else:
                N_lat = n_angle
                N_long = n_angle
                self.lmax = int(n_angle/2) -1


        elif grid_type=='DH2':
            if extend:
                N_lat = n_angle +1
                N_long = 2*n_angle +1
                self.lmax = int(n_angle/2) -1
            else:
                N_lat = n_angle
                N_long = 2*n_angle
                self.lmax = int(n_angle/2) -1

        else:
            if extend:
                N_lat = n_angle
                N_long = 2*n_angle 
                self.lmax = int(n_angle) -1
            else:
                N_lat = n_angle
                N_long = 2*n_angle -1
                self.lmax = int(n_angle) -1

        Vol.__init__(self, nq,N_lat, N_long, qmax, 180, 360, comp, path=path)






