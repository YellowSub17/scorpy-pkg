import numpy as np


class SphericalVolProps:

    @property
    def nq(self):
        '''
	scorpy.SphericalVol.nq:
            Number of voxels in q-axis directions.
        '''
        return self.nx

    @property
    def ntheta(self):
        '''
	scorpy.SphericalVol.ntheta:
            Number of voxels in theta-axis direction.
        '''
        return self.ny

    @property
    def nphi(self):
        '''
	scorpy.SphericalVol.nphi:
            Number of voxels in phi-axis direction.
        '''
        return self.nz

    @property
    def qmax(self):
        '''
	scorpy.SphericalVol.qmax:
            Maximum value of q-axes.
        '''
        return self.xmax

    @property
    def dq(self):
        '''
	scorpy.SphericalVol.dq:
            Size of a voxel in q-axis
        '''
        return self.dx

    @property
    def dtheta(self):
        '''
	scorpy.SphericalVol.dtheta:
            Size of a voxel in theta-axis
        '''
        return self.dy

    @property
    def dphi(self):
        '''
	scorpy.SphericalVol.dphi:
            Size of a voxel in phi-axis
        '''
        return self.dz

    @property
    def nl(self):
        '''
	scorpy.SphericalVol.nl:
            Number of spherical harmonics to satisfy sampling.
        '''
        return int(self._nl)

    @property
    def qpts(self):
        '''
	scorpy.SphericalVol.qpts:
            Array of sample points on the q-axis.
        '''
        return self.xpts

    @property
    def thetapts(self):
        '''
	scorpy.SphericalVol.thetapts:
            Array of sample points on the theta-axis.
        '''
        return self.ypts

    @property
    def phipts(self):
        '''
	scorpy.SphericalVol.phipts:
            Array of sample points on the phi-axis.
        '''
        return self.zpts

