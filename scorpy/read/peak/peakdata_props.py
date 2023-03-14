


import numpy as np




class PeakDataProperties:

    @property
    def geompath(self):
        '''
        path to geom
        '''
        return self._geompath

    @property
    def datapath(self):
        '''
        path to data
        '''
        return self._datapath

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


    # @property
    # def qmax(self):
        # '''
        # maximum scattering vector [A-1]
        # '''
        # return self._qmax





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


    @property
    def scat_rect(self):
        '''
        scattering rect
        '''
        return self._scat_rect

    @property
    def scat_rpol(self):
        '''
        scattering rpol
        '''
        return self._scat_rpol


    @property
    def scat_tpol(self):
        '''
        scattering tpol
        '''
        return self._scat_tpol

    @property
    def scat_qpol(self):
        '''
        scattering qpol
        '''
        return self._scat_qpol

    @property
    def scat_sph(self):
        '''
        scattering sph
        '''
        return self._scat_sph



