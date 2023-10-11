

import scorpy
import sys
import time




data_dir = '/home/ec2-user/corr/data'

xtal_size= sys.argv[1]
super_chunk = sys.argv[2]
chunk = int(sys.argv[3])


geom_code = '19MPz040'
pdb_code = '193l'

# cif = scorpy.CifData(f'{data_dir}/xtal/{pdb_code}-sf.cif')
# q_inte = min(cif.ast_mag, cif.bst_mag, cif.cst_mag)
# pk = scorpy.PeakData('', f'{data_dir}/geom/{geom_code}.geom')
# r_inte = pk.convert_q2r(q_inte)/2

r_inte = 0.003395225941658224 


print(20*'.', end='\r')
print(f'  {super_chunk} {chunk} {xtal_size}', end='\r')
for i_frame in range(0, 256):

    corr = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)

    npz_chunk_dir =  f'{data_dir}/frames/{xtal_size}-{geom_code}-{super_chunk}/{chunk}'
    npz_path = f'{npz_chunk_dir}/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-{chunk}-{i_frame}.npz'

    pk = scorpy.PeakData(npz_path, f'{data_dir}/geom/{geom_code}.geom')

    inte = pk.integrate_peaks(r_inte)
    pk.calc_scat(inte[:,0:3], inte[:,-1])

    corr.fill_from_peakdata(pk, verbose=0)

    corr_chunk_dir =  f'{data_dir}/qcor/{xtal_size}-{geom_code}-{super_chunk}/{chunk}'
    qcor_path = f'{corr_chunk_dir}/{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-{chunk}-{i_frame}-qcor.npy'

    corr.save(qcor_path)














