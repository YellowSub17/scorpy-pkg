
import CifFile as pycif
import numpy as np
from ...utils.utils import index_x, convert_rect2sph
from ...utils.symmetry import apply_sym
import itertools

from .cifdata_props import CifDataProperties
from .cifdata_saveload import CifDataSaveLoad






class CifData(CifDataProperties, CifDataSaveLoad):

    def __init__(self,path, qmax=None, fill_peaks=False, rotk=None, rottheta=None, skip_sym=False ):




        starcif = pycif.ReadCif(path)
        vk = starcif.visible_keys[0]
        cif_dict = dict(starcif[vk])


        self._get_cell_params(cif_dict)
        self._get_cell_vecs(rotk = rotk, rottheta = rottheta)



        if '_refln.index_h' in cif_dict.keys():
            self._calc_scat(cif_dict, qmax=qmax, fill_peaks=fill_peaks, skip_sym=skip_sym)

        else:
            self._scat_bragg= None
            self._scat_rect = None
            self._scat_sph = None





# def rfactor(self, cif_targ, sqrt=False):
        # assert np.all(cif_targ.scat_bragg[:,:3] == self.scat_bragg[:,:3]), 'Cannot calcuate Rfactor, bragg indices are different'

        # Fo = cif_targ.scat_bragg[:,-1]
        # Fc = self.scat_bragg[:,-1]


        # if sqrt:
            # Fo = np.sqrt(Fo)
            # Fc = np.sqrt(Fc)

        # Fo /= np.sum(Fo)
        # Fc /= np.sum(Fc)



        # R = np.sum( np.abs( np.abs(Fo) - np.abs(Fc)))/np.sum(np.abs(Fo))
        # return R






    def _get_cell_params(self, cif_dict):

        if '_cell_angle_alpha' in cif_dict.keys():
            sf = '_'
        else:
            sf = '.'

        self._alpha = np.radians(float(cif_dict[f'_cell{sf}angle_alpha'].split('(')[0]))
        self._beta = np.radians(float(cif_dict[f'_cell{sf}angle_beta'].split('(')[0]))
        self._gamma = np.radians(float(cif_dict[f'_cell{sf}angle_gamma'].split('(')[0]))

        self._a_mag = float(cif_dict[f'_cell{sf}length_a'].split('(')[0])
        self._b_mag = float(cif_dict[f'_cell{sf}length_b'].split('(')[0])
        self._c_mag = float(cif_dict[f'_cell{sf}length_c'].split('(')[0])

        for key in ['_symmetry.space_group_name_h-m', '_space_group_name_h-m_alt', '_symmetry_space_group_name_h-m']:
            if key in cif_dict.keys():
                self._spg = cif_dict[key].upper()




    def _get_cell_vecs(self, rotk=None, rottheta=0):
        '''
        Calculate vectors for direct and reciprocal crystal lattices
        '''
        a_unit = np.array([1.0, 0.0, 0.0])
        b_unit = np.array([np.cos(self.gamma), np.sin(self.gamma), 0])
        c_unit = np.array([
            np.cos(self.beta),
            (np.cos(self.alpha) - np.cos(self.beta) * np.cos(self.gamma)) / np.sin(self.gamma),
            np.sqrt(1 - np.cos(self.beta)**2 - ( (np.cos(self.alpha) - np.cos(self.beta) * np.cos(self.gamma)) / np.sin(self.gamma))**2)
        ])
        # # another expressions for cz
        # np.sqrt(1 - np.cos(self.alpha)**2 - np.cos(self.beta)**2 - np.cos(self.gamma)**2 + 2*np.cos(self.alpha)*np.cos(self.beta)*np.cos(self.gamma))/np.sin(self.gamma)

        #Rodriguiz formula
        if rotk is not None:
            rotk = rotk/np.linalg.norm(rotk)
            a_unit =  np.cos(rottheta)*a_unit + (1-np.cos(rottheta))*np.dot(a_unit, rotk)*rotk + np.sin(rottheta)*(np.cross(rotk, a_unit))
            b_unit =  np.cos(rottheta)*b_unit + (1-np.cos(rottheta))*np.dot(b_unit, rotk)*rotk + np.sin(rottheta)*(np.cross(rotk, b_unit))
            c_unit =  np.cos(rottheta)*c_unit + (1-np.cos(rottheta))*np.dot(c_unit, rotk)*rotk + np.sin(rottheta)*(np.cross(rotk, c_unit))

        self._a = self.a_mag * np.round(a_unit, 14)
        self._b = self.b_mag * np.round(b_unit, 14)
        self._c = self.c_mag * np.round(c_unit, 14)


        cell_volume = np.dot(self.a, np.cross(self.b, self.c))

        self._ast = 2 * np.pi * np.cross(self.b, self.c) / cell_volume
        self._bst = 2 * np.pi * np.cross(self.c, self.a) / cell_volume
        self._cst = 2 * np.pi * np.cross(self.a, self.b) / cell_volume

        self._ast_mag = np.linalg.norm(self._ast)
        self._bst_mag = np.linalg.norm(self._bst)
        self._cst_mag = np.linalg.norm(self._cst)











    def _calc_scat(self, cif_dict, qmax=None, fill_peaks=False, skip_sym=False):
        '''
        Parse cif data to generate scattering infomation, in Bragg indices,
        rectilinear reciprocal units, and spherical reciprocal units
        '''

        ##### Bragg Indices
        h = np.array(cif_dict['_refln.index_h']).astype(np.float).astype(np.int32)
        k = np.array(cif_dict['_refln.index_k']).astype(np.float).astype(np.int32)
        l = np.array(cif_dict['_refln.index_l']).astype(np.float).astype(np.int32)


        inten_keys = ['_refln.intensity_meas' ,'_refln.f_squared_meas','_refln.f_meas_au' ]

        I=None
        for inten_key, inten_pw in zip(inten_keys, [1,1,2]):
            if inten_key in cif_dict.keys():
                I = np.array(cif_dict[inten_key])
                I = I.astype(np.float64)**inten_pw
        assert I is not None, 'WARNING: No intensity found when reading cif.'


        # apply symmetry to generate all bragg points
        asym_refl = np.array([h, k, l, I]).T
        # loc = np.where(asym_refl[:, -1] >= 0)
        # asym_refl = asym_refl[loc]

        if skip_sym:
            sym_refl = asym_refl
        else:
            sym_refl = apply_sym(asym_refl, self.spg)


        if fill_peaks:
            # Fill missing bragg indices 
            h_max = np.max(np.abs(sym_refl[:,0]))
            k_max = np.max(np.abs(sym_refl[:,1]))
            l_max = np.max(np.abs(sym_refl[:,2]))

            ast_ite = np.arange(-h_max, h_max+1)
            bst_ite = np.arange(-k_max, k_max+1)
            cst_ite = np.arange(-l_max, l_max+1)

            all_bragg_xyz = np.array(list(itertools.product( ast_ite, bst_ite, cst_ite)))
            loc_000 = np.all(all_bragg_xyz == 0, axis=1)  # remove 000 reflection
            all_bragg_xyz = all_bragg_xyz[~loc_000]


            self._scat_bragg = np.zeros( (all_bragg_xyz.shape[0], 4))
            for i, bragg_pt in enumerate(all_bragg_xyz):
                self._scat_bragg[i,:-1] = bragg_pt
                loc = np.where( (sym_refl[:,:-1]==bragg_pt).all(axis=1))[0]
                if len(loc)==1:
                    self._scat_bragg[i,-1] = sym_refl[loc,-1]


        else:
            self._scat_bragg = sym_refl









        ##### Reciprocal Space Units
        self._scat_rect = np.zeros(self.scat_bragg.shape)
        self._scat_rect[:, :-1] = np.matmul(self.scat_bragg[:, :-1], np.array([self.ast, self.bst, self.cst]))
        self._scat_rect[:, -1] = self.scat_bragg[:,-1]


        ##### Spherical Coordinates
        self._scat_sph = np.zeros(self.scat_rect.shape)
        self._scat_sph[:, :-1] = convert_rect2sph(self.scat_rect[:,:3])
        self._scat_sph[:, -1] = self.scat_bragg[:,-1]


        inten_loc = np.where(self._scat_sph[:,-1]>0)[0]
        inten_qmax = self._scat_sph[inten_loc,0].max()



        if qmax is not None:
            qmax = min(qmax, inten_qmax)
        else:
            qmax = inten_qmax


        loc = np.where(self.scat_sph[:, 0] <= qmax)
        self._scat_rect = self._scat_rect[loc]
        self._scat_bragg = self._scat_bragg[loc]
        self._scat_sph = self._scat_sph[loc]


        self._qmax = np.round(np.max(self.scat_sph[:,0]), 14)

        self._scat_bragg = np.round(self.scat_bragg, 14)
        self._scat_sph = np.round(self.scat_sph, 14)
        self._scat_rect = np.round(self.scat_rect, 14)







    def fill_from_vhkl(self, path, qmax=None, skip_sym=False, fill_peaks=False):

        hklI = np.genfromtxt(path, skip_header=1, usecols=(0,1,2,6))

        hklI[:, -1] = hklI[:,-1]**2

        cif_dict = {}
        cif_dict['_refln.index_h'] =  hklI[:,0]
        cif_dict['_refln.index_k'] =  hklI[:,1]
        cif_dict['_refln.index_l'] =  hklI[:,2]
        cif_dict['_refln.intensity_meas'] = hklI[:,-1]

        self._calc_scat(cif_dict, qmax=qmax, skip_sym=skip_sym, fill_peaks=fill_peaks)







    def fill_from_sphv(self, sphv):

        ast_max_bragg_ind = int(sphv.qmax/self.ast_mag)+1
        bst_max_bragg_ind = int(sphv.qmax/self.bst_mag)+1
        cst_max_bragg_ind = int(sphv.qmax/self.cst_mag)+1

        ast_ite = np.arange(-ast_max_bragg_ind, ast_max_bragg_ind+1)
        bst_ite = np.arange(-bst_max_bragg_ind, bst_max_bragg_ind+1)
        cst_ite = np.arange(-cst_max_bragg_ind, cst_max_bragg_ind+1)

        bragg_xyz = np.array(list(itertools.product( ast_ite, bst_ite, cst_ite)))
        loc_000 = np.all(bragg_xyz == 0, axis=1)  # remove 000 reflection
        bragg_xyz = bragg_xyz[~loc_000]


        rect_xyz = np.matmul(
            bragg_xyz, np.array([self.ast, self.bst, self.cst]))

        sph_qtp = convert_rect2sph(rect_xyz)


        qloc = np.where(sph_qtp[:,0] <= sphv.qmax)

        bragg_xyz = bragg_xyz[qloc]
        rect_xyz = rect_xyz[qloc]
        sph_qtp = sph_qtp[qloc]

        ite = np.ones( sph_qtp.shape[0])
        q_inds = list(map(index_x, sph_qtp[:, 0], 0 * ite, sphv.qmax * ite, sphv.nq * ite))
        theta_inds = list(map(index_x, sph_qtp[:, 1], sphv.ymin * ite, sphv.ymax * ite, sphv.ny * ite))
        phi_inds = list(map(index_x, sph_qtp[:, 2], sphv.zmin * ite, sphv.zmax * ite, sphv.nz * ite, ite))


        I = np.zeros(sph_qtp.shape[0])
        for i, (q_ind, theta_ind, phi_ind ) in enumerate(zip(q_inds, theta_inds, phi_inds )):
            I[i] += sphv.vol[q_ind, theta_ind, phi_ind]


        cif_dict = {}
        cif_dict['_refln.index_h'] =  bragg_xyz[:,0]
        cif_dict['_refln.index_k'] =  bragg_xyz[:,1]
        cif_dict['_refln.index_l'] =  bragg_xyz[:,2]
        cif_dict['_refln.intensity_meas'] = I

        self._calc_scat(cif_dict, qmax=sphv.qmax, skip_sym=True, fill_peaks=False)

    def save_hkl(self, path):


        f = open(path, 'w')

        for bragg_pt in self.scat_bragg:

            line = '%4d%4d%4d%8.2f%8.2f\n' % (bragg_pt[0], bragg_pt[1], bragg_pt[2], bragg_pt[3], 0)

            f.write(line)
        f.write('   0   0   0       0       0       0       0')
        f.close()










