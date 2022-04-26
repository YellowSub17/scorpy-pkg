





import os
import shutil


import CifFile as pycif



from ..read.cifs.cifdata import CifData
from ..vols.sphv.sphericalvol import SphericalVol
import matplotlib.pyplot as plt
import numpy as np

from ..utils.utils import strerr2floaterrr




class AlgoHandlerPostRecon:





    def run_shelxl(self, sub_tag, count=None, skip_targ=True):

        ##make shelx folder
        if not os.path.exists(f'{self.path}/{sub_tag}/shelx/'):
            os.mkdir(f'{self.path}/{sub_tag}/shelx/')



        if count is None:
            shutil.copyfile(f'{self.hkl_count_path(sub_tag)}', f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}.hkl')
            shutil.copyfile(f'{self.path}/{self.tag}.ins', f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}.ins')
        elif count=='targ':
            cif_targ = CifData(self.cif_targ_path(), rotk=self.rotk, rottheta= self.rottheta)
            cif_targ.save_hkl(f'{self.path}/{sub_tag}/shelx/{self.tag}_targ.hkl')
            shutil.copyfile(f'{self.path}/{self.tag}.ins', f'{self.path}/{sub_tag}/shelx/{self.tag}_targ.ins')

        elif count >= 0:
            shutil.copyfile(f'{self.path}/{self.tag}.ins', f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}_count_{count}.ins')
            shutil.copyfile(f'{self.hkl_count_path(sub_tag, count)}', f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}_count_{count}.hkl')




        cwd = os.getcwd()
        os.chdir(f'{self.path}/{sub_tag}/shelx/')
        if count is None:
            os.system(f'shelxl {self.tag}_{sub_tag} > shelxl.log')
        elif count=='targ':
            os.system(f'shelxl {self.tag}_targ > shelxl.log')
        else:
            os.system(f'shelxl {self.tag}_{sub_tag}_count_{count} > shelxl.log')

        os.chdir(f'{cwd}')



    def get_intensity(self, sub_tag, count=None):

        cif_targ = CifData(self.cif_targ_path(), rotk=self.rotk, rottheta= self.rottheta)
        cif_final = CifData(self.cif_final_path(sub_tag), rotk=self.rotk, rottheta= self.rottheta)

        if count is not None:
            cif_final.fill_from_hkl(self.hkl_count_path(sub_tag, count=count))


        It = np.zeros(cif_targ.scat_bragg.shape[0])
        If = np.zeros(cif_targ.scat_bragg.shape[0])



        for i, hkli_targ in enumerate(cif_targ.scat_bragg):
            It[i] = hkli_targ[-1]
            bragg_loc =np.where( (cif_final.scat_bragg[:,:-1]==hkli_targ[:-1]).all(axis=1))[0]

            if bragg_loc.shape[0]>0:
                If[i] = cif_final.scat_bragg[bragg_loc, -1]

        return It, If




    def get_bond_distances(self, sub_tag, count=None):

        if count is None:
            cif = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}.cif')
        elif count == 'targ':
            cif =  pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_targ.cif')
        else:
            cif = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}_count_{count}.cif')


        vk = cif.visible_keys[0]
        
        bond_distances= dict(cif[vk])['_geom_bond_distance']

        vals, errs = np.zeros(len(bond_distances)), np.zeros(len(bond_distances))


        for i, bond_d in enumerate(bond_distances):
            val, err = strerr2floaterrr(bond_d)



            vals[i] = val
            errs[i] = err

        return vals, errs



    def get_bond_angles(self, sub_tag, count=None):

        if count is None:
            cif = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}.cif')
        elif count == 'targ':
            cif =  pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_targ.cif')
        else:
            cif = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}_count_{count}.cif')


        vk = cif.visible_keys[0]
        
        bond_angles = dict(cif[vk])['_geom_angles']

        vals, errs = np.zeros(len(bond_angles)), np.zeros(len(bond_angles))


        for i, bond_a in enumerate(bond_angels):
            val, err = strerr2floaterrr(bond_a)



            vals[i] = val
            errs[i] = err

        return vals, errs



    def get_rf(self, sub_tag, count=None):

        if count is None:
            cif = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}.cif')
        elif count == 'targ':
            cif =  pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_targ.cif')
        else:
            cif = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}_count_{count}.cif')


        vk = cif.visible_keys[0]

        # _refine_ls_r_factor_all, _refine_ls_wr_factor_ref, _refine_ls_wr_factor_gt
        rf = dict(cif[vk])['_refine_ls_r_factor_all']

        return float(rf)






















