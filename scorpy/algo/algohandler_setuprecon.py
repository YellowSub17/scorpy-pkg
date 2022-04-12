


import numpy as np
import os
import shutil


from ..read.cifs.cifdata import CifData

from ..vols.sphv.sphericalvol import SphericalVol
from ..vols.corr.correlationvol import CorrelationVol
from ..vols.blqq.blqqvol import BlqqVol
from ..iqlm.iqlmhandler import IqlmHandler

from ..utils.utils import verbose_dec



class AlgoHandlerSetupRecon:







    @verbose_dec
    def make_target(self, ciffname, insfname=None, verbose=0):

        print('Making target')

        # assert not os.path.exists(f'{self.path}/sphv_{self.tag}_targ.dbin'), "Target sphv already in folder"
        # assert not os.path.exists(f'{self.path}/{self.tag}_targ-sf.cif'), "Target cif already in folder"



        cif_targ = CifData(ciffname, qmax=self.qmax, rotk=self.rotk, rottheta=self.rottheta)
        cif_targ.save(f'{self.path}/{self.tag}_targ-sf.cif')

        if self.qmax is None:
            self.qmax = cif_targ.qmax
        sphv_targ = SphericalVol(nq=self.nq, ntheta=self.nl*2, nphi=self.nl*4, qmax=self.qmax)
        sphv_targ.fill_from_cif(cif_targ)
        sphv_targ.save(f'{self.path}/sphv_{self.tag}_targ.dbin')

        if insfname is not None:
            shutil.copyfile(insfname, f'{self.path}/{self.tag}.ins')



        self.save_params()





    @verbose_dec
    def make_support(self, ciffname, verbose=0):
        print('Making support')

        # assert not os.path.exists(f'{self.path}/sphv_{self.tag}_supp.dbin'), "Support SphericalVol already in folder"
        # assert not os.path.exists(f'{self.path}/{self.tag}_supp-sf.cif'), "Support cif already in folder"

        assert self.qmax is not None, "Cannot make support, qmax required"

        cif_supp = CifData(ciffname, rotk=self.rotk, rottheta=self.rottheta)
        sphv_supp = SphericalVol(nq=self.nq, ntheta=self.nl*2, nphi=self.nl*4, qmax=self.qmax)
        sphv_supp.vol+=1
        cif_supp.fill_from_sphv(sphv_supp)
        sphv_supp.vol*=0
        sphv_supp.fill_from_cif(cif_supp)

        sphv_supp.save(f'{self.path}/sphv_{self.tag}_supp_tight.dbin')

        for pti in sphv_supp.ls_pts(inds=True):
            xul = int(pti[0]-self.dxsupp), int(pti[0]+self.dxsupp+1)
            yul = int(pti[1]-self.dxsupp), int(pti[1]+self.dxsupp+1)
            zul = int(pti[2]-self.dxsupp), int(pti[2]+self.dxsupp+1)

            sphv_supp.vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]:zul[1]] = 1

            #wrap support around phi axis
            if zul[1]>sphv_supp.nz:
                sphv_supp.vol[xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]-sphv_supp.nz] = 1

            if zul[0]<0:
                sphv_supp.vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]:] = 1
                sphv_supp.vol[xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]] = 1

        sphv_supp.save(f'{self.path}/sphv_{self.tag}_supp_loose.dbin')


    @verbose_dec
    def make_data(self,  verbose=0):
        print('Making data')

        cif_targ = CifData(f'{self.path}/{self.tag}_targ-sf.cif', qmax=self.qmax, rotk=self.rotk, rottheta=self.rottheta)

        corr_data = CorrelationVol(self.nq, self.npsi, self.qmax)
        corr_data.fill_from_cif(cif_targ, verbose=verbose-1)
        blqq_data = BlqqVol(self.nq, self.nl, self.qmax)
        blqq_data.fill_from_corr(corr_data, rcond=self.pinv_rcond, verbose=verbose-1)
        blqq_data.vol[:,:,self.lcrop:] = 0

        blqq_data.save(f'{self.path}/blqq_{self.tag}_data.dbin')













