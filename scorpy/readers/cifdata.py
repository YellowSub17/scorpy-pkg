
import CifFile as pycif
import numpy as np
from ..symmetry import apply_sym
from ..utils import index_x


class CifData:

    def __init__(self,fname, qmax=None):

        cif = pycif.ReadCif(fname)
        vk = cif.visible_keys[0]


        self._cif = dict(cif[vk])
        self._spg = self.cif['_symmetry.space_group_name_h-m']


        self._alpha = np.radians(float(self.cif['_cell.angle_alpha']))
        self._beta = np.radians(float(self.cif['_cell.angle_beta']))
        self._gamma = np.radians(float(self.cif['_cell.angle_gamma']))



        a_unit = np.array([1.0,0.0,0.0])
        b_unit = np.array([np.cos(self.gamma), np.sin(self.gamma), 0])
        c_unit = np.array([
                            np.cos(self.beta),
                           (np.cos(self.alpha) - np.cos(self.beta)*np.cos(self.gamma))/np.sin(self.gamma),
                            np.sqrt( 1 - np.cos(self.beta)**2 - (( np.cos(self.alpha) -np.cos(self.beta)*np.cos(self.gamma))/np.sin(self.gamma))**2)
                        ])

        self._a = float(self.cif['_cell.length_a'])*np.round(a_unit,14)
        self._b = float(self.cif['_cell.length_b'])*np.round(b_unit,14)
        self._c = float(self.cif['_cell.length_c'])*np.round(c_unit,14)


        cell_volume = np.dot(self.a,np.cross(self.b,self.c))

        self._ast = 2*np.pi*np.cross(self.b,self.c) /cell_volume
        self._bst = 2*np.pi*np.cross(self.c,self.a) /cell_volume
        self._cst = 2*np.pi*np.cross(self.a,self.b) /cell_volume


        self._scat_bragg, self._scat_rect, self._scat_sph = self.get_refl(qmax)



        if qmax is None:
            self._qmax = np.max(self._scat_sph[:,0])
        else:
            self._qmax = qmax



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








    def get_refl(self, qmax):
        '''
        Parse cif data to generate scattering infomation, in Bragg indices,
        rectilinear reciprocal units, and spherical reciprocal units


        Arguments:
            qmax: maximum reciprocal unit distance to retreive [1/A].

        Returns:
            bragg: list of bragg indices and intensity.
            scattering: list of scattering postions in reciprocal units [1/A].
            spherical: list of scattering positions in spherical units.
        '''

        # Read h,k,l indices
        h = np.array(self.cif['_refln.index_h']).astype(np.int32)
        k = np.array(self.cif['_refln.index_k']).astype(np.int32)
        l = np.array(self.cif['_refln.index_l']).astype(np.int32)

        # Read intensities
        if '_refln.intensity_meas' in self.cif.keys():
            I = np.array(self.cif['_refln.intensity_meas'])
            I = np.where(I == '?', '0', I)
            I = I.astype(np.float64)
        elif '_refln.f_meas_au' in self.cif.keys():
            I = np.array(self.cif['_refln.f_meas_au'])
            I = np.where(I == '?', '0', I)
            I = I.astype(np.float64)**2 
        elif '_refln.f_squared_meas' in self.cif.keys():
            I = np.array(self.cif['_refln.f_squared_meas'])
            I = np.where(I == '?', '0', I)
            I = I.astype(np.float64)
        else:
            print('WARNING: No intensity found when reading cif.')
            return None

        #apply symmetry to generate all bragg points
        asym_refl = np.array([h, k, l, I]).T
        bragg = apply_sym(asym_refl, self.spg)

        # convert bragg indices to rect reciprocal units 
        scattering_pos = np.matmul(bragg[:,:-1], np.array([self.ast, self.bst, self.cst]))
        scattering = np.zeros(bragg.shape)
        scattering[:, :-1] = scattering_pos
        scattering[:, -1] = bragg[:, -1]


        # convert rect reciprocal units to spherical coords
        q_mag = np.linalg.norm(scattering[:,:3], axis=1)
        #up and down
        theta = np.arctan2(np.linalg.norm(scattering[:,:2], axis=1),scattering[:,2]) #0 -> pi
        theta -= np.pi/2 # -pi/2 -> pi/2

        #around
        phi = np.arctan2(scattering[:,1], scattering[:,0]) # -pi -> pi
        phi[np.where(phi<0)] = phi[np.where(phi<0)] + 2*np.pi  #0 -> 2pi
        spherical  = np.array([q_mag, theta, phi, bragg[:,-1]]).T

        if not qmax is None:
            loc = np.where(spherical[:,0] <= qmax)
            scattering = scattering[loc]
            bragg = bragg[loc]
            spherical = spherical[loc]

        return bragg, scattering, spherical




    def bin_sph(self, nq, ntheta, nphi):


        qs = self.spherical[:,0]
        ts = self.spherical[:,1]+np.pi/2 #0 -> pi
        ps = self.spherical[:,2]

        ite = np.ones(np.shape(qs))

        qinds = list(map(index_x, qs, self.qmax*ite, nq*ite))
        tinds = list(map(index_x, ts*ite, np.pi*ite, ntheta*ite))
        pinds = list(map(index_x, ps*ite, 2*np.pi*ite, nphi*ite))



        print(qinds)

        qspace = np.linspace(0, self.qmax, nq)
        tspace = np.linspace(-np.pi/2, np.pi/2, ntheta)
        pspace = np.linspace(0, 2*np.pi, nphi)





        self.spherical[:,0] = qspace[qinds]
        self.spherical[:,1] = tspace[tinds]
        self.spherical[:,2] = pspace[pinds]

















