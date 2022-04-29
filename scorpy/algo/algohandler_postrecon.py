





import os
import shutil


import CifFile as pycif



from ..read.cifs.cifdata import CifData
from ..vols.sphv.sphericalvol import SphericalVol
import matplotlib.pyplot as plt
import numpy as np

from ..utils.utils import strerr2floaterrr, verbose_dec
import time




class AlgoHandlerPostRecon:





    def run_shelx(self, sub_tag, count=None, skip_targ=True):

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



    def get_intensity(self, sub_tag, count=None, loc=None):

        cif_targ = CifData(self.cif_targ_path(), rotk=self.rotk, rottheta= self.rottheta)
        cif_final = CifData(self.cif_final_path(sub_tag), rotk=self.rotk, rottheta= self.rottheta)

        if count is not None:
            cif_final.fill_from_hkl(self.hkl_count_path(sub_tag, count=count), qmax=self.qmax)




        if loc is None:
            loc = self.get_targ_final_scat_eq_loc(sub_tag)

        It = cif_targ.scat_bragg[:,-1]

        If = cif_final.scat_bragg[loc, -1]




        return It, If


    def get_targ_final_scat_eq_loc(self, sub_tag):

        cif_targ = CifData(self.cif_targ_path(), rotk=self.rotk, rottheta= self.rottheta)
        cif_final = CifData(self.cif_final_path(sub_tag), rotk=self.rotk, rottheta= self.rottheta)


        loc = np.zeros(cif_targ.scat_bragg.shape[0])


        for i, hkli_targ in enumerate(cif_targ.scat_bragg):
            bragg_loc =np.where( (cif_final.scat_bragg[:,:-1]==hkli_targ[:-1]).all(axis=1))[0][0]
            loc[i] = bragg_loc

        return loc.astype(int)








    def get_geometry_vals(self, sub_tag, count=None, geometry='distances'):


        assert geometry =='distances' or 'angles', 'geometry must be "distances" or "angles"'

        if count is None:
            cif = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}.cif')
        elif count == 'targ':
            cif =  pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_targ.cif')
        else:
            cif = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}_count_{count}.cif')

        if geometry=='angles':
            key = '_geom_angles'
        else:
            key = '_geom_bond_distance'

        vk = cif.visible_keys[0]
        x = dict(cif[vk])[key]
        vals, errs = np.zeros(len(x)), np.zeros(len(x))

        for i, xi in enumerate(x):
            val, err = strerr2floaterrr(xi)

            vals[i] = val
            errs[i] = err

        return vals, errs



    def get_shelx_rf(self, sub_tag, count=None):

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


    def get_inten_rf(self, sub_tag, count=None, loc=None):


        It, If = self.get_intensity(sub_tag, count=count, loc=loc)

        It /=np.sum(It)
        If /=np.sum(If)

        rf = np.sum(np.abs(It - If))/np.sum(np.abs(If))

        return rf




    @verbose_dec
    def save_rfs(self, sub_tag, verbose=0):
        print(f'Saving R factors: {self.tag} {sub_tag}')
        print(f'Started: {time.asctime()}')


        ncounts = len(os.listdir(self.hkls_path(sub_tag)))
        loc = self.get_targ_final_scat_eq_loc(sub_tag)

        rfs_shelx = np.zeros(ncounts)
        rfs_inten = np.zeros(ncounts)

        for count in range(ncounts):
            print(count, end='\r')
            rf_shelx = self.get_shelx_rf(sub_tag, count=count)
            rf_inten = self.get_inten_rf(sub_tag, count=count, loc=loc)
            rfs_shelx[count] = rf_shelx
            rfs_inten[count] = rf_inten

        np.save(self.rfs_shelx_path(sub_tag), rfs_shelx)
        np.save(self.rfs_inten_path(sub_tag), rfs_inten)


        print(f'Finished: {time.asctime()}')






























    # def get_bond_distances(self, sub_tag, count=None):

        # if count is None:
            # cif = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}.cif')
        # elif count == 'targ':
            # cif =  pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_targ.cif')
        # else:
            # cif = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}_count_{count}.cif')


        # vk = cif.visible_keys[0]
        
        # bond_distances= dict(cif[vk])['_geom_bond_distance']

        # vals, errs = np.zeros(len(bond_distances)), np.zeros(len(bond_distances))


        # for i, bond_d in enumerate(bond_distances):
            # val, err = strerr2floaterrr(bond_d)



            # vals[i] = val
            # errs[i] = err

        # return vals, errs

