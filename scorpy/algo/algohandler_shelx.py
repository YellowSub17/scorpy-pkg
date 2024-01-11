



import numpy as np
import CifFile as pycif
import shutil
import os
from ..read.cifs.cifdata import CifData
from ..utils.str_funcs import strerr2floaterrr 




class AlgoHandlerShelx:




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




    def get_geometry_vals(self, sub_tag, count=None, geometry='distances'):


        assert geometry =='distances' or 'angles', 'geometry must be "distances" or "angles"'

        if count is None:
            cif = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}.cif')
        elif count == 'targ':
            cif =  pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_targ.cif')
        else:
            cif = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}_count_{count}.cif')

        if geometry=='angles':
            key = '_geom_angle'
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


    def get_xyzs(self, sub_tag, count=None):

        if count is None:
            cif = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}.cif')
        elif count == 'targ':
            cif =  pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_targ.cif')
        else:
            cif = pycif.ReadCif(f'{self.path}/{sub_tag}/shelx/{self.tag}_{sub_tag}_count_{count}.cif')

        vk = cif.visible_keys[0]

        a = strerr2floaterrr(dict(cif[vk])['_cell_length_a'])[0]
        b = strerr2floaterrr(dict(cif[vk])['_cell_length_a'])[0]
        c = strerr2floaterrr(dict(cif[vk])['_cell_length_b'])[0]

        xstrs = dict(cif[vk])['_atom_site_fract_x']
        ystrs = dict(cif[vk])['_atom_site_fract_y']
        zstrs = dict(cif[vk])['_atom_site_fract_z']

        xyzs = np.zeros( (len(xstrs), 3))

        for i, (fracx, fracy, fracz) in enumerate( zip(xstrs, ystrs, zstrs)):
            x = strerr2floaterrr(fracx)[0]*a
            y = strerr2floaterrr(fracy)[0]*b
            z = strerr2floaterrr(fracz)[0]*c

            xyzs[i, :] =   [x,y,z]

        return xyzs










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





