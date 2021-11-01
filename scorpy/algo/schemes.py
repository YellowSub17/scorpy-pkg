



class AlgoHandlerSchemes:



    def ER(self, sphv_i=None):

        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()

        self.Pm()
        self.Pm()
        self.Ps()

        sphv_f = self.sphv_iter.copy()

        return sphv_i, sphv_f


    def HIO(self, beta=0.99, sphv_i=None):



        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()

        self.Pm()
        self.Pm()
        pm_out, ps_out = self.Ps()

        self.sphv_iter.vol[self.supp_notloc] = sphv_i.vol[self.supp_notloc] - beta*pm_out.vol[self.supp_notloc]

        sphv_f = self.sphv_iter.copy()
        return sphv_i, sphv_f


    def DM(self, beta=0.7, gamma_m=-1/0.7, gamma_s=1/0.7, sphv_i=None):

        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()


        _, p1 = self.Rm(gamma_m, sphv_i)
        _, p1 = self.Ps(p1)

        _, p2 = self.Rs(gamma_m, sphv_i)
        _, p2 = self.Pm(p2)
        _, p2 = self.Pm(p2)

        self.sphv_iter.vol = sphv_i.vol + beta*(p1.vol - p2.vol)


        sphv_f = self.sphv_iter.copy()
        return sphv_i, sphv_f


    def RAAR(self, beta=0.5, gamma_m=1, gamma_s=1, sphv_i=None):

        if sphv_i is None:
            sphv_i = self.sphv_iter.copy()
        else:
            self.sphv_iter = sphv_i.copy()

        _, p1 = self.Rm(gamma_m, sphv_i)
        _, p1 = self.Rs(gamma_s, sphv_i)

        p1.vol += sphv_i.vol
        p1.vol *= beta/2

        _, p2 = self.Pm(sphv_i)
        _, p2 = self.Pm(p2)
        p2.vol *= (1-beta)

        self.sphv_iter.vol = p1.vol + p2.vol

        sphv_f = self.sphv_iter.copy()
        return sphv_i, sphv_f





































