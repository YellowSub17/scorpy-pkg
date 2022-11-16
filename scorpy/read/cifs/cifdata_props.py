
class CifDataProperties:

    @property
    def a(self):
        '''
        Direct lattice vector a
        '''
        return self._a

    @property
    def b(self):
        '''
        Direct lattice vector b
        '''
        return self._b

    @property
    def c(self):
        '''
        Direct lattice vector c
        '''
        return self._c
    
    @property
    def a_mag(self):
        return self._a_mag

    @property
    def b_mag(self):
        return self._b_mag

    @property
    def c_mag(self):
        return self._c_mag

    @property
    def ast_mag(self):
        return self._ast_mag

    @property
    def bst_mag(self):
        return self._bst_mag

    @property
    def cst_mag(self):
        return self._cst_mag

    @property
    def alpha(self):
        '''
        Angle between direct lattice vectors b and c
        '''
        return self._alpha

    @property
    def beta(self):
        '''
        Angle between direct lattice vectors a and c
        '''
        return self._beta

    @property
    def gamma(self):
        '''
        Angle between direct lattice vectors a and b
        '''
        return self._gamma

    @property
    def ast(self):
        '''
        Reciprocal lattice vector a*
        '''
        return self._ast

    @property
    def bst(self):
        '''
        Reciprocal lattice vector b*
        '''
        return self._bst

    @property
    def cst(self):
        '''
        Reciprocal lattice vector c*
        '''
        return self._cst

    @property
    def cif(self):
        '''
        Dictionary representation of the cif file
        '''
        return self._cif

    @property
    def spg(self):
        '''
        Space group of the crystal.
        '''
        return self._spg

    @property
    def scat_bragg(self):
        '''
        Array of Bragg scattering data.
        Columns are h,k,l and diffraction intensity.
        '''
        return self._scat_bragg

    @property
    def scat_rect(self):
        '''
        Array of rectilinear scattering data.
        Columns are qx, qy, qz and diffraction intensity.
        '''
        return self._scat_rect

    @property
    def scat_sph(self):
        '''
        Array of spherical scattering data.
        Columns are q magnitude, theta, phi and diffraction intensity.
        theta ranges from [-pi/2, pi/2], and is the polar angle.
        phi ranges from [0, 2pi] and is the azimuthal angle.
        '''
        return self._scat_sph



    @property
    def qmax(self):
        '''
        Maximum reciprocal distance in the scattering data.
        Determines resolution of reconstructions.
        '''
        return self._qmax


    # @property
    # def max_bragg_ast(self):
        # return self._max_bragg_ast

    # @property
    # def max_bragg_bst(self):
        # return self._max_bragg_bst

    # @property
    # def max_bragg_cst(self):
        # return self._max_bragg_cst


