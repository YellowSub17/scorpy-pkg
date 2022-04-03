






class PeakDataProperties:

    @property
    def geom(self):
        '''
        ExpoGeom object that handles experiment geometry.
        '''
        return self._geom

    @property
    def cxi_flag(self):
        '''
        Boolean flag for if data came from XFEL dataset (True) or simulated ensemble (False)
        '''
        return self._cxi_flag

    @property
    def df(self):
        '''
        data frame containing frame numbers, fs and ss pixel indices and scattering intensity 
        '''
        return self._df

    @property
    def frame_numbers(self):
        '''
        Set of unique frame numbers for peaklist
        '''
        return self._frame_numbers

    @property
    def scat_pol(self):
        '''
        scattering in polar coordinates
        '''
        return self._scat_pol

    @property
    def scat_rect(self):
        '''
        scatting in 3D carteasian coordinates
        '''
        return self._scat_rect

    @property
    def scat_sph(self):
        '''
        scatting in 3D spherical coordinates
        '''
        return self._scat_sph

    @property
    def qmax(self):
        return self._qmax

    @property
    def qmin(self):
        return self._qmin

    @property
    def mask_flag(self):
        return self._mask_flag




