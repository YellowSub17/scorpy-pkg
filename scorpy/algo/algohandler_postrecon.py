





import os
import shutil


import CifFile as pycif



from ..read.cifs.cifdata import CifData
from ..vols.sphv.sphericalvol import SphericalVol
import matplotlib.pyplot as plt
import numpy as np




class AlgoHandlerPostRecon:




    def rfactors(self, sub_tag):
        pass


    def intensity_xy_plot(self, sub_tag, count=None):


        cif_targ = CifData(f'{self.path}/{self.tag}_targ-sf.cif', rotk=self.rotk, rottheta= self.rottheta)
        cif_final = CifData(f'{self.path}/{sub_tag}/{self.tag}_{sub_tag}_final-sf.cif', rotk=self.rotk, rottheta= self.rottheta)

        if count is not None:
            cif_final.fill_from_hkl(f'{self.path}/{sub_tag}/hkl/{self.tag}_{sub_tag}_count_{count}.hkl')


        It = []
        If = []



        for hkli_targ in cif_targ.scat_bragg:
            It.append(hkli_targ[-1])
            bragg_loc =np.where( (cif_final.scat_bragg[:,:-1]==hkli_targ[:-1]).all(axis=1))[0]

            if bragg_loc.shape[0]>0:
                If.append(cif_final.scat_bragg[bragg_loc, -1])




        plt.figure()
        plt.scatter(It/np.sum(It), If/np.sum(If))

        plt.plot([0, np.max(It)/np.sum(It)],[0, np.max(It)/np.sum(It)])






    def integrate_final(self,sub_tag):

        sphv_supp_tight = SphericalVol(path=f'{self.path}/sphv_{self.tag}_supp_tight.dbin')

        sphv_integrated = SphericalVol(path=f'{self.path}/{sub_tag}/sphv_{self.tag}_{sub_tag}_final.dbin')
        sphv_integrated.integrate_peaks(sphv_supp_tight, self.dxsupp)
        sphv_integrated.save(f'{self.path}/{sub_tag}/sphv_{self.tag}_{sub_tag}_final_integrated.dbin')


        cif_integrated = CifData(f'{self.path}/{self.tag}_targ-sf.cif', rotk=self.rotk, rottheta=self.rottheta)

        cif_integrated.fill_from_sphv(sphv_integrated)
        cif_integrated.save(f'{self.path}/{sub_tag}/{self.tag}_{sub_tag}_final-sf.cif')














    def prep_shelxl(self, sub_tag, count=None):


        cif_targ = CifData(f'{self.path}/{self.tag}_targ-sf.cif', rotk=self.rotk, rottheta= self.rottheta)
        cif_targ.save_hkl(f'{self.path}/{sub_tag}/shelx/{self.tag}_targ.hkl')

        cif_integrated = CifData(f'{self.path}/{sub_tag}/{self.tag}_{sub_tag}_final-sf.cif', rotk=self.rotk, rottheta=self.rottheta)
        shutil.copyfile(f'{self.path}/{self.tag}.ins', f'{self.path}/{sub_tag}/shelx/{self.tag}_targ.ins')

        if count is not None:
            shutil.copyfile(f'{self.path}/{self.tag}.ins', f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}_count_{count}.ins')
            cif_integrated.fill_from_hkl(f'{self.path}/{sub_tag}/hkl/{self.tag}_{sub_tag}_count_{count}.hkl')
            cif_integrated.save_hkl(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}_count_{count}.hkl')
        else:
            shutil.copyfile(f'{self.path}/{self.tag}.ins', f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}.ins')
            cif_integrated.scat_bragg[:,-1] /=np.max(cif_integrated.scat_bragg[:,-1])
            cif_integrated.scat_bragg[:,-1] *=1000
            cif_integrated.save_hkl(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}.hkl')





    def bond_distance_xy_plot(self,sub_tag):

        cif_targ = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_targ.cif')
        cif_algo = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}.cif')

        vk_targ = cif_targ.visible_keys[0]
        vk_algo = cif_algo.visible_keys[0]
        
        targ_vals, targ_errs = [], []
        algo_vals, algo_errs = [], []


        for bond_distance in dict(cif_targ[vk_targ])['_geom_bond_distance']:

            val, err = bond_distance.split('(')[0], bond_distance.split('(')[1][:-1]
            ndeci = len(val.split('.')[1])
            err = float('0.'+(ndeci-1)*'0'+'1')*float(err)
            targ_vals.append(float(val))
            targ_errs.append(err)

        for bond_distance in dict(cif_algo[vk_algo])['_geom_bond_distance']:

            val, err = bond_distance.split('(')[0], bond_distance.split('(')[1][:-1]
            ndeci = len(val.split('.')[1])
            err = float('0.'+(ndeci-1)*'0'+'1')*float(err)
            algo_vals.append(float(val))
            algo_errs.append(err)

        plt.figure()
        plt.errorbar(targ_vals, algo_vals,xerr=targ_errs, yerr=algo_errs, fmt='b.')
        plt.plot([np.min(targ_vals), np.max(targ_vals)], [np.min(targ_vals), np.max(targ_vals)], 'b-')
        plt.xlabel('bond dist target')
        plt.ylabel('bond dist algo')





    # def bond_angle_xy_plot(self,sub_tag):

        # cif_targ = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_targ.cif')
        # cif_algo = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}.cif')

        # vk_targ = cif_targ.visible_keys[0]
        # vk_algo = cif_algo.visible_keys[0]
        
        # targ_vals, targ_errs = [], []
        # algo_vals, algo_errs = [], []


        # for bond_distance in dict(cif_targ[vk_targ])['_geom_angle']:

            # val, err = bond_distance.split('(')[0], bond_distance.split('(')[1][:-1]
            # ndeci = len(val.split('.')[1])
            # err = float('0.'+(ndeci-1)*'0'+'1')*float(err)
            # targ_vals.append(float(val))
            # targ_errs.append(err)

        # for bond_distance in dict(cif_algo[vk_algo])['_geom_angle']:

            # val, err = bond_distance.split('(')[0], bond_distance.split('(')[1][:-1]
            # ndeci = len(val.split('.')[1])
            # err = float('0.'+(ndeci-1)*'0'+'1')*float(err)
            # algo_vals.append(float(val))
            # algo_errs.append(err)

        # plt.figure()
        # plt.errorbar(targ_vals, algo_vals,xerr=targ_errs, yerr=algo_errs, fmt='b.')
        # plt.plot([np.min(targ_vals), np.max(targ_vals)], [np.min(targ_vals), np.max(targ_vals)], 'b-')


























