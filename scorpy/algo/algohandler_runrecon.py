


import numpy as np
import os
import shutil
import time


from ..read.cifs.cifdata import CifData

from ..vols.sphv.sphericalvol import SphericalVol
from ..vols.corr.correlationvol import CorrelationVol
from ..vols.blqq.blqqvol import BlqqVol
from ..iqlm.iqlmhandler import IqlmHandler

from ..utils.utils import verbose_dec



class AlgoHandlerRunRecon:


    @verbose_dec
    def check_inputs(self, verbose=0):
        print(f'Checking Inputs')
        assert os.path.exists(self.blqq_data_path()), "Data BlqqVol not saved to algo folder"
        blqq = BlqqVol(path=self.blqq_data_path())


        assert os.path.exists(self.sphv_supp_loose_path()), "Support SphericalVol not saved to algo folder"
        sphv_supp = SphericalVol(path=self.sphv_supp_loose_path())


        assert blqq.nq == sphv_supp.nq == self.nq
        assert blqq.qmax == sphv_supp.qmax == self.qmax
        assert blqq.nl*2 == sphv_supp.ntheta
        assert blqq.nl*4 == sphv_supp.nphi
        assert self.nl == blqq.nl




        # save eigens
        self.lams, self.us = blqq.get_eig()
        eigs_thresh = np.max(self.lams, axis=0)*self.eig_rcond
        for l_ind, eig_thresh in enumerate(eigs_thresh):
            loc = np.where(np.abs(self.lams[:,l_ind]) < eig_thresh)
            self.lams[loc, l_ind] = 0
            loc = np.where(self.lams[:,l_ind] ==0)
            self.us[:, loc, l_ind] = 0

        # save support
        self.supp_loc = np.where(sphv_supp.vol != 0 )
        self.supp_notloc = np.where(sphv_supp.vol == 0 )

        # save base
        self.iqlm_base = IqlmHandler(self.nq, self.nl, self.qmax, True)
        self.sphv_base = SphericalVol(self.nq, self.nl*2, self.nl*4, self.qmax)


    @verbose_dec
    def run_recon(self, sub_tag, recipe, sphv_init=None, verbose=0):


        print(f'Running Recon {self.tag}_{sub_tag}')
        print(f'Started: {time.asctime()}')



        os.mkdir(f'{self.path}/{sub_tag}')
        os.mkdir(f'{self.path}/{sub_tag}/hkls')

        shutil.copyfile(f'{recipe}', f'{self.path}/{sub_tag}/recipe_{self.tag}_{sub_tag}.txt')


        if sphv_init is not None:
            self.sphv_iter = sphv_init.copy()
        else:
            self.sphv_iter = self.sphv_base.copy()
            self.sphv_iter.vol = 2*np.random.random(self.sphv_iter.vol.shape)-1







        self.sphv_iter.save(f'{self.path}/{sub_tag}/sphv_{self.tag}_{sub_tag}_init.dbin')





        recipe_file = open(f'{self.path}/{sub_tag}/recipe_{self.tag}_{sub_tag}.txt')

        count = 0
        for line in recipe_file:

            terms = line.split()
            if terms == [] or line[0]=='#':
                continue
            niter = int(terms[0])
            scheme = eval('self.'+terms[1])

            kwargs = {}
            for kwarg in terms[2:]:
                kwargs[kwarg.split('=')[0]] = eval(kwarg.split('=')[1])



            print(f'Running: {line[:-1]}')
            for iter_num in range(niter):
                print(f'{iter_num}', end='\r')


                self.sphv_iter.save(self.sphv_iter_path(sub_tag))
                self.integrate_iter(sub_tag)


                _,_, step = scheme(**kwargs)
                count +=1

        self.sphv_iter.save(self.sphv_iter_path(sub_tag))
        self.integrate_iter(sub_tag)
        cif_integrated = CifData(self.cif_targ_path(), rotk=self.rotk, rottheta=self.rottheta)



        print(f'Finished: {time.asctime()}')










    def integrate_iter(self,sub_tag):

        sphv_supp_tight = SphericalVol(path=self.sphv_supp_tight_path())
        sphv_integrated = SphericalVol(path=self.sphv_iter_path(sub_tag))
        sphv_integrated.integrate_peaks(sphv_supp_tight, self.dxsupp)
        sphv_integrated.save(self.sphv_final_path(sub_tag))

        cif_integrated = CifData(self.cif_targ_path(), rotk=self.rotk, rottheta=self.rottheta)
        cif_integrated.fill_from_sphv(sphv_integrated)
        cif_integrated.save(self.cif_final_path(sub_tag))
        cif_integrated.save_hkl(self.hkl_count_path(sub_tag, count=None))






