


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
    def make_target(self, ciffname, verbose=0):

        print('Making Target')

        cif_targ = CifData(ciffname, qmax=self.qmax, rotk=self.rotk, rottheta=self.rottheta)
        cif_targ.save(self.cif_targ_path())

        if self.qmax is None:
            self.qmax = cif_targ.qmax
        sphv_targ = SphericalVol(nq=self.nq, ntheta=self.nl*2, nphi=self.nl*4, qmax=self.qmax)
        sphv_targ.fill_from_cif(cif_targ)
        sphv_targ.save(self.cif_targ_path())


        self.save_params()



    @verbose_dec
    def make_support(self, ciffname, verbose=0, unit=False):
        print('Making Support')

        assert self.qmax is not None, "Cannot make support, qmax required"

        cif_supp = CifData(ciffname, rotk=self.rotk, rottheta=self.rottheta)
        sphv_supp_tight = SphericalVol(nq=self.nq, ntheta=self.nl*2, nphi=self.nl*4, qmax=self.qmax)
        sphv_supp_tight.vol+=1
        cif_supp.fill_from_sphv(sphv_supp_tight)
        sphv_supp_tight.vol*=0
        sphv_supp_tight.fill_from_cif(cif_supp)

        # sphv_supp_tight.save(f'{self.path}/sphv_{self.tag}_supp_tight.dbin')
        sphv_supp_tight.save(self.sphv_supp_tight_path())


        sphv_supp_loose = sphv_supp_tight.copy()
        sphv_supp_loose.vol *=0

        for pti in sphv_supp_tight.ls_pts(inds=True):
            xul = int(pti[0]-self.dxsupp), int(pti[0]+self.dxsupp+1)
            yul = int(pti[1]-self.dxsupp), int(pti[1]+self.dxsupp+1)
            zul = int(pti[2]-self.dxsupp), int(pti[2]+self.dxsupp+1)

            sphv_supp_loose.vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]:zul[1]] += 1

            #wrap support around phi axis
            if zul[1]>sphv_supp_loose.nz:
                sphv_supp_loose.vol[xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]-sphv_supp_loose.nz] += 1

            if zul[0]<0:
                sphv_supp_loose.vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]:] += 1
                sphv_supp_loose.vol[xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]] += 1

        overlaps = np.where(sphv_supp_loose.vol>1)
        if len(overlaps[0])>0:
            print('OVERLAP IN SUPPORT')

        if unit:
            sphv_supp_loose.make_mask()

        sphv_supp_loose.save(self.sphv_supp_loose_path())







    # # @verbose_dec
    # def check_support_overlap(self, ciffname, verbose=0, boundry=0):
        # print('Checking Support')
        # assert self.qmax is not None, "Cannot make support, qmax required"

        # cif_supp = CifData(ciffname, rotk=self.rotk, rottheta=self.rottheta)
        # sphv_supp_tight = SphericalVol(nq=self.nq, ntheta=self.nl*2, nphi=self.nl*4, qmax=self.qmax)
        # sphv_supp_tight.vol+=1
        # cif_supp.fill_from_sphv(sphv_supp_tight)
        # sphv_supp_tight.vol*=0
        # sphv_supp_tight.fill_from_cif(cif_supp)

        # # sphv_supp_tight.save(f'{self.path}/sphv_{self.tag}_supp_tight.dbin')
        # sphv_supp_loose = sphv_supp_tight.copy()
        # sphv_supp_loose.vol *=0

        # for pti in sphv_supp_tight.ls_pts(inds=True):
            # xul = int(pti[0]-self.dxsupp-boundry), int(pti[0]+self.dxsupp+1+boundry)
            # yul = int(pti[1]-self.dxsupp-boundry), int(pti[1]+self.dxsupp+1+boundry)
            # zul = int(pti[2]-self.dxsupp-boundry), int(pti[2]+self.dxsupp+1+boundry)

            # sphv_supp_loose.vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]:zul[1]] += 1

            # #wrap support around phi axis
            # if zul[1]>sphv_supp_loose.nz:
                # sphv_supp_loose.vol[xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]-sphv_supp_loose.nz] += 1

            # if zul[0]<0:
                # sphv_supp_loose.vol[xul[0]:xul[1], yul[0]:yul[1], zul[0]:] += 1
                # sphv_supp_loose.vol[xul[0]:xul[1], yul[0]:yul[1], 0:zul[1]] += 1

        # overlaps = np.where(sphv_supp_loose.vol>1)
        # return overlaps
        # # print('o', overlaps)
        # if len(overlaps[0])>0:
            # print('OVERLAP IN SUPPORT')








    @verbose_dec
    def make_data(self,  verbose=0):
        print('Making Data')

        cif_targ = CifData(f'{self.path}/{self.tag}_targ-sf.cif', qmax=self.qmax, rotk=self.rotk, rottheta=self.rottheta)

        corr_data = CorrelationVol(self.nq, self.npsi, self.qmax)
        corr_data.fill_from_cif(cif_targ, verbose=verbose-1)
        blqq_data = BlqqVol(self.nq, self.nl, self.qmax)
        blqq_data.fill_from_corr(corr_data, rcond=self.pinv_rcond, verbose=verbose-1)
        blqq_data.vol[:,:,self.lcrop:] = 0

        blqq_data.save(f'{self.path}/blqq_{self.tag}_data.dbin')













