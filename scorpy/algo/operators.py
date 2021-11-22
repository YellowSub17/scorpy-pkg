

import numpy as np


class AlgoHandlerOperators:



    def Ref_fn(self, fn, gamma=1, sphv_i=None):

        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()


        ##### input and output of functions
        fn_in, fn_out = fn(self.sphv_iter)

        ##### initiaize reflected volume and calculate, save to iterating vol
        self.sphv_r = self.sphv_base.copy()
        self.sphv_r.vol = (1 + gamma)*fn_out.vol - gamma*fn_in.vol
        self.sphv_iter = self.sphv_r.copy()

        ##### copy final output
        sphv_f = self.sphv_iter.copy()



        ##### return input and output
        return sphv_i, sphv_f



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
        # self.sphv_diff.vol = self.sphv_lm.vol - self.sphv_iter.vol

        ##### Transform K[I_(q, l, m)]
        self.knlm = self.iqlm_iter.copy()
        self.knlm.calc_knlm(self.us)

        ##### Inverse Transform K-1[ K[ I(q, l, m)] ]
        self.ikqlm = self.knlm.copy()
        self.ikqlm.calc_iqlmp(self.us)

        ##### difference lost over K transformation
        self.iqlm_diff = self.iqlm_base.copy()
        self.iqlm_diff.vals = self.iqlm_iter.vals - self.ikqlm.vals
        # self.iqlm_diff.vals = self.ikqlm.vals - self.iqlm_iter.vals

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


        ##### retrun input and output
        return sphv_i, sphv_f




    def Ps(self, sphv_i=None):
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

        self.sphv_b.vol[ self.sphv_b.vol <0] =0

        ##### replace iterating sphv
        self.sphv_iter = self.sphv_b.copy()

        ##### copy final output
        sphv_f = self.sphv_iter.copy()


        ##### return input and output
        return sphv_i, sphv_f


