



import CifFile as pycif
import numpy as np
from ...utils.decorator_funcs import verbose_dec

class CifDataSaveLoad:

    @verbose_dec
    def save(self, path, verbose=0):

        cif = pycif.CifFile()
        block = pycif.CifBlock()
        cif['block'] = block
        cif['block']['_symmetry.space_group_name_h-m'] = f'{self.spg}'
        cif['block']['_cell.angle_alpha'] = np.degrees(self.alpha)
        cif['block']['_cell.angle_beta'] = np.degrees(self.beta)
        cif['block']['_cell.angle_gamma'] = np.degrees(self.gamma)
        cif['block']['_cell.length_a'] = self.a_mag
        cif['block']['_cell.length_b'] = self.b_mag
        cif['block']['_cell.length_c'] = self.c_mag

        cif['block']['_refln.index_h'] = self.scat_bragg[:,0]
        cif['block']['_refln.index_k'] = self.scat_bragg[:,1]
        cif['block']['_refln.index_l'] = self.scat_bragg[:,2]
        cif['block']['_refln.intensity_meas'] = self.scat_bragg[:,3]
        cif['block'].CreateLoop( ['_refln.index_h', '_refln.index_k', '_refln.index_l', '_refln.intensity_meas'] )

        outfile = open(path, 'w')
        outfile.write(cif.WriteOut())
        outfile.close()



    def save_shelx_hkl(self, path):

        self.scat_bragg[:,-1] /=np.max(self.scat_bragg[:,-1])
        self.scat_bragg[:,-1] *=9999.99
        f = open(path, 'w')
        for bragg_pt in self.scat_bragg:

            line = '%4d%4d%4d%8.2f%8.2f\n' % (round(bragg_pt[0]), round(bragg_pt[1]), round(bragg_pt[2]), bragg_pt[3], 0)

            f.write(line)
        f.write('   0   0   0       0       0       0       0')
        f.close()


    def save_crystfel_hkl(self, path):

        f = open(path, 'w')

        f.write('CrystFEL reflection list version 2.0\n')
        f.write('Symmetry: 1\n')
        f.write('\th\tk\tl\tI\tphase\tsigma(I)\tnmeas\n')


        for bragg_pt in self.scat_bragg:

            line = f'\t{int(bragg_pt[0])}\t{int(bragg_pt[1])}\t{int(bragg_pt[2])}\t{round(bragg_pt[3],16)}\t-\t0.0\t1\n'


            f.write(line)
        f.write('End of reflections')
        f.close()





