
import numpy as np
from ...utils.convert_funcs import convert_rect2sph
import itertools

from ...utils.sym_funcs import apply_sym






class CifDataFill:

    def make_support(self ):
        self._scat_bragg[:,-1] = 1
        self._scat_rect[:,-1] = 1
        self._scat_sph[:,-1] = 1



    def calc_scat(self, h, k, l, I, fill_missing=True):


        #####sum check on hkl to ensure no doubles (eg 3 5 9 in agno3)

        self._scat_bragg = np.zeros( 4 )
        self._scat_sph = np.zeros( 4 )
        self._scat_rect = np.zeros( 4 )

        # asymetric reflection list
        asym_refl = np.array([h, k, l, I]).T

        # print('a', np.isnan(asym_refl).any())
        
        hklI = apply_sym(asym_refl, self.spg)

        # print('b', np.isnan(hklI).any())

        if fill_missing:
            hklI = self.fill_missing(hklI, ab_flag='b')
            hklI = self.fill_missing(hklI, ab_flag='a')


        hkl_uni, hkl_uni_i = np.unique(hklI[:,:-1], axis=0, return_index=True)

        hklI = hklI[hkl_uni_i]

        # print('c', np.isnan(hklI).any())
        #bragg points
        self._scat_bragg = hklI

        ##### Reciprocal Space Units
        self._scat_rect = np.zeros(self.scat_bragg.shape)
        self._scat_rect[:, :-1] = np.matmul(self.scat_bragg[:, :-1], np.array([self.ast, self.bst, self.cst]))
        self._scat_rect[:, -1] = self.scat_bragg[:,-1]


        ##### Spherical Coordinates
        self._scat_sph = np.zeros(self.scat_rect.shape)
        self._scat_sph[:, :-1] = convert_rect2sph(self.scat_rect[:,:3])
        self._scat_sph[:, -1] = self.scat_bragg[:,-1]

        self.make_qmax()

        # print('d', self._scat_bragg)
        



    def make_qmax(self):


        if self.qmax is None:
            self._qmax = self._scat_sph[:,0].max()

        # inten_loc = np.where(self.scat_sph[:,-1] >= 0)[0] #positions that have intensity
        # inten_qmax = self.scat_sph[inten_loc,0].max() #maximum q value of the positions with intensity


        # if self.qmax is None:
            # self._qmax = inten_qmax


        ##remove vectors above qmax
        loc = np.where(self.scat_sph[:, 0] <= self.qmax)
        self._scat_rect = self.scat_rect[loc]
        self._scat_bragg = self.scat_bragg[loc]
        self._scat_sph = self.scat_sph[loc]

        self._qmax = self._scat_sph[:,0].max()


    
    def fill_missing(self,hklI, ab_flag='b'):

        
        if ab_flag=='b':
            h_max, k_max, l_max = np.max(np.abs(hklI[:,:-1]), axis=0)
            missing_sf = np.nan

        elif ab_flag=='a':

            if self.qmax is None:
                return hklI

            missing_sf = np.nan
            h_max = int(self.qmax/self.ast_mag)+1
            k_max = int(self.qmax/self.bst_mag)+1
            l_max = int(self.qmax/self.cst_mag)+1


        h_ite = np.arange(-h_max, h_max+1)
        k_ite = np.arange(-k_max, k_max+1)
        l_ite = np.arange(-l_max, l_max+1)


        cube = set(itertools.product( h_ite, k_ite, l_ite))
        pts = set(map(tuple, hklI[:,:-1]))
        cube.difference_update(pts)

        missing_hklI = missing_sf*np.ones( (len(cube), 4) )

        missing_hklI[:, :-1] = np.array(list(cube))

        #remove 000
        loc_000 = np.all(missing_hklI[:, :3] == 0, axis=1)
        missing_hklI = missing_hklI[~loc_000]


        hklI_w_missing = np.concatenate( (hklI, missing_hklI), axis=0 )

        return hklI_w_missing






    def fill_from_cifdict(self, cif_dict, sep, fill_missing=False):


        h = np.array(cif_dict[f'_refln{sep}index_h']).astype(float).astype(np.int32)
        k = np.array(cif_dict[f'_refln{sep}index_k']).astype(float).astype(np.int32)
        l = np.array(cif_dict[f'_refln{sep}index_l']).astype(float).astype(np.int32)


        inten_pow_dict = {f'_refln{sep}intensity_meas':1,
                          f'_refln{sep}f_squared_meas':1,
                          f'_refln{sep}f_meas_au':2}


        inten_key = list(set(inten_pow_dict.keys()).intersection(cif_dict.keys()))[0]

        # print('x:', len(cif_dict[inten_key]))


        I = np.array(cif_dict[inten_key])

        # print('y:', len(I))

        nan_loc = np.where(I=='nan')
        # print(nan_loc)

        I = I.astype(float)**inten_pow_dict[inten_key]

 #        print('z:', len(I))
        # print('zz:', np.isnan(I).any())



        self.calc_scat(h, k, l , I, fill_missing=fill_missing)









    def fill_from_vhkl(self, path, fill_missing=False):


        hklI = np.genfromtxt(path, skip_header=1, usecols=(0,1,2,6))

        h, k, l, I = hklI[:,0], hklI[:,1], hklI[:,2], hklI[:,3]**2

        self._spg = 'X'
        self.calc_scat(h,k,l,I, fill_missing)



    def fill_from_shelx_hkl(self, path, fill_missing=False):


        # hklI = np.genfromtxt(path, skip_header=0, usecols=(0,1,2,3), skip_footer=1)
        ## to do: rather then read cols, should read %4d%4d%4d%8.2f%8.2f for fortran


        h,k,l,I = [],[],[],[]

        f = open(path, 'r')
        for line in f:
            h.append(int(line[:4]))
            k.append(int(line[4:8]))
            l.append(int(line[8:12]))
            I.append(float(line[12:20]))
        f.close()

        self._spg = 'X'
        self.calc_scat(h,k, l, I, fill_missing)




    def fill_from_sphv(self, sphv, fill_missing=False):


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




        if self.qmax is None:
            self._qmax = sphv.qmax
        qloc = np.where(sph_qtp[:,0] <= self.qmax)


        bragg_xyz = bragg_xyz[qloc]
        rect_xyz = rect_xyz[qloc]
        sph_qtp = sph_qtp[qloc]



        q_inds = sphv.get_indices(sph_qtp[:,0], axis=0)
        theta_inds = sphv.get_indices(sph_qtp[:,1], axis=1)
        phi_inds = sphv.get_indices(sph_qtp[:,2], axis=2)

        I = np.zeros(sph_qtp.shape[0])
        for i, (q_ind, theta_ind, phi_ind ) in enumerate(zip(q_inds, theta_inds, phi_inds )):
            I[i] += sphv.vol[q_ind, theta_ind, phi_ind]


        self._spg = 'X'

        h, k, l = bragg_xyz[:,0], bragg_xyz[:,1], bragg_xyz[:,2]

        self.calc_scat(h, k, l, I, fill_missing=fill_missing)











