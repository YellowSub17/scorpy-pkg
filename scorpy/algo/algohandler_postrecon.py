





import os



from ..read.cifs.cifdata import CifData
import numpy as np

from ..utils.decorator_funcs import verbose_dec




class AlgoHandlerPostRecon:


    def get_target_nnanloc(self):
        cif_targ = CifData(path=self.cif_targ_path())
        nnanloc = np.where(np.logical_not(np.isnan(cif_targ.scat_bragg[:,-1])))
        return nnanloc


    def get_target_cif_intensity(self, norm=True):
        cif_targ = CifData(path=self.cif_targ_path())
        sf = np.nansum(cif_targ.scat_bragg[:,-1]) if norm else 1
        return cif_targ.scat_bragg[:,-1]*sf

    def get_final_cif_intensity(self, sub_tag, norm=True):
        cif_final = CifData(path=self.cif_final_path(sub_tag))
        sf = np.nansum(cif_final.scat_bragg[:,-1]) if norm else 1
        return cif_final.scat_bragg[:,-1]*sf

    def get_target_hkl_intensity(self, norm=True):

        x = np.fromfile(self.hkl_targ_path(), dtype=float, count=-1, sep=' ')[:-7]
        hklI = x.reshape(int(x.shape[0]/5), 5)

        sf = np.nansum(hklI[:,-2]) if norm else 1
        return hklI[:,-2]*sf


    def get_count_hkl_intensity(self,sub_tag, count, norm=True):

        hkl_file= self.hkl_count_path(sub_tag, count)
        x = np.fromfile(hkl_file, dtype=float, count=-1, sep=' ')[:-7]
        hklI = x.reshape(int(x.shape[0]/5), 5)

        sf = np.nansum(hklI[:,-2]) if norm else 1
        return hklI[:,-2]*sf



    def calc_rfs(self, sub_tag, counts):

        targ_inten = self.get_target_hkl_intensity(norm=False)

        rfs = np.zeros(len(counts))
        for i, count in enumerate(counts):
            count_inten = self.get_count_hkl_intensity(sub_tag, count, norm=False)
            rf = np.nansum(np.abs(targ_inten - count_inten))/np.nansum(np.abs(count_inten))
            rfs[i] = rf
        return rfs

            

    # rfs[:, i] = np.sum(np.abs(Its - Ifs), axis=-1) /np.sum( np.abs(Ifs), axis=-1 )







