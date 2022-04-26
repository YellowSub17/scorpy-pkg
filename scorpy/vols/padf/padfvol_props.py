import numpy as np

class PadfVolProps:

    @property
    def nr(self):
        '''
	scorpy.PadfVol.nr:
            Number of voxels in r-axis directions.
        '''
        return self.nx

    @property
    def npsi(self):
        '''
	scorpy.PadfVol.nr:
            Number of voxels in psi-axis direction.
        '''
        return self.nz

    @property
    def rmax(self):
        '''
	scorpy.PadfVol.rmax:
            Maximum value of r-axes.
        '''
        return self.xmax

    @property
    def dr(self):
        '''
	scorpy.PadfVol.dr:
            Size of a voxel in r-axis
        '''
        return self.dx

    @property
    def dpsi(self):
        '''
	scorpy.PadfVol.dpsi:
            Size of a voxel in psi-axis
        '''
        return self.dz

    @property
    def nl(self):
        '''
	scorpy.PadfVol.nl:
            Number of spherical harmonics in calculation.
        '''
        return self._nl


    @property
    def rpts(self):
        '''
	scorpy.PadfVol.rpts:
            Array of sample points on the r-axis.
        '''
        return self.xpts

    @property
    def psipts(self):
        '''
	scorpy.PadfVol.psipts:
            Array of sample points on the psi-axis.
        '''
        return self.zpts

    @property
    def wavelength(self):
        '''
        scorpy.PadfVol.wavelength:
            wavelength of experiment, used in PADF calculation.
        '''
        return self._wavelength


