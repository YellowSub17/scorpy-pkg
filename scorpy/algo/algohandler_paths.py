


from ..vols.sphv.sphericalvol import SphericalVol
from ..vols.blqq.blqqvol import BlqqVol
import os



class AlgoHandlerPaths:

    def params_path(self):
        return self.path / f'algo_{self.tag}_params.txt'

    def sphv_supp_tight_path(self):
        return self.path / f'sphv_{self.tag}_supp_tight'

    def sphv_supp_loose_path(self):
        return self.path / f'sphv_{self.tag}_supp_loose'

    def sphv_targ_path(self):
        return self.path / f'sphv_{self.tag}_targ'

    def blqq_data_path(self):
        return self.path / f'blqq_{self.tag}_data'

    def corr_data_path(self):
        return self.path / f'corr_{self.tag}_data'

    def cif_targ_path(self):
        return self.path / f'{self.tag}_targ-sf.cif'





    def sphv_init_path(self, sub_tag):
        return self.path / f'{sub_tag}' / f'sphv_{self.tag}_{sub_tag}_init'

    def sphv_iter_path(self, sub_tag):
        return self.path / f'{sub_tag}' / f'sphv_{self.tag}_{sub_tag}_iter'

    def cif_final_path(self, sub_tag):
        return self.path / f'{sub_tag}' / f'{self.tag}_{sub_tag}_final-sf.cif'

    def sphv_final_path(self, sub_tag):
        return self.path / f'{sub_tag}' / f'sphv_{self.tag}_{sub_tag}_final'


    def hkls_path(self, sub_tag):
        return self.path / f'{sub_tag}' / 'hkls'
    def hkl_count_path(self, sub_tag, count=-1):
        if count is None:
            count = len(os.listdir(self.hkls_path(sub_tag)))
        elif count<0:
            count = len(os.listdir(self.hkls_path(sub_tag))) + count
        return self.hkls_path(sub_tag) / f'{self.tag}_{sub_tag}_count_{count}.hkl'






    def rfs_inten_path(self, sub_tag):
        return self.path / f'{sub_tag}' / f'{self.tag}_{sub_tag}_inten_rfs.npy'
    def rfs_shelx_path(self, sub_tag):
        return self.path / f'{sub_tag}' / 'shelx' / f'{self.tag}_{sub_tag}_shelx_rfs.npy'






    def mean_dxyzs_path(self, sub_tag):
        return self.path / f'{sub_tag}' / 'shelx' / f'{self.tag}_{sub_tag}_mean_dxyzs.npy'
    def min_dxyzs_path(self, sub_tag):
        return self.path / f'{sub_tag}' / 'shelx' / f'{self.tag}_{sub_tag}_min_dxyzs.npy'
    def max_dxyzs_path(self, sub_tag):
        return self.path / f'{sub_tag}' / 'shelx' / f'{self.tag}_{sub_tag}_max_dxyzs.npy'
    def std_dxyzs_path(self, sub_tag):
        return self.path / f'{sub_tag}' / 'shelx' / f'{self.tag}_{sub_tag}_std_dxyzs.npy'







    def mean_bond_distances_path(self, sub_tag):
        return self.path / f'{sub_tag}' / 'shelx' / f'{self.tag}_{sub_tag}_mean_bond_distances.npy'

    def max_bond_distances_path(self, sub_tag):
        return self.path / f'{sub_tag}' / 'shelx' / f'{self.tag}_{sub_tag}_max_bond_distances.npy'

    def min_bond_distances_path(self, sub_tag):
        return self.path / f'{sub_tag}' / 'shelx' / f'{self.tag}_{sub_tag}_min_bond_distances.npy'

    def std_bond_distances_path(self, sub_tag):
        return self.path / f'{sub_tag}' / 'shelx' / f'{self.tag}_{sub_tag}_std_bond_distances.npy'



    def mean_bond_angles_path(self, sub_tag):
        return self.path / f'{sub_tag}' / 'shelx' / f'{self.tag}_{sub_tag}_mean_bond_angles.npy'

    def max_bond_angles_path(self, sub_tag):
        return self.path / f'{sub_tag}' / 'shelx' / f'{self.tag}_{sub_tag}_max_bond_angles.npy'

    def min_bond_angles_path(self, sub_tag):
        return self.path / f'{sub_tag}' / 'shelx' / f'{self.tag}_{sub_tag}_min_bond_angles.npy'

    def std_bond_angles_path(self, sub_tag):
        return self.path / f'{sub_tag}' / 'shelx' / f'{self.tag}_{sub_tag}_std_bond_angles.npy'










