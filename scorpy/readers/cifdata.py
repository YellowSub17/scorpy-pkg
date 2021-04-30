
import CifFile as pycif
import numpy as np
from ..symmetry import apply_sym
from ..utils import index_x

from .propertymixins import CifDataProperties


class CifData(CifDataProperties):

    def __init__(self,fname, qmax=None, ):

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


        #TODO: Work out if we need an extra 2*pi factor on reciprocal units
        self._ast = np.cross(self.b,self.c) /cell_volume
        self._bst = np.cross(self.c,self.a) /cell_volume
        self._cst = np.cross(self.a,self.b) /cell_volume


        self._scat_bragg, self._scat_rect, self._scat_sph = self.get_scat(qmax)



        if qmax is None:
            self._qmax = np.max(self._scat_sph[:,0])
        else:
            self._qmax = qmax







    def get_scat(self, qmax):
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

        #cropp any negative intensity
        loc = np.where(asym_refl[:,-1] >= 0)
        asym_refl = asym_refl[loc]

    


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










    # def bin_sph(self, nq, ntheta, nphi):

        # qs = self.spherical[:,0]
        # ts = self.spherical[:,1]+np.pi/2 #0 -> pi
        # ps = self.spherical[:,2]

        # ite = np.ones(np.shape(qs))

        # qinds = list(map(index_x, qs, self.qmax*ite, nq*ite))
        # tinds = list(map(index_x, ts*ite, np.pi*ite, ntheta*ite))
        # pinds = list(map(index_x, ps*ite, 2*np.pi*ite, nphi*ite))



        # print(qinds)

        # qspace = np.linspace(0, self.qmax, nq)
        # tspace = np.linspace(-np.pi/2, np.pi/2, ntheta)
        # pspace = np.linspace(0, 2*np.pi, nphi)





        # self.spherical[:,0] = qspace[qinds]
        # self.spherical[:,1] = tspace[tinds]
        # self.spherical[:,2] = pspace[pinds]

















