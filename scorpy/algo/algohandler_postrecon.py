





import os



from ..read.cifs.cifdata import CifData
import numpy as np

from ..utils.decorator_funcs import verbose_dec




class AlgoHandlerPostRecon:



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


        return It, If










    def get_targ_final_scat_eq_loc(self, sub_tag):

        cif_targ = CifData(self.cif_targ_path(), rotk=self.rotk, rottheta= self.rottheta)
        cif_final = CifData(self.cif_final_path(sub_tag), rotk=self.rotk, rottheta= self.rottheta)


        loc = np.zeros(cif_targ.scat_bragg.shape[0])


        for i, hkli_targ in enumerate(cif_targ.scat_bragg):
            bragg_loc =np.where( (cif_final.scat_bragg[:,:-1]==hkli_targ[:-1]).all(axis=1))[0][0]
            loc[i] = bragg_loc

        return loc.astype(int)







    def get_inten_rf(self, sub_tag, count=None):


        It, If = self.get_intensity(sub_tag, count=count)

        It /=np.sum(It)
        If /=np.sum(If)

        rf = np.sum(np.abs(It - If))/np.sum(np.abs(If))

        return rf



    def get_It_If_loc(self, sub_tag):

        #it is missing some intensities
        It_cif = CifData(self.cif_targ_path())
        #if has too many brag peaks
        If_hkli = np.genfromtxt(self.hkl_count_path(sub_tag, count=0),delimiter=(4,4,4,8), skip_footer=1, usecols=(0,1,2,3))

        loc = np.zeros(It_cif.scat_bragg.shape[0])
        print(f'checking for missing bragg points ({It_cif.scat_bragg.shape[0]})')
        for i, (h, k, l, I) in enumerate(It_cif.scat_bragg):
            print(f'{i}', end='\r')
            bragg_loc =np.where( (If_hkli[:,:-1]==[h,k,l]).all(axis=1))[0][0]
            loc[i] = bragg_loc
        print()
        print('Done')

        #an array that 
        loc = loc.astype(int)
         
        return loc


    @verbose_dec
    def get_inten_quick(self, sub_tag, counts, loc=None, verbose=0):


        # #it is missing some intensities
        # It_cif = CifData(self.cif_targ_path())
        #if has too many brag peaks
        If_hkli = np.genfromtxt(self.hkl_count_path(sub_tag, count=0),delimiter=(4,4,4,8), skip_footer=1, usecols=(0,1,2,3))

        if loc is None:
            print('loc is none, gettting loc')
            loc = self.get_It_If_loc(sub_tag)

        intens = np.zeros((len(counts), loc.shape[0]))   

        # It = It_cif.scat_bragg[:,-1]
        # It /=np.sum(It)
        for i, count in enumerate(counts):
            print(i)

            If = np.genfromtxt(self.hkl_count_path(sub_tag, count=count),delimiter=(4, 4, 4, 8 ), skip_footer=1, usecols=3)

            If = If[loc]


            intens[i] = If

        return intens



    def get_targ_inten(self):
        It_cif = CifData(self.cif_targ_path())
        It = It_cif.scat_bragg[:,-1]
        return It


    def get_inten_rfs_quick(self, sub_tag, n, loc=None, It=None):

        #it is missing some intensities
        If_hkli = np.genfromtxt(self.hkl_count_path(sub_tag, count=0),delimiter=(4,4,4,8), skip_footer=1, usecols=(0,1,2,3))

        if loc is None:

            loc = self.get_It_If_loc(sub_tag)




        rfs = np.zeros(n)   
        if It is None:
            It_cif = CifData(self.cif_targ_path())
            It = It_cif.scat_bragg[:,-1]

        It /=np.sum(It)
        for i in range(n):
            print(i)

            If = np.genfromtxt(self.hkl_count_path(sub_tag, count=i),delimiter=(4, 4, 4, 8 ), skip_footer=1, usecols=3)

            If = If[loc]

            If /=np.sum(If)

            rf = np.sum(np.abs(It - If))/np.sum(np.abs(If))
            rfs[i] = rf

        return rfs



            











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





