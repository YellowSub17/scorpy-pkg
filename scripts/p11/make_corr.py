





import numpy as np
import scorpy
import matplotlib.pyplot as plt
import glob





# ##### make qcor from all frames
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





# runs = [i for i in range( 11, 25 )] + [i for i in range(40, 61) ]

# for run in runs:

    # print(f'Starting run:\t{run}')
    # datapath = f'/home/ec2-user/corr/data/p11'
    # runpath = f'{datapath}/crystfel_calc/{run}/pk8_thr5_snr5'

    # numpeaks =np.load(f'{runpath}/pklists/run{run}_numpeaks.npy')
    # maxintens =np.load(f'{runpath}/pklists/run{run}_maxintens.npy')
    # loc = np.where(np.logical_and(numpeaks>1, maxintens<1e4))

    # # print(numpeaks[loc])
    # # print(maxintens[loc])


    # corr_a = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)
    # corr_b = scorpy.CorrelationVol(nq=150, npsi=180, qmax=1.5, qmin=0.4, cos_sample=False)


    # for i_pklist in loc[0][::2]:
        # print(i_pklist, end='\r')
        # pkfname = f'{runpath}/pklists/pklist-{i_pklist}.npy'
        # pk = scorpy.PeakData(f'{pkfname}',
                             # f'{datapath}/crystfel_calc/eiger.geom')
        # corr_a.fill_from_peakdata(pk, verbose=0)


    # for i_pklist in loc[0][1::2]:
        # print(i_pklist, end='\r')
        # pkfname = f'{runpath}/pklists/pklist-{i_pklist}.npy'
        # pk = scorpy.PeakData(f'{pkfname}',
                             # f'{datapath}/crystfel_calc/eiger.geom')
        # corr_b.fill_from_peakdata(pk, verbose=0)


    # corr_a.save(f'{datapath}/qcor/p11_run{run}_a_thresh.dbin')
    # corr_b.save(f'{datapath}/qcor/p11_run{run}_b_thresh.dbin')
















cifpath = f'/home/ec2-user/corr/data/xtal/193l-sf.cif'
corr_3d = scorpy.CorrelationVol(nq=200, npsi=5760, qmax=1.5, qmin=0.4, cos_sample=False)
cif = scorpy.CifData(cifpath, qmax=1.5)
corr_3d.fill_from_cif(cif, verbose=99)
corr_3d.save(f'/home/ec2-user/corr/data/qcor/193l_3d_big_qcor.dbin')



# print('Lysozyme 193l-sf.cif')
# print('qmax(a-1)\tres(a)\t\tnvec')
# for qmax in np.arange(0.5, 4.6, 0.5):
    # cif = scorpy.CifData(cifpath, qmax=qmax)
    # print(np.round(cif.qmax,3), np.round((2*np.pi)/cif.qmax, 3), cif.scat_rect.shape[0], sep='\t\t')









