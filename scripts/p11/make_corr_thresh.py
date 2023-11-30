





import numpy as np
import scorpy
import matplotlib.pyplot as plt
import glob










datapath = f'/home/ec2-user/corr/data/p11'

runs = [i for i in range( 11, 25 )] + [i for i in range(40, 61) ]

all_numpeaks = []
all_maxintens = []
all_runids = []
all_frameids = []

for i_run, run in enumerate( runs):
    runpath = f'{datapath}/crystfel_calc/{run}/pk8_thr5_snr5'

    numpeaks =np.load(f'{runpath}/pklists/run{run}_numpeaks.npy')
    maxintens =np.load(f'{runpath}/pklists/run{run}_maxintens.npy')
    #number of peaks in each of the frames in this run
    all_numpeaks +=list(numpeaks)

    #maximum intensity in each of the frames in this run
    all_maxintens +=list(maxintens)

    #the run in each of the frames in this run
    all_runids += [run]*len(maxintens)
    #the frame id of the frames in this run
    all_frameids +=[i for i in range(len(maxintens))]

#turn them all in arrays
all_maxintens = np.array(all_maxintens)
all_numpeaks = np.array(all_numpeaks)
all_runids = np.array(all_runids)
all_frameids = np.array(all_frameids)

#shuffle all the arrays (in the same way)
np.random.seed(0)
p = np.random.permutation(len(all_maxintens))
all_maxintens =all_maxintens[p]
all_numpeaks =all_numpeaks[p]
all_runids =all_runids[p]
all_frameids =all_frameids[p]




d_inten_thresh = 5e3



# min_thresh = 60e3
# max_thresh = 65e3




thresh_bounds = np.arange(0e3, 81e3, 5e3)







# for i_thresh_bound, thresh_bound in enumerate(thresh_bounds[:-1]):
    # min_thresh = thresh_bound
    # max_thresh = thresh_bounds[i_thresh_bound+1]
    # print('OPTIONS:')
    # print(i_thresh_bound, min_thresh, max_thresh)





import sys

i_thresh_bound = int(sys.argv[1])

min_thresh = thresh_bounds[i_thresh_bound]
max_thresh = thresh_bounds[i_thresh_bound+1]


print('Correlating Frames with max intensity between:')
print(i_thresh_bound, min_thresh, max_thresh)




thresh_loc = np.logical_and(all_maxintens>=min_thresh, all_maxintens <max_thresh)


loc = np.where(np.logical_and(all_numpeaks>1,
                        np.logical_and(all_maxintens>=min_thresh,
                                       all_maxintens< max_thresh)))





corr_a = scorpy.CorrelationVol(nq=200, npsi=360, qmax=1.5, qmin=0.4, cos_sample=False)
corr_b = scorpy.CorrelationVol(nq=200, npsi=360, qmax=1.5, qmin=0.4, cos_sample=False)

print('Starting A half.')
for i, (runid, frameid) in enumerate(zip(all_runids[loc][::2], all_frameids[loc][::2])):

    print(f'{i+1}\t\t / {len(all_runids[loc][::2])}',end='\r')
    runpath = f'{datapath}/crystfel_calc/{runid}/pk8_thr5_snr5'

    pkfname = f'{runpath}/pklists/pklist-{frameid}.npy'
    pk = scorpy.PeakData(f'{pkfname}',
                         f'{datapath}/crystfel_calc/eiger.geom')
    corr_a.fill_from_peakdata(pk, verbose=0)

print(f'{0}\t\t / {len(all_runids[loc][::2])}',end='\r')
print('A half done.')

corr_a_fname = f'{datapath}/qcor/thresh/p11_allruns_d5k_{i_thresh_bound}_a_qcor'
corr_a.save(corr_a_fname)

print('Starting B half.')
for i, (runid, frameid) in enumerate(zip(all_runids[loc][1::2], all_frameids[loc][1::2])):

    print(f'{i+1}\t\t / {len(all_runids[loc][1::2])}',end='\r')
    runpath = f'{datapath}/crystfel_calc/{runid}/pk8_thr5_snr5'

    pkfname = f'{runpath}/pklists/pklist-{frameid}.npy'
    pk = scorpy.PeakData(f'{pkfname}',
                         f'{datapath}/crystfel_calc/eiger.geom')
    corr_b.fill_from_peakdata(pk, verbose=0)

print(f'{0}\t\t / {len(all_runids[loc][1::2])}',end='\r')
print('B half done.')

corr_b_fname = f'{datapath}/qcor/thresh/p11_allruns_d5k_{i_thresh_bound}_b_qcor'
corr_b.save(corr_b_fname)





print('\n'*3)



plt.show()







cifpath = f'/home/ec2-user/corr/data/xtal/193l-sf.cif'
corr_3d = scorpy.CorrelationVol(nq=200, npsi=360, qmax=1.5, qmin=0.4, cos_sample=False)
cif = scorpy.CifData(cifpath, qmax=1.5)
corr_3d.fill_from_cif(cif, verbose=99)

corr_3d.save(f'/home/ec2-user/corr/data/qcor/193l_3d_qcor.dbin')









