import numpy as np
import matplotlib.pyplot as plt
import scorpy
import glob

plt.rc('font', size=8)




# datapath = f'/home/ec2-user/corr/data/p11'


# # runs = [i for i in range( 11, 25 )] + [i for i in range(40, 61) ]
# # runs = [i for i in range( 11, 25 )] 
# # runs = [i for i in range(40, 61) ]



# runs_opt = '13'
# runs_opt = 'all'


# if runs_opt ==  'all':
    # runs = [i for i in range( 11, 25 )] + [i for i in range(40, 61) ]
# else:
    # runs = [ runs_opt ]

# all_numpeaks = []
# all_maxintens = []


# for i_run, run in enumerate( runs):
    # print(run)
    # runpath = f'{datapath}/crystfel_calc/{run}/pk8_thr5_snr5'


    # numpeaks =np.load(f'{runpath}/pklists/run{run}_numpeaks.npy')
    # maxintens =np.load(f'{runpath}/pklists/run{run}_maxintens.npy')
    # all_numpeaks +=list(numpeaks)
    # all_maxintens +=list(maxintens)


# all_maxintens = np.array(all_maxintens)
# all_numpeaks = np.array(all_numpeaks)




# print(np.sum(all_numpeaks==0))


# # print(np.sum(p.where(numpeaks>0)))

# # min_thresh = 0.5e4
# # max_thresh = 1e4

# # min_thresh = 0.e4
# # max_thresh = 10.0e4



# # np.random.seed(0)
# # p = np.random.permutation(len(all_maxintens))
# # all_maxintens, all_numpeaks = all_maxintens[p], all_numpeaks[p]

# # loc = np.where(np.logical_and(all_numpeaks>1,
                        # # np.logical_and(all_maxintens>=min_thresh,
                                       # # all_maxintens< max_thresh)))


datapath = f'/home/ec2-user/corr/data/p11'

runs_opt = '13'
runs_opt = 'all'


if runs_opt ==  'all':
    runs = [i for i in range( 11, 25 )] + [i for i in range(40, 61) ]
else:
    runs = [ runs_opt ]



# runs = [i for i in range( 11, 25 )] + [i for i in range(40, 61) ]

all_numpeaks = []
all_maxintens = []
all_runids = []
all_frameids = []

for i_run, run in enumerate( runs):
    runpath = f'{datapath}/crystfel_calc/{run}/pk8_thr5_snr5'

    numpeaks =np.load(f'{runpath}/pklists/run{run}_numpeaks.npy')
    maxintens =np.load(f'{runpath}/pklists/run{run}_maxintens.npy')
    all_numpeaks +=list(numpeaks)
    all_maxintens +=list(maxintens)
    all_runids += [run]*len(maxintens)
    all_frameids +=[i for i in range(len(maxintens))]

all_maxintens = np.array(all_maxintens)
all_numpeaks = np.array(all_numpeaks)
all_runids = np.array(all_runids)
all_frameids = np.array(all_frameids)

np.random.seed(0)
p = np.random.permutation(len(all_maxintens))
print(p)
all_maxintens =all_maxintens[p]
all_numpeaks =all_numpeaks[p]
all_runids =all_runids[p]
all_frameids =all_frameids[p]



# min_thresh = 0
# max_thresh = np.max(all_maxintens)+10

min_thresh = 50e3
max_thresh = 60e3




thresh_loc = np.logical_and(all_maxintens>=min_thresh, all_maxintens <max_thresh)


loc = np.where(np.logical_and(all_numpeaks>1,
                        np.logical_and(all_maxintens>=min_thresh,
                                       all_maxintens< max_thresh)))





grp_ab = all_maxintens
grp_ab_loc = all_maxintens[loc]
grp_a_loc = all_maxintens[loc][::2]
grp_b_loc = all_maxintens[loc][1::2]


plt.figure(figsize=(8/2.54, 8/2.54), dpi = 300)

plt.vlines( min_thresh ,0, 2 , color=(0.5,0.5,0.5, 0.5), ls='dashed')
plt.vlines( max_thresh ,0, 2 , color=(0.5,0.5,0.5, 0.5), ls='dashed')

binwidth = 200

bins = np.arange(0, np.max(grp_ab)+binwidth, binwidth)
counts,_= np.histogram(grp_ab, bins=bins)


plt.hist(bins[:-1], bins, weights=np.log10(counts +1), color=(0,0,0), label='All')

counts,_= np.histogram(grp_ab_loc, bins=bins)
plt.hist(bins[:-1], bins, weights=np.log10(counts +1), color=(0, 1, 1, 0.75), label='Crop')

plt.xlabel('Max Intensity (x1e4)')
plt.ylabel('Frequency (log10)')


plt.legend(title=f'Run: {runs_opt}')

plt.tight_layout()



binwidth = 20

plt.figure(figsize=(8/2.54, 8/2.54), dpi = 300)

plt.vlines( min_thresh ,0, 2 , color=(0.5,0.5,0.5, 0.5), ls='dashed')
plt.vlines( max_thresh ,0, 2 , color=(0.5,0.5,0.5, 0.5), ls='dashed')

bins = np.arange(min_thresh, max_thresh+binwidth, binwidth)
counts,_= np.histogram(grp_a_loc, bins=bins)
mean_a= np.mean(grp_a_loc)
plt.hist(bins[:-1], bins, weights=np.log10(counts +1), color=(0,0,1,1), label='Half a')
plt.plot(mean_a, -0.125, color='b', marker='x')


counts,_= np.histogram(grp_b_loc, bins=bins)
mean_b= np.mean(grp_b_loc)
plt.hist(bins[:-1], bins, weights=np.log10(counts +1), color=(1, 0, 0,0.75 ), label='Half b')
plt.plot(mean_b, -0.12,color='r', marker='x')


plt.xlabel('Max Intensity (x1e4)')
plt.ylabel('Frequency (log10)')
plt.legend(title=f'Run: {runs_opt}')

plt.tight_layout()
plt.show()

