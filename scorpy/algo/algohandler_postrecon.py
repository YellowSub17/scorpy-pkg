





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

#     @verbose_dec
    # def get_intensity(self, sub_tag, count=None, z=None, n_scats=10000, verbose=0):

        # print('## algo.get_intensity: Getting target cif')
        # cif_targ = CifData(self.cif_targ_path(), rotk=self.rotk, rottheta= self.rottheta)
        # print('## algo.get_intensity: Getting final cif')
        # cif_final = CifData(self.cif_final_path(sub_tag), rotk=self.rotk, rottheta= self.rottheta)

        # if count is not None:
            # print('## algo.get_intensity: filling hkl')
            # cif_final.fill_from_hkl(self.hkl_count_path(sub_tag, count=count), qmax=self.qmax)


        # if n_scats==-1 or n_scats >cif_targ.scat_bragg.shape[0]:
            # n_scats = cif_targ.scat_bragg.shape[0]
        # loc = np.zeros(n_scats)

        # scats = list(cif_targ.scat_bragg)
        # np.random.shuffle(scats)


        # print('## algo.get_intensity: Finding bragg points')
        # for i, (h, k, l, I) in enumerate(scats[:n_scats]):
            # print(f'{i}/{n_scats}', end='\r')
            # bragg_loc =np.where( (cif_final.scat_bragg[:,:-1]==[h,k,l]).all(axis=1))[0][0]
            # loc[i] = bragg_loc
        # loc = loc.astype(int)

        # It = np.array(scats[:n_scats])[:,-1]
        # If = cif_final.scat_bragg[loc, -1]


        # if z=='q':
            # z = cif_final.scat_sph[loc,0]
        # elif z=='theta':
            # z = cif_final.scat_sph[loc,1]
        # elif z=='phi':
            # z = cif_final.scat_sph[loc,2]

        # return It, If, z

    @verbose_dec
    def get_intensity(self, sub_tag, count=None, n_scats=-1, verbose=0):

        print('## algo.get_intensity: Getting target cif')
        cif_targ = CifData(self.cif_targ_path(), rotk=self.rotk, rottheta= self.rottheta)
        print('## algo.get_intensity: Getting final cif')
        cif_final = CifData(self.cif_final_path(sub_tag), rotk=self.rotk, rottheta= self.rottheta)

        if count is not None:
            print('## algo.get_intensity: filling hkl')
            cif_final.fill_from_hkl(self.hkl_count_path(sub_tag, count=count), qmax=self.qmax)


        if n_scats==-1 or n_scats >cif_targ.scat_bragg.shape[0]:
            n_scats = cif_targ.scat_bragg.shape[0]
        loc = np.zeros(n_scats)

        scats = list(cif_targ.scat_bragg)


        print('## algo.get_intensity: Finding bragg points')
        for i, (h, k, l, I) in enumerate(cif_targ.scat_bragg):
            # print(f'{i}/{n_scats}', end='\r')
            bragg_loc =np.where( (cif_final.scat_bragg[:,:-1]==[h,k,l]).all(axis=1))[0][0]
            loc[i] = bragg_loc
        loc = loc.astype(int)

        It = np.array(scats[:n_scats])[:,-1]
        If = cif_final.scat_bragg[loc, -1]

        # It = cif_targ.scat_bragg[:, -1]
        # If = cif_targ.scat_bragg[:, -1]




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


    def get_inten_rf(self, sub_tag, count=None, loc=None):


        It, If = self.get_intensity(sub_tag, count=count, loc=loc)

        It /=np.sum(It)
        If /=np.sum(If)

        rf = np.sum(np.abs(It - If))/np.sum(np.abs(If))

        return rf






    @verbose_dec
    def save_dxyzs(self, sub_tag, verbose=0):
        print(f'Saving dxyz: {self.tag} {sub_tag}')
        print(f'Started: {time.asctime()}')


        ncounts = len(os.listdir(self.hkls_path(sub_tag)))

        dxyzs = np.zeros(ncounts)
        mindxyzs = np.zeros(ncounts)
        maxdxyzs = np.zeros(ncounts)
        stddxyzs = np.zeros(ncounts)

        targ_xyz = self.get_xyzs(sub_tag, count='targ')



        for count in range(ncounts):

            print(count, end='\r')
            count_xyz = self.get_xyzs(sub_tag, count=count)

            count_dxyz =  np.abs( targ_xyz - count_xyz)

            count_dxyz_norm = np.linalg.norm(count_dxyz, axis=1)

            dxyzs[count] = np.mean(count_dxyz_norm)
            mindxyzs[count] = np.min(count_dxyz_norm)
            maxdxyzs[count] = np.max(count_dxyz_norm)
            stddxyzs[count] = np.std(count_dxyz_norm)

        np.save(self.mean_dxyzs_path(sub_tag), dxyzs)
        np.save(self.min_dxyzs_path(sub_tag), mindxyzs)
        np.save(self.max_dxyzs_path(sub_tag), maxdxyzs)
        np.save(self.std_dxyzs_path(sub_tag), stddxyzs)


        print(f'Finished: {time.asctime()}')


    @verbose_dec
    def save_dgeom(self, sub_tag,geometry='distances', verbose=0):
        print(f'Saving mean bond {geometry}: {self.tag} {sub_tag}')
        print(f'Started: {time.asctime()}')


        ncounts = len(os.listdir(self.hkls_path(sub_tag)))

        mean_geom = np.zeros(ncounts)
        min_geom = np.zeros(ncounts)
        max_geom = np.zeros(ncounts)
        std_geom = np.zeros(ncounts)

        targ_xs, targ_errs = self.get_geometry_vals(sub_tag, count='targ', geometry=geometry)




        for count in range(ncounts):

            print(count, end='\r')
            count_xs, count_errs = self.get_geometry_vals(sub_tag, count=count, geometry=geometry)


            count_dxs = np.abs(targ_xs- count_xs)
            mean_geom[count] = np.mean(count_dxs)
            min_geom[count] = np.min(count_dxs)
            max_geom[count] = np.max(count_dxs)
            std_geom[count] = np.std(count_dxs)



        if geometry=='distances':
            np.save(self.mean_bond_distances_path(sub_tag), mean_geom)
            np.save(self.min_bond_distances_path(sub_tag), min_geom)
            np.save(self.max_bond_distances_path(sub_tag), max_geom)
            np.save(self.std_bond_distances_path(sub_tag), std_geom)
        elif geometry=='angles':
            np.save(self.mean_bond_angles_path(sub_tag), mean_geom)
            np.save(self.min_bond_angles_path(sub_tag), min_geom)
            np.save(self.max_bond_angles_path(sub_tag), max_geom)
            np.save(self.std_bond_angles_path(sub_tag), std_geom)


        print(f'Finished: {time.asctime()}')




    @verbose_dec
    def save_rfs(self, sub_tag, verbose=0):
        print(f'Saving R factors: {self.tag} {sub_tag}')
        print(f'Started: {time.asctime()}')


        ncounts = len(os.listdir(self.hkls_path(sub_tag)))

        rfs_shelx = np.zeros(ncounts)

        for count in range(ncounts):
            print(count, end='\r')
            rf_shelx = self.get_shelx_rf(sub_tag, count=count)
            rfs_shelx[count] = rf_shelx

        np.save(self.rfs_shelx_path(sub_tag), rfs_shelx)


        print(f'Finished: {time.asctime()}')





