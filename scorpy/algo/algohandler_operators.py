

import numpy as np


class AlgoHandlerOperators:



    def Ref_fn(self, fn, gamma=1, sphv_i=None):

        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()


        ##### input and output of functions
        fn_in, fn_out, _ = fn(self.sphv_iter)

        ##### initiaize reflected volume and calculate, save to iterating vol
        self.sphv_r = self.sphv_base.copy()
        self.sphv_r.vol = (1 + gamma)*fn_out.vol - gamma*fn_in.vol
        self.sphv_iter = self.sphv_r.copy()

        ##### copy final output
        sphv_f = self.sphv_iter.copy()

        err = np.linalg.norm(sphv_f.vol - sphv_i.vol)

        ##### return input, output and error
        return sphv_i, sphv_f, err



    def Rm(self, gamma=1, sphv_i=None):
        return self.Ref_fn(self.Pm, gamma, sphv_i)

    def Rs(self, gamma=1, sphv_i=None):
        return self.Ref_fn(self.Ps, gamma, sphv_i)






    def Pm(self, sphv_i=None):


        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()


        ##### Convert spherical coordinates to harmonic coeff.
        self.iqlm_iter = self.iqlm_base.copy()
        self.iqlm_iter.fill_from_sphv(self.sphv_iter)

        ##### get low pass filtered spherical coordinates
        self.sphv_lm = self.sphv_base.copy()
        self.sphv_lm.fill_from_iqlm(self.iqlm_iter)

        ##### difference lost between low pass filtered and original coords.
        self.sphv_diff = self.sphv_base.copy()
        self.sphv_diff.vol = self.sphv_iter.vol - self.sphv_lm.vol

        ##### Transform K[I_(q, l, m)]
        self.knlm = self.iqlm_iter.copy()
        self.knlm.calc_knlm(self.us)

        ##### Inverse Transform K-1[ K[ I(q, l, m)] ]
        self.ikqlm = self.knlm.copy()
        self.ikqlm.calc_iqlmp(self.us)

        ##### difference lost over K transformation
        self.iqlm_diff = self.iqlm_base.copy()
        self.iqlm_diff.vals = self.iqlm_iter.vals - self.ikqlm.vals

        ##### Calculate K' after modifered by lamda
        self.knlmp = self.knlm.copy()
        # print('RM ME: uncomment calc_knlmp')
        self.knlmp.calc_knlmp(self.lams)

        ##### Inverse K' to I(q, l, m)
        self.iqlmp = self.knlmp.copy()
        self.iqlmp.calc_iqlmp(self.us)

        ##### Add in difference lost over K trasnformation
        self.iqlm_add = self.iqlmp.copy()
        if self.lossy_iqlm:
            self.iqlm_add.vals += self.iqlm_diff.vals


        ##### calculate the spherical coordinates deom new harmonics
        self.sphvp = self.sphv_base.copy()
        self.sphvp.fill_from_iqlm(self.iqlm_add)


        ##### Add in difference lost over low pass filter 
        self.sphv_add = self.sphvp.copy()
        if self.lossy_sphv:
            self.sphv_add.vol += self.sphv_diff.vol

        ##### replace iterating volume
        self.sphv_iter = self.sphv_add.copy()

        ##### copy final output
        sphv_f = self.sphv_iter.copy()

        err = np.linalg.norm(sphv_f.vol - sphv_i.vol)

        ##### retrun input and output
        return sphv_i, sphv_f, err




    def Ps(self, sphv_i=None, posit=True):
        '''

        add positivitiy constraint
        set negative values to 0 inside support
        '''

        #tight support : known shape
        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()


        ##### only keep intenisty values at bragg positions defined by support
        self.sphv_b = self.sphv_base.copy()

        self.sphv_b.vol = self.sphv_iter.vol * self.sphv_supp.vol


        # # # # #global positivitiy: if the intensity is still negative, set to 0
        self.sphv_b.vol[self.sphv_b.vol<0] = 0


        ##### replace iterating sphv
        self.sphv_iter = self.sphv_b.copy()

        ##### copy final output
        sphv_f = self.sphv_iter.copy()


        err = np.linalg.norm(sphv_f.vol - sphv_i.vol)
        ##### return input and output
        return sphv_i, sphv_f, err




    def Pm_fast(self):


        sphv_i_vol = self.sphv_iter.vol


        ##### Convert spherical coordinates to harmonic coeff.
        self.iqlm_iter.fill_from_sphv(self.sphv_iter)

        ##### get low pass filtered spherical coordinates
        self.sphv_iter.fill_from_iqlm(self.iqlm_iter)
        sphv_lm_vol = self.sphv_iter.vol

        ##### difference lost between low pass filtered and original coords.
        sphv_diff_vol = sphv_i_vol - sphv_lm_vol

        ##### Transform K[I_(q, l, m)]
        self.iqlm_iter.calc_knlm(self.us)
        knlm_vals = self.iqlm_iter.vals

        ##### Inverse Transform K-1[ K[ I(q, l, m)] ]
        self.iqlm_iter.calc_iqlmp(self.us)
        ikqlm_vals = self.iqlm_iter.vals


        self.iqlm_iter.vals = knlm_vals

        ##### difference lost over K transformation
        iqlm_diff_vals = self.iqlm_iter.vals - ikqlm_vals

        ##### Calculate K' after modifered by lamda
        # print('RM ME: uncomment calc_knlmp')
        self.iqlm_iter.calc_knlmp(self.lams)
        knlmp_vals = self.iqlm_iter.vals

        ##### Inverse K' to I(q, l, m)
        self.iqlm_iter.calc_iqlmp(self.us)
        iqlmp_vals = self.iqlm_iter.vals

        ##### Add in difference lost over K trasnformation
        self.iqlm_iter.vals += iqlm_diff_vals


        ##### calculate the spherical coordinates deom new harmonics
        self.sphv_iter.fill_from_iqlm(self.iqlm_iter)


        ##### Add in difference lost over low pass filter 
        self.sphv_iter.vol += sphv_diff_vol


        return None, None, None




    def Ps_fast(self):
        '''

        add positivitiy constraint
        set negative values to 0 inside support
        '''


        self.sphv_iter.vol *= self.sphv_supp.vol

        # # # # #global positivitiy: if the intensity is still negative, set to 0
        self.sphv_iter.vol[self.sphv_iter.vol<0] = 0



        return None, None, None


