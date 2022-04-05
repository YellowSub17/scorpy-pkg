


import numpy as np
import os
import shutil


from ..read.cifs.cifdata import CifData

from ..vols.sphv.sphericalvol import SphericalVol
from ..vols.corr.correlationvol import CorrelationVol
from ..vols.blqq.blqqvol import BlqqVol



class AlgoHandlerSetupRecon:


    def setup_recon(self, targ_cif_fname, supp_cif_fname, nq,npsi, nl, lcrop, qmax, pinv_rcond, rotk, rottheta, dxsupp):

        self.make_target(targ_cif_fname, nq, nl, qmax, rotk, rottheta)
        self.make_support(supp_cif_fname, nq, nl, qmax, rotk, rottheta, dxsupp)
        self.make_data(nq,npsi, nl,lcrop,  qmax,pinv_rcond, rotk, rottheta)






    def make_target(self, ciffname, nq, nl, qmax, rotk, rottheta):

        cif_targ = CifData(ciffname, qmax=qmax, rotk=rotk, rottheta=rottheta)

        cif_targ.save(f'{self.path}/{self.tag}_targ-sf.cif')
        sphv_targ = SphericalVol(nq=nq, ntheta=nl*2, nphi=nl*4, qmax=qmax)
        sphv_targ.fill_from_cif(cif_targ)
        sphv_targ.save(f'{self.path}/sphv_{self.tag}_targ.dbin')





    def make_support(self, ciffname, nq, nl, qmax, rotk, rottheta, dxsupp):
        cif_supp = CifData(ciffname, qmax=qmax, rotk=rotk, rottheta=rottheta)
        sphv_supp = SphericalVol(nq=nq, ntheta=nl*2, nphi=nl*4, qmax=qmax)
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





    def make_data(self, nq,npsi, nl, lcrop, qmax, pinv_rcond, rotk, rottheta):

        cif_targ = CifData(f'{self.path}/{self.tag}_targ-sf.cif', qmax=qmax, rotk=rotk, rottheta=rottheta)

        corr_data = CorrelationVol(nq, npsi, qmax)
        corr_data.fill_from_cif(cif_targ, verbose=2)
        blqq_data = BlqqVol(nq, nl, qmax)
        blqq_data.fill_from_corr(corr_data, rcond=pinv_rcond, verbose=1)
        blqq_data.vol[:,:,lcrop:] = 0

        blqq_data.save(f'{self.path}/blqq_{self.tag}_data.dbin')


    def run_recon(self, sub_tag, recipe):

        os.mkdir(f'{self.path}/{sub_tag}')


        shutil.copyfile(f'{recipe}', f'{self.path}/{sub_tag}/recipe_{self.tag}_{sub_tag}.txt')









