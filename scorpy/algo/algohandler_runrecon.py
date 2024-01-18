


import numpy as np
import os
import shutil
import timeit
import time


from ..read.cifs.cifdata import CifData

from ..vols.sphv.sphericalvol import SphericalVol
from ..vols.corr.correlationvol import CorrelationVol
from ..vols.blqq.blqqvol import BlqqVol
from ..iqlm.iqlmhandler import IqlmHandler

from ..utils.decorator_funcs import verbose_dec



class AlgoHandlerRunRecon:


    @verbose_dec
    def check_inputs(self, verbose=0):
        print(f'Checking Inputs')

        blqq_check1 = os.path.exists(self.blqq_data_path()+'.npy')
        blqq_check2 = os.path.exists(self.blqq_data_path()+'.dbin')
        assert blqq_check1 or blqq_check2, "Data BlqqVol not saved to algo folder"
        blqq = BlqqVol(path=self.blqq_data_path())


        supp_check1 = os.path.exists(self.sphv_supp_loose_path()+'.npy')
        supp_check2 = os.path.exists(self.sphv_supp_loose_path()+'.dbin')
        assert supp_check1 or supp_check2, "Loose support SphericalVol not saved to algo folder"
        sphv_supp_l = SphericalVol(path=self.sphv_supp_loose_path())


        supp_check1 = os.path.exists(self.sphv_supp_tight_path()+'.npy')
        supp_check2 = os.path.exists(self.sphv_supp_tight_path()+'.dbin')
        assert supp_check1 or supp_check2, "Tight support SphericalVol not saved to algo folder"
        sphv_supp_t = SphericalVol(path=self.sphv_supp_tight_path())

        assert sphv_supp_t.vol.shape == sphv_supp_l.vol.shape, 'Tight and loose supports are different shapes'

        assert blqq.nq == sphv_supp_l.nq == self.nq
        assert blqq.qmax == sphv_supp_l.qmax == self.qmax
        assert blqq.qmin == sphv_supp_l.qmin == self.qmin
        assert blqq.nl*2 == sphv_supp_l.ntheta
        assert blqq.nl*4 == sphv_supp_l.nphi
        assert self.nl == blqq.nl


        print(f'Blqq and Sphv Supports passed checks.')




    @verbose_dec
    def load_inputs(self, verbose=0):
        print('Loading eigenvector/value and support inputs.')


        blqq = BlqqVol(path=self.blqq_data_path())
        # save eigens
        self.lams, self.us = blqq.get_eig()
        eigs_thresh = np.max(self.lams, axis=0)*self.eig_rcond
        for l_ind, eig_thresh in enumerate(eigs_thresh):
            loc = np.where(np.abs(self.lams[:,l_ind]) < eig_thresh)
            self.lams[loc, l_ind] = 0
            loc = np.where(self.lams[:,l_ind] ==0)
            self.us[:, loc, l_ind] = 0

        sphv_supp = SphericalVol(path=self.sphv_supp_loose_path())
        # save support
        self.supp_loc = np.where(sphv_supp.vol != 0 )
        self.supp_notloc = np.where(sphv_supp.vol == 0 )
        
        print(f'Done Loading.')


    @verbose_dec
    def run_recon(self, sub_tag, recipe, sphv_init=None, overwrite=0, verbose=0):




        if not os.path.exists(f'{self.path}/{sub_tag}'):
            print('Creating new sub_tag folder.')

            os.mkdir(f'{self.path}/{sub_tag}')
            os.mkdir(f'{self.path}/{sub_tag}/hkls')

        elif os.path.exists(f'{self.path}/{sub_tag}') and overwrite==2:

            print('Overwriting sub_tag folder.')
            shutil.rmtree(f'{self.path}/{sub_tag}')
            os.mkdir(f'{self.path}/{sub_tag}')
            os.mkdir(f'{self.path}/{sub_tag}/hkls')

        elif os.path.exists(f'{self.path}/{sub_tag}') and overwrite==1:
            print(f'Algo path {self.path}/{sub_tag} exists. Overwrite? (y/n)')
            query = input('>> ')
            if query=='y':
                print('Overwriting sub_tag folder.')
                shutil.rmtree(f'{self.path}/{sub_tag}')
                os.mkdir(f'{self.path}/{sub_tag}')
                os.mkdir(f'{self.path}/{sub_tag}/hkls')

            else:
                print(f'Subtag {sub_tag} exists. Cancelling run.')
                return

        else:
            print(f'Subtag {sub_tag} exists. Cancelling run.')
            return




        shutil.copyfile(f'{recipe}', self.recipe_path(sub_tag))


        if sphv_init is not None:
            self.sphv_iter = sphv_init.copy()
        else:
            self.sphv_iter = self.sphv_base
            self.sphv_iter.vol = 2*np.random.random(self.sphv_iter.vol.shape)-1
            # self.sphv_iter.vol = np.random.random(self.sphv_iter.vol.shape)


        self.sphv_iter.save(self.sphv_init_path(sub_tag))


        print('Saved recipe and sphv_init to sub_tag folder.')



        print(f'Running Recon {self.tag}_{sub_tag}')
        print(f'Started: {time.asctime()}'),[]

        recipe_file = open(self.recipe_path(sub_tag))
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

                # print('a')
                # t1 = time.time()
                self.sphv_iter.save(self.sphv_iter_path(sub_tag))
                # t2 = time.time()
                # print(t2-t1)

                # print('b')
                # t1 = time.time()
                self.integrate_iter(sub_tag)
                # t2 = time.time()
                # print(t2-t1)

                # print('c')
                # t1 = time.time()
                _,_, step = scheme(**kwargs)
                # t2 = time.time()
                # print(t2-t1)
                count +=1

        self.sphv_iter.save(self.sphv_iter_path(sub_tag))
        self.integrate_iter(sub_tag)

        print(f'Finished: {time.asctime()}')










    def integrate_iter(self,sub_tag):

        sphv_supp_tight = SphericalVol(path=self.sphv_supp_tight_path())
        sphv_integrated = SphericalVol(path=self.sphv_iter_path(sub_tag))
        sphv_integrated.integrate_bragg_peaks(sphv_supp_tight, self.dxsupp)
        sphv_integrated.save(self.sphv_final_path(sub_tag))

        cif_integrated = CifData(path=self.cif_supp_path(), rotk=self.rotk, rottheta=self.rottheta)
        cif_integrated.fill_from_sphv(sphv_integrated)
        cif_integrated.save(self.cif_final_path(sub_tag))
        cif_integrated.save_shelx_hkl(self.hkl_count_path(sub_tag, count=None))






