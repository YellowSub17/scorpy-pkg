


import numpy as np

from ..read.cifs.cifdata import CifData

from ..vols.sphv.sphericalvol import SphericalVol



class AlgoHandlerRecon:


    def make_target(self, ciffname):

        cif_targ = CifData(ciffname, qmax=self.qmax, rotk=self.rotk, rottheta=self.rottheta)

        if self.qmax is None:
            self.qmax = cif_targ.qmax
        cif_targ.save(f'{self.path}/{self.tag}_targ-sf.cif')
        sphv_targ = SphericalVol(nq=self.nq, ntheta=self.nl*2, nphi=self.nl*4, qmax=self.qmax)
        sphv_targ.fill_from_cif(cif_targ)
        sphv_targ.save(f'{self.path}/sphv_{self.tag}_targ.dbin')





    def make_support(self, ciffname, dxsupp=2):
        cif_supp = CifData(ciffname, qmax=self.qmax, rotk=self.rotk, rottheta=self.rottheta)
        if self.qmax is None:
            self.qmax = cif_supp.qmax
        sphv_supp = SphericalVol(nq=self.nq, ntheta=self.nl*2, nphi=self.nl*4, qmax=self.qmax)
        sphv_supp.vol+=1
        cif_supp.fill_from_sphv(sphv_supp)
        cif_supp.save(f'{self.path}/{self.tag}_supp-sf.cif')

        sphv_supp.vol*=0
        sphv_supp.fill_from_cif(cif_supp)

        for pti in sphv_supp.ls_pts(inds=True):
            xul = int(pti[0]-dxsupp), int(pti[0]+dxsupp+1)
            yul = int(pti[1]-dxsupp), int(pti[1]+dxsupp+1)
            zul = int(pti[2]-dxsupp), int(pti[2]+dxsupp+1)

            sphv_supp.vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]:zul[1]] = 1

            #wrap support around phi axis
            if zul[1]>sphv_supp.nz:
                sphv_supp.vol[xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]-sphv_supp.nz] = 1

            if zul[0]<0:
                sphv_supp.vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]:] = 1
                sphv_supp.vol[xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]] = 1

        sphv_supp.save(f'{self.path}/sphv_{self.tag}_supp.dbin')
        




        
        print(cif_supp.scat_bragg[:6, :])
        print(cif_supp.scat_sph[:6, :])



        return cif_supp






    def make_data(self):
        pass

#     def setup_recon(self):
        # pass

    # def load_recon(self):
        # pass

    # def run_recon(self):
        # pass

