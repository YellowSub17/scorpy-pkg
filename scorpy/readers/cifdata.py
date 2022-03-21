
import CifFile as pycif
import numpy as np
from ..utils import index_x, apply_sym
import itertools

from .readersprops import CifDataProperties






class CifData(CifDataProperties):

    def __init__(self,path, qmax=None, rotk=None, rottheta=None):




        starcif = pycif.ReadCif(path)
        vk = starcif.visible_keys[0]
        cif_dict = dict(starcif[vk])


        self._get_cell_params(cif_dict)
        self._get_cell_vecs(rotk = rotk, rottheta = rottheta)



        if '_refln.index_h' in cif_dict.keys():
            self._calc_scat_bragg(cif_dict)
            self._calc_scat_rect()
            self._calc_scat_sph()
            self._qcrop(qmax)


        else:
            self._scat_bragg = None
            self._scat_rect = None
            self._scat_sph = None
            self._qmax = None









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
                self._spg = cif_dict[key]







    def _get_cell_vecs(self, rotk=None, rottheta=np.pi/6):
        '''
        Calculate vectors for direct and reciprocal crystal lattices
        '''
        a_unit = np.array([1.0, 0.0, 0.0])
        b_unit = np.array([np.cos(self.gamma), np.sin(self.gamma), 0])
        c_unit = np.array([
            np.cos(self.beta),
            (np.cos(self.alpha) - np.cos(self.beta) * np.cos(self.gamma)) / np.sin(self.gamma),
            np.sqrt(1 - np.cos(self.beta)**2 - ((np.cos(self.alpha) - np.cos(self.beta) * np.cos(self.gamma)) / np.sin(self.gamma))**2)
        ])

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








    def _calc_scat_bragg(self, cif_dict):
        '''
        Parse cif data to generate scattering infomation, in Bragg indices,
        rectilinear reciprocal units, and spherical reciprocal units

        '''

        # Read h,k,l indices

        h = np.array(cif_dict['_refln.index_h']).astype(np.float).astype(np.int32)
        k = np.array(cif_dict['_refln.index_k']).astype(np.float).astype(np.int32)
        l = np.array(cif_dict['_refln.index_l']).astype(np.float).astype(np.int32)


        # Read intensities
        if '_refln.intensity_meas' in cif_dict.keys():
            I = np.array(cif_dict['_refln.intensity_meas'])
            I = np.where(I == '?', '0', I)
            I = I.astype(np.float64)
        elif '_refln.f_meas_au' in cif_dict.keys():
            I = np.array(cif_dict['_refln.f_meas_au'])
            I = np.where(I == '?', '0', I)
            I = I.astype(np.float64)**2
        elif '_refln.f_squared_meas' in cif_dict.keys():
            I = np.array(cif_dict['_refln.f_squared_meas'])
            I = np.where(I == '?', '0', I)
            I = I.astype(np.float64)
        else:
            print('WARNING: No intensity found when reading cif.')
            print('Requires: intensity_meas, f_meas_au, f_squared_meas')
            return None

        # apply symmetry to generate all bragg points
        asym_refl = np.array([h, k, l, I]).T
        loc = np.where(asym_refl[:, -1] >= 0)
        asym_refl = asym_refl[loc]
        self._scat_bragg = apply_sym(asym_refl, self.spg)


    def _calc_scat_rect(self):


        # update intensity vector to include reflections
        I = self.scat_bragg[:,-1]

        # convert bragg indices to rect reciprocal units
        rect_xyz = np.matmul(
            self.scat_bragg[:, :-1], np.array([self.ast, self.bst, self.cst]))
        scat_rect = np.zeros(self.scat_bragg.shape)
        scat_rect[:, :-1] = rect_xyz
        scat_rect[:, -1] = I

        self._scat_rect = scat_rect

    def _calc_scat_sph(self):

        # convert rect reciprocal units to spherical coords
        q_mag = np.linalg.norm(self.scat_rect[:,:-1], axis=1)
        # up and down
        theta = np.arctan2(np.linalg.norm(self.scat_rect[:, :2], axis=1), self.scat_rect[:, 2])  # 0 -> pi

        # around
        phi = np.arctan2(self.scat_rect[:, 1], self.scat_rect[:, 0])  # -pi -> pi
        phi[np.where(phi < 0)] = phi[np.where(phi < 0)] + 2 * np.pi  # 0 -> 2pi
        scat_sph = np.array([q_mag, theta, phi, self.scat_bragg[:,-1]]).T
        self._scat_sph = scat_sph






    def _qcrop(self, qmax):
        if qmax is not None:
            loc = np.where(self.scat_sph[:, 0] <= qmax)
            self._scat_rect = self._scat_rect[loc]
            self._scat_bragg = self._scat_bragg[loc]
            self._scat_sph = self._scat_sph[loc]

        self._qmax = np.round(np.max(self.scat_sph[:,0]), 14)

        self._scat_bragg = np.round(self.scat_bragg, 14)
        self._scat_sph = np.round(self.scat_sph, 14)
        self._scat_rect = np.round(self.scat_rect, 14)








    def fill_from_vhkl(self, path, qmax=None):

        hklI = np.genfromtxt(path, skip_header=1, usecols=(0,1,2,6))

        hklI[:, -1] = hklI[:,-1]**2

        loc = np.where(hklI[:, -1] >= 0)
        hklI = hklI[loc]
        self._scat_bragg = apply_sym(hklI, self.spg)



        self._calc_scat_rect()
        self._calc_scat_sph()
        self._qcrop(qmax)




    def fill_from_sphv(self, sphv):

        assert self.scat_bragg is None, "This CifData has already been filled."

        self._qmax = sphv.qmax

        max_bragg_ind = np.floor(self.qmax/min(self.ast_mag, self.bst_mag, self.cst_mag))

        if max_bragg_ind > 35:
            print(f'Max Bragg Index: {max_bragg_ind}')
            ans = input('Continue? (y/n)')
            if ans != 'y':
                return None



        ite = np.arange(-max_bragg_ind, max_bragg_ind+1)

        bragg_xyz = np.array(list(itertools.product( ite, ite, ite)))

        # remove 000 reflection
        loc_000 = np.all(bragg_xyz == 0, axis=1)
        bragg_xyz = bragg_xyz[~loc_000]

        rect_xyz = np.matmul(
            bragg_xyz, np.array([self.ast, self.bst, self.cst]))

        q_mag = np.linalg.norm(rect_xyz, axis=1)
        theta = np.arctan2(np.linalg.norm(rect_xyz[:, :2], axis=1), rect_xyz[:, 2])  # 0 -> pi
        phi = np.arctan2(rect_xyz[:, 1], rect_xyz[:, 0])  # -pi -> pi
        phi[np.where(phi < 0)] = phi[np.where(phi < 0)] + 2 * np.pi  # 0 -> 2pi
        sph_qtp = np.array([q_mag, theta, phi]).T

        loc = np.where(sph_qtp[:, 0] <= self.qmax)
        rect_xyz = rect_xyz[loc]
        bragg_xyz = bragg_xyz[loc]
        sph_qtp = sph_qtp[loc]

        ite = np.ones( sph_qtp.shape[0])

        q_inds = list(map(index_x, sph_qtp[:, 0], 0 * ite, sphv.qmax * ite, sphv.nq * ite))
        theta_inds = list(map(index_x, sph_qtp[:, 1], sphv.ymin * ite, sphv.ymax * ite, sphv.ny * ite))
        phi_inds = list(map(index_x, sph_qtp[:, 2], sphv.zmin * ite, sphv.zmax * ite, sphv.nz * ite, ite))



        scat_bragg = np.zeros( (sph_qtp.shape[0], 4))
        scat_bragg[:,:-1] = bragg_xyz

        scat_sph = np.zeros( (sph_qtp.shape[0], 4))
        scat_sph[:,:-1] = sph_qtp

        scat_rect = np.zeros( (sph_qtp.shape[0], 4))
        scat_rect[:,:-1] = rect_xyz


        for i, (q_ind, theta_ind, phi_ind ) in enumerate(zip(q_inds, theta_inds, phi_inds )):

            scat_bragg[i, -1] += sphv.vol[q_ind, theta_ind, phi_ind]
            scat_sph[i, -1] += sphv.vol[q_ind, theta_ind, phi_ind]
            scat_rect[i, -1] += sphv.vol[q_ind, theta_ind, phi_ind]


        #rm zeros peaks
        inten0_loc = scat_bragg[:,-1]==0
        scat_bragg = scat_bragg[~inten0_loc]
        scat_sph = scat_sph[~inten0_loc]
        scat_rect = scat_rect[~inten0_loc]


        self._scat_bragg = scat_bragg
        self._scat_sph = scat_sph
        self._scat_rect = scat_rect

        self._qcrop(sphv.qmax)


    def save(self, path):

        cif = pycif.CifFile()
        block = pycif.CifBlock()
        cif['block'] = block
        cif['block']['_symmetry.space_group_name_h-m'] = f'{self.spg}'
        cif['block']['_cell.angle_alpha'] = np.degrees(self.alpha)
        cif['block']['_cell.angle_beta'] = np.degrees(self.beta)
        cif['block']['_cell.angle_gamma'] = np.degrees(self.gamma)


        cif['block']['_cell.length_a'] = self.a_mag
        cif['block']['_cell.length_b'] = self.b_mag
        cif['block']['_cell.length_c'] = self.c_mag
        cif['block']['_refln.index_h'] = self.scat_bragg[:,0]
        cif['block']['_refln.index_k'] = self.scat_bragg[:,1]
        cif['block']['_refln.index_l'] = self.scat_bragg[:,2]
        cif['block']['_refln.intensity_meas'] = self.scat_bragg[:,3]
        cif['block'].CreateLoop( ['_refln.index_h', '_refln.index_k', '_refln.index_l', '_refln.intensity_meas'] )

        outfile = open(path, 'w')
        outfile.write(cif.WriteOut())
        outfile.close()


    def save_hkl(self, path):

        file = open(path, 'w')

        preamble = ''
        preamble += 'CrystFEL reflection list version 2.0\n'
        preamble += 'Symmetry: 1\n'
        preamble += '\th\tk\tl\tI\tphase\tsigma(I)\tnmeas\n'

        file.write(preamble)

        for scat in self.scat_bragg:
            line = f'\t{int(scat[0])}\t{int(scat[1])}\t{int(scat[2])}\t{scat[3]}\t-\t0.0\t1\n'
            file.write(line)

        postscript = ''
        postscript += 'End of reflections\n'
        postscript += 'Generated by CrystFEL 0.9.0\n'
        postscript += 'partialator -i cxi_io108_it1.stream -o ./it1_merging/108_it1_par.hkl -y 4/mmm --model=unity --iterations=1\n'
        postscript += 'Audit information from stream:\n'
        postscript += 'Generated by CrystFEL 0.9.0\n'
        postscript += 'indexamajig -i files.lst -o cxi_io108_it1.stream -g agipd_2304_opt_102020.geom -p 1vds.pdb --peaks=cxi -j 6 --multi --int-radius=2,3,5.\n'
        postscript += 'Indexing methods selected: dirax,asdf,xgandalf\n'

        file.write(postscript)

        file.close()


    # def save_pdb(self, path):

        # file = open(path, 'w')

        # cont = f'CRYST1   {self.a_mag}   {self.b_mag}   {self.c_mag}   {np.degrees(self.alpha)}   {np.degrees(self.beta)}   {np.degrees(self.gamma)} P -1     8\nEND'
        # file.write(cont)

        # file.close()

















































    def make_2D(self, lam):

        if lam is None:
            self._scat_sph[:,1] = np.pi/2
        else:
            self._scat_sph[:,1] = np.arccos( self._scat_sph[:,0]*lam/2)


    def bin_sph(self, nq, ntheta, nphi):

        qs = self.scat_sph[:, 0]
        ts = self.scat_sph[:, 1]
        ps = self.scat_sph[:, 2]

        ite = np.ones(np.shape(qs))

        qinds = list(map(index_x, qs, 0 * ite, self.qmax * ite, nq * ite))
        tinds = list(map(index_x, ts * ite, -np.pi * ite,
                         2, np.pi * ite / 2, ntheta * ite))
        pinds = list(map(index_x, ps * ite, 0 * ite,
                         2 * np.pi * ite, nphi * ite))

        qspace = np.linspace(0, self.qmax, nq)
        tspace = np.linspace(-np.pi / 2, np.pi / 2, ntheta)
        pspace = np.linspace(0, 2 * np.pi, nphi)

        self.scat_sph[:, 0] = qspace[qinds]
        self.scat_sph[:, 1] = tspace[tinds]
        self.scat_sph[:, 2] = pspace[pinds]



