
import CifFile as pycif
import numpy as np
from ...utils.convert_funcs import index_x_wrap, index_x_nowrap, convert_rect2sph
from ...utils.sym_funcs import apply_sym, fill_missing
import itertools

from .cifdata_props import CifDataProperties
from .cifdata_saveload import CifDataSaveLoad
from .cifdata_fill import CifDataFill






class CifData(CifDataProperties, CifDataSaveLoad, CifDataFill):

    def __init__(self,path, qmax=None, rotk=[1,0,0], rottheta=0, spg=None,fill_peaks=False):


        starcif = pycif.ReadCif(f'{path}')
        vk = starcif.visible_keys[0]

        cif_dict = dict(starcif[vk])
        sep = '_' if '_cell_angle_alpha' in cif_dict.keys() else '.'

        if spg is None:
            spg_keys = {f'_symmetry{sep}space_group_name_h-m', '_space_group_name_h-m_alt'}
            spg_key = list(spg_keys.intersection(cif_dict.keys()))[0]
            self._spg = cif_dict[spg_key].upper()
        else:
            self._spg = spg.upper()




        ### get cell angles
        self._alpha = np.radians(float(cif_dict[f'_cell{sep}angle_alpha'].split('(')[0]))
        self._beta = np.radians(float(cif_dict[f'_cell{sep}angle_beta'].split('(')[0]))
        self._gamma = np.radians(float(cif_dict[f'_cell{sep}angle_gamma'].split('(')[0]))

        ### get cell sides
        self._a_mag = float(cif_dict[f'_cell{sep}length_a'].split('(')[0])
        self._b_mag = float(cif_dict[f'_cell{sep}length_b'].split('(')[0])
        self._c_mag = float(cif_dict[f'_cell{sep}length_c'].split('(')[0])



        ### calculate lattice vectors
        a_unit = np.array([1.0, 0.0, 0.0])
        b_unit = np.array([np.cos(self.gamma), np.sin(self.gamma), 0])
        c_unit = np.array([
            np.cos(self.beta),
            (np.cos(self.alpha) - np.cos(self.beta) * np.cos(self.gamma)) / np.sin(self.gamma),
            np.sqrt(1 - np.cos(self.beta)**2 - ( (np.cos(self.alpha) - np.cos(self.beta) * np.cos(self.gamma)) / np.sin(self.gamma))**2)
        ])


        units = [a_unit, b_unit, c_unit]
        mags = [self.a_mag, self.b_mag, self.c_mag]


        rotk = rotk/np.linalg.norm(rotk)
        c = np.cos(rottheta)
        s = np.sin(rottheta)


        abc = np.zeros((3,3))
        for i, (unit, mag) in enumerate(zip(units, mags)):
            #rodriguiz formula
            rot_unit =  c*unit + (1-c)*np.dot(unit, rotk)*rotk + s*(np.cross(rotk, unit))

            abc[i] = rot_unit*mag

        abc = np.round(abc, 14)

        self._a, self._b, self._c = abc

        ### calculate reciprocal lattice vectors

        cell_volume = np.dot(self.a, np.cross(self.b, self.c))

        self._ast = 2 * np.pi * np.cross(self.b, self.c) / cell_volume
        self._bst = 2 * np.pi * np.cross(self.c, self.a) / cell_volume
        self._cst = 2 * np.pi * np.cross(self.a, self.b) / cell_volume

        ### calculate reciprocal lattice vector magnitudes

        self._ast_mag = np.linalg.norm(self._ast)
        self._bst_mag = np.linalg.norm(self._bst)
        self._cst_mag = np.linalg.norm(self._cst)




        ### get bragg indices


        h = np.array(cif_dict[f'_refln{sep}index_h']).astype(float).astype(np.int32)
        k = np.array(cif_dict[f'_refln{sep}index_k']).astype(float).astype(np.int32)
        l = np.array(cif_dict[f'_refln{sep}index_l']).astype(float).astype(np.int32)



        inten_pow_dict = {f'_refln{sep}intensity_meas':1,
                          f'_refln{sep}f_squared_meas':1,
                          f'_refln{sep}f_meas_au':2}


        inten_key = list(set(inten_pow_dict.keys()).intersection(cif_dict.keys()))[0]


        I = np.array(cif_dict[inten_key])
        I = I.astype(float)**inten_pow_dict[inten_key]

        # asymetric reflection list
        asym_refl = np.array([h, k, l, I]).T



        sym_refl = apply_sym(asym_refl, self.spg)

        if fill_peaks:
            sym_refl = fill_missing(sym_refl)



        #bragg points
        self._scat_bragg = sym_refl


        ##### Reciprocal Space Units
        self._scat_rect = np.zeros(self.scat_bragg.shape)
        self._scat_rect[:, :-1] = np.matmul(self.scat_bragg[:, :-1], np.array([self.ast, self.bst, self.cst]))
        self._scat_rect[:, -1] = self.scat_bragg[:,-1]


        ##### Spherical Coordinates
        self._scat_sph = np.zeros(self.scat_rect.shape)
        self._scat_sph[:, :-1] = convert_rect2sph(self.scat_rect[:,:3])
        self._scat_sph[:, -1] = self.scat_bragg[:,-1]


        inten_loc = np.where(self._scat_sph[:,-1] != 0)[0] #positions that have intensity
        inten_qmax = self._scat_sph[inten_loc,0].max() #maximum q value of the positions with intensity


        if qmax is None:
            qmax = inten_qmax


        loc = np.where(self.scat_sph[:, 0] <= qmax)
        self._scat_rect = self._scat_rect[loc]
        self._scat_bragg = self._scat_bragg[loc]
        self._scat_sph = self._scat_sph[loc]


        self._qmax = np.round(np.max(self.scat_sph[:,0]), 14)

        self._scat_bragg = np.round(self.scat_bragg, 14)
        self._scat_sph = np.round(self.scat_sph, 14)
        self._scat_rect = np.round(self.scat_rect, 14)




