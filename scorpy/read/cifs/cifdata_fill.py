
import numpy as np






class CifDataFill:






    def fill_from_vhkl(self, path, qmax=None, skip_sym=False, fill_peaks=False):

        hklI = np.genfromtxt(path, skip_header=1, usecols=(0,1,2,6))

        hklI[:, -1] = hklI[:,-1]**2

        cif_dict = {}
        cif_dict['_refln.index_h'] =  hklI[:,0]
        cif_dict['_refln.index_k'] =  hklI[:,1]
        cif_dict['_refln.index_l'] =  hklI[:,2]
        cif_dict['_refln.intensity_meas'] = hklI[:,-1]

        self._calc_scat(cif_dict, qmax=qmax, skip_sym=skip_sym, fill_peaks=fill_peaks)


    def fill_from_hkl(self, path, qmax=None, skip_sym=False, fill_peaks=False):

        hklI = np.genfromtxt(path, skip_header=0, usecols=(0,1,2,3), skip_footer=1)
        ## to do: rather then read cols, should read %4d%4d%4d%8.2f%8.2f for fortran

        hs = []
        ks = []
        ls = []
        Is = []

        f = open(path, 'r')
        for line in f:
            hs.append(int(line[:4]))
            ks.append(int(line[4:8]))
            ls.append(int(line[8:12]))
            Is.append(float(line[12:20]))
        f.close()


        cif_dict = {}
        cif_dict['_refln.index_h'] = hs
        cif_dict['_refln.index_k'] =  ks
        cif_dict['_refln.index_l'] =  ls
        cif_dict['_refln.intensity_meas'] = Is

        self._calc_scat(cif_dict, qmax=qmax, skip_sym=skip_sym, fill_peaks=fill_peaks)






    def fill_from_merged_crystfel(self, path, qmax=None, skip_sym=False, fill_peaks=False, inten_thresh=0):

        hklI = np.genfromtxt(path, skip_header=3, skip_footer=1, usecols=(0,1,2,3))

        I = hklI[:,-1]

        inten_loc = np.where(I>inten_thresh)

        cif_dict = {}
        cif_dict['_refln.index_h'] = hklI[inten_loc[0],0]
        cif_dict['_refln.index_k'] = hklI[inten_loc[0],1]
        cif_dict['_refln.index_l'] = hklI[inten_loc[0],2]
        cif_dict['_refln.intensity_meas'] = hklI[inten_loc[0],3]


        # hklI = np.genfromtxt(path, skip_header=3, skip_footer=1, usecols=(0,1,2,3))
        # cif_dict = {}
        # cif_dict['_refln.index_h'] = hklI[:,0]
        # cif_dict['_refln.index_k'] = hklI[:,1]
        # cif_dict['_refln.index_l'] = hklI[:,2]
        # cif_dict['_refln.intensity_meas'] = hklI[:,3]

        self._calc_scat(cif_dict, qmax=qmax, skip_sym=skip_sym, fill_peaks=fill_peaks)







    def fill_from_sphv(self, sphv):

        ast_max_bragg_ind = round(sphv.qmax/self.ast_mag)+1
        bst_max_bragg_ind = round(sphv.qmax/self.bst_mag)+1
        cst_max_bragg_ind = round(sphv.qmax/self.cst_mag)+1

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
        q_inds = list(map(index_x_nowrap, sph_qtp[:, 0], 0 * ite, sphv.qmax * ite, sphv.nq * ite))
        theta_inds = list(map(index_x_nowrap, sph_qtp[:, 1], sphv.ymin * ite, sphv.ymax * ite, sphv.ny * ite))
        phi_inds = list(map(index_x_wrap, sph_qtp[:, 2], sphv.zmin * ite, sphv.zmax * ite, sphv.nz * ite))


        I = np.zeros(sph_qtp.shape[0])
        for i, (q_ind, theta_ind, phi_ind ) in enumerate(zip(q_inds, theta_inds, phi_inds )):
            I[i] += sphv.vol[q_ind, theta_ind, phi_ind]


        cif_dict = {}

        cif_dict['_symmetry.space_group_name_h-m'] = 'X'
        self._spg = 'X'

        cif_dict['_refln.index_h'] =  bragg_xyz[:,0]
        cif_dict['_refln.index_k'] =  bragg_xyz[:,1]
        cif_dict['_refln.index_l'] =  bragg_xyz[:,2]
        cif_dict['_refln.intensity_meas'] = I

        self._calc_scat(cif_dict, qmax=sphv.qmax, skip_sym=True, fill_peaks=False)






