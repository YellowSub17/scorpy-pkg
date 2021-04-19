
import CifFile as pycif
import numpy as np
from ..symmetry import apply_sym


class CifData:

    def __init__(self,fname, qmax=None):

        self.fname = fname
        cif = pycif.ReadCif(self.fname)

        vk = cif.visible_keys[0]
        self.cif = dict(cif[vk])
        self.spg = self.cif['_symmetry.space_group_name_h-m']

        # self.dcell_angles = self.get_dcell_angles()
        # self.dcell_vectors = self.get_dcell_vectors()
        # self.qcell_vectors = self.get_qcell_vectors()
        # self.bragg, self.scattering, self.spherical = self.get_refl()



        self.alpha = np.radians(float(self.cif['_cell.angle_alpha']))
        self.beta = np.radians(float(self.cif['_cell.angle_beta']))
        self.gamma = np.radians(float(self.cif['_cell.angle_gamma']))



        a_unit = np.array([1.0,0.0,0.0])
        b_unit = np.array([np.cos(self.gamma), np.sin(self.gamma), 0])
        c_unit = np.array([
                            np.cos(self.beta),
                           (np.cos(self.alpha) - np.cos(self.beta)*np.cos(self.gamma))/np.sin(self.gamma),
                            np.sqrt( 1 - np.cos(self.beta)**2 - (( np.cos(self.alpha) -np.cos(self.beta)*np.cos(self.gamma))/np.sin(self.gamma))**2)
                        ])

        self.a = float(self.cif['_cell.length_a'])*a_unit
        self.b = float(self.cif['_cell.length_b'])*b_unit
        self.c = float(self.cif['_cell.length_c'])*c_unit


        self.ast = np.cross(self.b,self.c) /np.dot(self.a,np.cross(self.b,self.c))
        self.bst = np.cross(self.a,self.c) /np.dot(self.a,np.cross(self.b,self.c))
        self.cst = np.cross(self.a,self.b) /np.dot(self.a,np.cross(self.b,self.c))


        self.bragg, self.scattering, self.spherical = self.get_refl()

        # self.bragg_scattering, self.scattering, self.spherical = self.get_refl()


        if qmax is None:
            self.qmax = np.max(self.spherical[:,0])
        else:
            self.qmax = qmax
            loc = np.where(self.spherical[:,0]<self.qmax)
            self.scattering = self.scattering[loc]
            self.bragg = self.bragg[loc]
            self.spherical = self.spherical[loc]









    def get_refl(self):
        '''
        Parse cif data for scattering infomation

        Arguments:
            None.

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

        asym_refl = np.array([h, k, l, I]).T
        bragg = apply_sym(asym_refl, self.spg)

        scattering_pos = np.matmul(bragg[:,:-1], np.array([self.ast, self.bst, self.cst]))

        scattering = np.zeros(bragg.shape)
        scattering[:, :-1] = scattering_pos
        scattering[:, -1] = bragg[:, -1]


        q_mag = np.linalg.norm(scattering[:,:3], axis=1)
        phi = np.arctan2(scattering[:,1], scattering[:,0]) # -pi -> pi
        phi[np.where(phi<0)] = phi[np.where(phi<0)] + 2*np.pi  #0 -> 2pi
        theta = np.arctan2(np.linalg.norm(scattering[:,:2], axis=1),scattering[:,2]) #0 -> pi

        spherical  =np.array([q_mag, theta, phi, bragg[:,-1]]).T


        return bragg, scattering, spherical




        




