

class BlqqVolProps:

    @property
    def nq(self):
        '''
    scorpy.BlqqVol.nx:
            Number of voxels in q-axis directions.
        '''
        return self.nx

    @property
    def nl(self):
        '''
    scorpy.BlqqVol.dq:
            Number of spherical harmonics.
        '''
        return self.nz

    @property
    def qmax(self):
        '''
    scorpy.BlqqVol.qmax:
            Maximum value of q-axes.
        '''
        return self.xmax

    @property
    def qmin(self):
        '''
    scorpy.BlqqVol.qmax:
            Minimum value of q-axes.
        '''
        return self.xmin



    @property
    def dq(self):
        '''
    scorpy.BlqqVol.dq:
            Size of a voxel in q-axis
        '''
        return self.dx

    @property
    def qpts(self):
        '''
    scorpy.CorrelationVol.qpts:
            Array of sample points on the q-axis.
        '''
        return self.xpts

    @property
    def inc_odds(self):
        return self._inc_odds


