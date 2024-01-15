
import CifFile as pycif
import numpy as np
from ...utils.convert_funcs import index_x_wrap, index_x_nowrap, convert_rect2sph
import itertools

from .cifdata_props import CifDataProperties
from .cifdata_saveload import CifDataSaveLoad
from .cifdata_fill import CifDataFill




class CifData(CifDataProperties, CifDataSaveLoad, CifDataFill):

    def __init__(self,a_mag=1, b_mag=1, c_mag=1,
                 alpha=90, beta=90, gamma=90,
                 spg='X', qmax=None, rotk=[1,0,0], rottheta=0, fill_missing=False, path=None):


        if path is not None:

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

        else:

            ### get cell angles
            self._alpha = np.radians(alpha)
            self._beta = np.radians(beta)
            self._gamma = np.radians(gamma)

            ### get cell sides
            self._a_mag = a_mag
            self._b_mag = b_mag
            self._c_mag = c_mag

            self._spg = spg
           


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


        self._qmax = qmax

        if path is not None:
            self.fill_from_cifdict(cif_dict, sep, fill_missing)



