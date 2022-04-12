


import numpy as np
import os
import shutil


from ..read.cifs.cifdata import CifData

from ..vols.sphv.sphericalvol import SphericalVol
from ..vols.corr.correlationvol import CorrelationVol
from ..vols.blqq.blqqvol import BlqqVol
from ..iqlm.iqlmhandler import IqlmHandler

from ..utils.utils import verbose_dec



class AlgoHandlerRunRecon:






    @verbose_dec
    def run_recon(self, sub_tag, recipe, sphv_init=None, verbose=0):
        print('Running recon')

        assert os.path.exists(f'{self.path}/blqq_{self.tag}_data.dbin'), "Data BlqqVol not saved to algo folder"
        self.blqq = BlqqVol(path=f'{self.path}/blqq_{self.tag}_data.dbin')
        self.lams, self.us = self.blqq.get_eig()
        #condition threshold
        eigs_thresh = np.max(self.lams, axis=0)*self.eig_rcond
        for l_ind, eig_thresh in enumerate(eigs_thresh):
            loc = np.where(np.abs(self.lams[:,l_ind]) < eig_thresh)
            self.lams[loc, l_ind] = 0
            loc = np.where(self.lams[:,l_ind] ==0)
            self.us[:, loc, l_ind] = 0




        assert os.path.exists(f'{self.path}/sphv_{self.tag}_supp_loose.dbin'), "Support SphericalVol not saved to algo folder"
        self.sphv_supp = SphericalVol(path=f'{self.path}/sphv_{self.tag}_supp_loose.dbin')
        self.supp_loc = np.where(self.sphv_supp.vol == 1 )
        self.supp_notloc = np.where(self.sphv_supp.vol == 0 )


        assert self.blqq.nq ==self.sphv_supp.nq
        self.nq = self.blqq.nq

        assert self.blqq.nl*2 ==self.sphv_supp.ntheta
        assert self.blqq.nl*4 ==self.sphv_supp.nphi

        self.nl = self.blqq.nl
        self.ntheta = self.sphv_supp.ntheta
        self.nphi = self.sphv_supp.nphi

        assert self.blqq.qmax == self.sphv_supp.qmax

        self.qmax = self.blqq.qmax

        # ##### base objects to copy from
        self.iqlm_base = IqlmHandler(self.nq, self.nl, self.qmax,True)
        self.sphv_base = SphericalVol(self.nq, self.ntheta, self.nphi, self.qmax)



        os.mkdir(f'{self.path}/{sub_tag}')
        os.mkdir(f'{self.path}/{sub_tag}/hkls')

        shutil.copyfile(f'{recipe}', f'{self.path}/{sub_tag}/recipe_{self.tag}_{sub_tag}.txt')


        if sphv_init is not None:
            self.sphv_iter = sphv_init.copy()
        else:
            self.sphv_iter = self.sphv_base.copy()
            self.sphv_iter.vol = np.random.random(self.sphv_iter.vol.shape)




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

                _,_, step = scheme(**kwargs)
                count +=1

                self.sphv_iter.save(f'{self.path}/{sub_tag}/sphv_{self.tag}_{sub_tag}_final.dbin')

                self.integrate_final(sub_tag)

                cif_integrated = CifData(f'{self.path}/{sub_tag}/{self.tag}_{sub_tag}_final-sf.cif', rotk=self.rotk, rottheta=self.rottheta)
                cif_integrated.scat_bragg[:,-1] /=np.max(cif_integrated.scat_bragg[:,-1])
                cif_integrated.scat_bragg[:,-1] *=1000
                cif_integrated.save_hkl(f'{self.path}/{sub_tag}/hkls/{self.tag}_{sub_tag}_count_{count}.hkl')









        self.sphv_iter.save(f'{self.path}/{sub_tag}/sphv_{self.tag}_{sub_tag}_final.dbin')








