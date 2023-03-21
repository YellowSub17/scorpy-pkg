


class CorrelationVolProps:

    @property
    def nq(self):
        '''
	scorpy.CorrelationVol.nx:
            Number of voxels in q-axis directions.
        '''
        return self.nx

    @property
    def npsi(self):
        '''
	scorpy.CorrelationVol.npsi:
            Number of voxels in psi-axis direction.
        '''
        return self.nz

    @property
    def qmax(self):
        '''
	scorpy.CorrelationVol.qmax:
            Maximum value of q-axes.
        '''
        return self.xmax

    @property
    def qmin(self):
        '''
	scorpy.CorrelationVol.qmin:
            Minimum value of q-axes.
        '''
        return self.xmin

    @property
    def dq(self):
        '''
	scorpy.CorrelationVol.dq:
            Size of a voxel in q-axis
        '''
        return self.dx

    @property
    def dpsi(self):
        '''
	scorpy.CorrelationVol.dpsi:
            Size of a voxel in psi-axis
        '''
        return self.dz

    @property
    def qpts(self):
        '''
	scorpy.CorrelationVol.qpts:
            Array of sample points on the q-axis.
        '''
        return self.xpts

    @property
    def psipts(self):
        '''
	scorpy.CorrelationVol.psipts:
            Array of sample points on the psi-axis.
        '''
        return self.zpts

    @property
    def cos_sample(self):
        return self._cos_sample

    @property
    def inc_self_corr(self):
        return self._inc_self_corr



