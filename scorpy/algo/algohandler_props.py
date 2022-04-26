


from ..vols.sphv.sphericalvol import SphericalVol
from ..vols.blqq.blqqvol import BlqqVol
import os


class AlgoHandlerProps:



    def sphv_supp_tight_path(self):
        return f'{self.path}/sphv_{self.tag}_supp_tight.dbin'

    def sphv_supp_loose_path(self):
        return f'{self.path}/sphv_{self.tag}_supp_loose.dbin'

    def sphv_targ_path(self):
        return f'{self.path}/sphv_{self.tag}_targ.dbin'

    def blqq_data_path(self):
        return f'{self.path}/blqq_{self.tag}_data.dbin'

    def cif_targ_path(self):
        return f'{self.path}/{self.tag}_targ-sf.cif'





    def sphv_init_path(self, sub_tag):
        return f'{self.path}/{sub_tag}/sphv_{self.tag}_{sub_tag}_init.dbin'


    def sphv_iter_path(self, sub_tag):
        return f'{self.path}/{sub_tag}/sphv_{self.tag}_{sub_tag}_iter.dbin'

    def cif_final_path(self, sub_tag):
        return f'{self.path}/{sub_tag}/{self.tag}_{sub_tag}_final-sf.cif'

    def sphv_final_path(self, sub_tag):
        return f'{self.path}/{sub_tag}/sphv_{self.tag}_{sub_tag}_final.dbin'

    def hkl_count_path(self, sub_tag, count=-1):
        if count is None:
            count = len(os.listdir(f'{self.path}/{sub_tag}/hkls/'))
        elif count<0:
            count = len(os.listdir(f'{self.path}/{sub_tag}/hkls/')) + count
        return f'{self.path}/{sub_tag}/hkls/{self.tag}_{sub_tag}_count_{count}.hkl'







