





import numpy as np
import scorpy
import matplotlib.pyplot as plt
import glob






# runs = [i for i in range( 11, 25 )] + [i for i in range(40, 61) ]
# for run in runs:

    # print(f'Starting run:\t{run}')
    # datapath = f'/home/ec2-user/corr/data/p11'
    # runpath = f'{datapath}/crystfel_calc/{run}/pk8_thr5_snr5'
    # pklists = glob.glob(f'{runpath}/pklists/pklist-*.npy')

    # corr_total = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)

    # for i_pklist,  pklist in enumerate(pklists):
        # print(i_pklist, end='\r')
        # pk = scorpy.PeakData(f'{pklist}',
                             # f'{datapath}/crystfel_calc/eiger.geom')
        # corr_total.fill_from_peakdata(pk, verbose=0)



    # corr_total.save(f'{datapath}/qcor/p11_run{run}_total_qcor.dbin')




# cifpath = f'/home/ec2-user/corr/data/xtal/193l-sf.cif'
# corr_3d = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)
# cif = scorpy.CifData(cifpath, qmax=1.5)


# corr_3d.fill_from_cif(cif, verbose=99)

# corr_3d.save(f'/home/ec2-user/corr/data/qcor/193l_3d_qcor.dbin')









