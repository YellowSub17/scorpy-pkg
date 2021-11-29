

import numpy as np


class AlgoHandlerSchemes:



    def ER(self, sphv_i=None, posit=True):
        '''Error Reduction'''


        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()

        self.Pm()
        self.Ps(posit=posit)

        sphv_f = self.sphv_iter.copy()


        err = np.linalg.norm(sphv_f.vol - sphv_i.vol)

        return sphv_i, sphv_f, err


    def SF(self, sphv_i=None):
        '''Solvent Flipping'''


        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()

        self.Pm()
        self.Rs()

        sphv_f = self.sphv_iter.copy()


        err = np.linalg.norm(sphv_f.vol - sphv_i.vol)
        return sphv_i, sphv_f, err




    def HIO(self, beta=0.9, sphv_i=None, posit=True):
        '''Hybrid Input Output'''



        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()

        self.Pm()
        pm_out, ps_out, _ = self.Ps(posit=posit)

        self.sphv_iter.vol[self.supp_notloc] = sphv_i.vol[self.supp_notloc] - beta*pm_out.vol[self.supp_notloc]

        sphv_f = self.sphv_iter.copy()


        err = np.linalg.norm(sphv_f.vol - sphv_i.vol)
        return sphv_i, sphv_f, err


    def DM(self, beta=0.7, gamma_m=None, gamma_s=None, sphv_i=None, posit=True):
        '''Difference Map'''



        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()

        if beta==0:
            sphv_f = self.sphv_iter.copy()
            return sphv_i, sphv_f

        if gamma_m is None:
            gamma_m = 1/beta

        if gamma_s is None:
            gamma_s = -1/beta



        _, p1, _ = self.Rm(gamma_m, sphv_i)
        _, p1, _ = self.Ps(p1, posit=posit)

        _, p2, _ = self.Rs(gamma_m, sphv_i)
        _, p2, _ = self.Pm(p2)

        self.sphv_iter.vol = sphv_i.vol + beta*(p1.vol - p2.vol)


        sphv_f = self.sphv_iter.copy()

        err = np.linalg.norm(sphv_f.vol - sphv_i.vol)

        return sphv_i, sphv_f, err




    def ASR(self, gamma_m=1, gamma_s=1, sphv_i=None):
        '''Averaged Successive Reflections'''

        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()


        self.Rm()
        self.Rs()

        self.sphv_iter.vol += sphv_i.vol

        self.sphv_iter.vol *=0.5


        sphv_f = self.sphv_iter.copy()

        err = np.linalg.norm(sphv_f.vol - sphv_i.vol)

        return sphv_i, sphv_f, err




    def HPR(self, beta=0.5, gamma_m=1, gamma_s=1, sphv_i=None):
        '''Hybrid Projection Reflection'''

        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()


        _, p1, _ = self.Rm(gamma_m, sphv_i)
        _, p1, _ = self.Rs(gamma_s, p1)


        _, pm, _ = self.Pm(sphv_i)

        p2 = pm.copy()
        p2.vol *= (beta-1)
        _, p2, _ = self.Rs(gamma_s, p2)



        p3 = sphv_i.copy()

        p4 = pm.copy()
        p4.vol *= (1-beta)

        self.sphv_iter.vol = 0.5*(p1.vol + p2.vol + p3.vol + p4.vol)

        sphv_f = self.sphv_iter.copy()

        err = np.linalg.norm(sphv_f.vol - sphv_i.vol)

        return sphv_i, sphv_f, err








    def RAAR(self, beta=0.5, gamma_m=1, gamma_s=1, sphv_i=None):
        '''Relaxed Averaged Alternating Reflectors'''


        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()

        _, p1, _ = self.Rm(gamma_m, sphv_i)
        _, p1, _ = self.Rs(gamma_s, p1)

        p1.vol += sphv_i.vol
        p1.vol *= beta/2

        _, p2, _ = self.Pm(sphv_i)
        p2.vol *= (1-beta)

        self.sphv_iter.vol = p1.vol + p2.vol

        sphv_f = self.sphv_iter.copy()

        err = np.linalg.norm(sphv_f.vol - sphv_i.vol)
        return sphv_i, sphv_f, err







































