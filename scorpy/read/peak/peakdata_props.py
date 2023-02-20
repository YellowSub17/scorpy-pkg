






class PeakDataProperties:

    @property
    def geompath(self):
        '''
        path to geom
        '''
        return self._geompath

    @property
    def h5path(self):
        '''
        path to data
        '''
        return self._h5path


    @property
    def geom_params(self):
        '''
        parameters defined in geom
        '''
        return self._geom_params

    @property
    def res(self):
        '''
        resolution = 1/pix size [1/m]
        '''
        return float(self.geom_params['res'])

    @property
    def clen(self):
        '''
        camera length
        '''
        return float(self.geom_params['clen'])  # camera length


    @property
    def photon_energy(self):
        '''
        photon engery [eV]
        '''
        return float(self.geom_params['photon_energy'])  # eV




    @property
    def wavelength(self):
        '''
        wavelength [A]
        '''
        return (4.135667e-15 * 2.99792e8 *1e10) / self.photon_energy  # A


    @property
    def k(self):
        '''
        wavenumber
        '''
        return (2 * np.pi) / self.wavelength # 1/A



    @property
    def panels(self):
        '''
        list of panels
        '''
        return self.geom_params['panels']











        # self.res = float(self.geom_params['res'])
        # self.clen = 
        # self.photon_energy = 

        # #props
        # self.wavelength = 
        # self.k = 




