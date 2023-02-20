






class PeakDataProperties:

    @property
    def geom(self):
        '''
        ExpoGeom object that handles experiment geometry.
        '''
        return self._geom

    @property
    def path(self):
        '''
        path to data
        '''
        return self._path



  
    @property
    def df(self):
        '''
        data frame containing frame numbers, fs and ss pixel indices and scattering intensity 
        '''
        return self._df



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




