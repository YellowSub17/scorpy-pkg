


import numpy as np
import os
import shutil


from ..read.cifs.cifdata import CifData

from ..vols.sphv.sphericalvol import SphericalVol
from ..vols.corr.correlationvol import CorrelationVol
from ..vols.blqq.blqqvol import BlqqVol
from ..iqlm.iqlmhandler import IqlmHandler

from ..utils.decorator_funcs import verbose_dec



class AlgoHandlerSetupRecon:



    @verbose_dec
    def save_targets(self, cif_fname, verbose=0):

        print('Saving Targets')

        cif_targ = CifData(path=cif_fname,qmax=self.qmax, fill_missing=True, rotk=self.rotk, rottheta=self.rottheta)
        cif_targ.save(self.cif_targ_path())
        # cif_targ.save_shelx_hkl(self.hkl_targ_path())

        # cif_targ = CifData(path=self.cif_targ_path(), rotk=self.rotk, rottheta=self.rottheta)


        sphv_targ = SphericalVol(nq=self.nq, ntheta=self.nl*2, nphi=self.nl*4, qmax=self.qmax, qmin=self.qmin)
        sphv_targ.fill_from_cif(cif_targ)
        sphv_targ.save(self.sphv_targ_path())






    @verbose_dec
    def make_support(self, verbose=0):
        print('Making Support')

        cif_supp = CifData(path=self.cif_targ_path(),  rotk=self.rotk, rottheta=self.rottheta)
        cif_supp.make_support()

        cif_supp.save(self.cif_supp_path())


        sphv_supp_tight = SphericalVol(nq=self.nq, ntheta=self.nl*2, nphi=self.nl*4, qmax=self.qmax, qmin=self.qmin)
        sphv_supp_tight.fill_from_cif(cif_supp)

        tight_overlaps = np.where(sphv_supp_tight.vol>1)
        if len(tight_overlaps[0])>0:
            print('OVERLAP IN TIGHT SUPPORT')

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

        # overlaps = np.where(sphv_supp_loose.vol>1)
        # if len(overlaps[0])>0:
            # print('OVERLAP IN SUPPORT')


        loose_overlaps = np.where(sphv_supp_loose.vol>1)
        if len(loose_overlaps[0])>0:
            print('OVERLAP IN LOOSE SUPPORT')


        sphv_supp_loose.save(self.sphv_supp_loose_path())





    @verbose_dec
    def make_data(self,  verbose=0, save_corr=True, corr_nchunks=1):
        print('Making Data')

        cif_targ = CifData(path=self.cif_targ_path(),  rotk=self.rotk, rottheta=self.rottheta)

        corr_data = CorrelationVol(self.nq, self.npsi, self.qmax, self.qmin)
        corr_data.fill_from_cif(cif_targ, nchunks=corr_nchunks, verbose=verbose-1)
        blqq_data = BlqqVol(self.nq, self.nl, self.qmax, self.qmin)
        blqq_data.fill_from_corr(corr_data, rcond=self.pinv_rcond, verbose=verbose-1)
        # blqq_data.vol[:,:,self.lcrop:] = 0

        blqq_data.save(self.blqq_data_path())

        if save_corr:
            corr_data.save(self.corr_data_path())
















