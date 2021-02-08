from xfelcorrel import *
from blqq import *
import json

infile = open('data/cxi/run_statistics.json', 'r')
stats = json.load(infile)

import numpy as np

def cosine_sim(x,y):
    x_flat = x.flatten()
    y_flat = y.flatten()
    x_mag = np.linalg.norm(x_flat)
    y_mag = np.linalg.norm(y_flat)
    return np.dot(x_flat/x_mag, y_flat/y_mag)


def corr_cosine_sim(c1,c2, mask=None, convolve=False):
    ##take out lowest row (full of zeros in mask)
    c1.cvol = c1.cvol[1:,1:,:]
    c2.cvol = c2.cvol[1:,1:,:]
    c1.nq -=1
    c2.nq -=1

    if mask is not None:

        #take out lowest row (full of zeros in mask)
        mask.cvol = mask.cvol[1:, 1:, :]
        mask.nq -= 1

        #divide by mask
        c1.cvol *= 1/mask.cvol
        c2.cvol *= 1/mask.cvol
        #set correlations to 0 is mask is too low
        c1.cvol[np.where(mask.cvol <1e-1)] = 0
        c2.cvol[np.where(mask.cvol <1e-1)] = 0

    if convolve:
        #convolve the correlation volumes
        c1.cvol = c1.convolve(kern_L=7, kern_size=9, std_q=3.5, std_t=3.5)
        c2.cvol = c2.convolve(kern_L=7, kern_size=9, std_q=3.5, std_t=3.5)


   #  for it in range(c1.ntheta):
        # theta_ave1 = np.mean(c1.cvol[:, :, it])
        # theta_ave2 = np.mean(c2.cvol[:, :, it])
        # c1.cvol[:, : , it] -= theta_ave1
        # c2.cvol[:, : , it] -= theta_ave2
    # return cosine_sim(c1.cvol, c2.cvol)


    for iq1 in range(c1.nq):
        for iq2 in range(c1.nq):

            ave1 = np.mean(c1.cvol[iq1, iq2, :])
            ave2 = np.mean(c2.cvol[iq1, iq2, :])
            c1.cvol[iq1, iq2, :] -= ave1
            c2.cvol[iq1, iq2, :] -= ave2
    return cosine_sim(c1.cvol, c2.cvol)

# ###    subtract mean for volume, then compare similarity 
    # return cosine_sim(c1.cvol - c1.cvol.mean(), c2.cvol - c2.cvol.mean())




runs150 = [112,123,113,125,102,103,104,105]
runs144 = [118,108,119,109,120,110,121]
runs = runs150+runs144



runs = [108, 109, 110]




numseeds = 20



for run in runs:

    sims = []
    for seed in range(numseeds):
        corra = CorrelationVol(fromfile=True, fname=f'data/dbins/cosine_sim/{run}/qcor_a_seed{seed}')
        corrb = CorrelationVol(fromfile=True, fname=f'data/dbins/cosine_sim/{run}/qcor_b_seed{seed}')
        mask_cor = CorrelationVol(fromfile=True, fname='data/masks/radial_mask_iwr_qcor_qmax')

        sims.append(corr_cosine_sim(corra, corrb, convolve=True ))

    corra.plot_q1q2()
    plt.title(f'Run: {run}, half (a)')
    plt.savefig(f'data/saved_plots/run{run}_corra.png')

    corrb.plot_q1q2()
    plt.title(f'Run: {run}, half (b)')
    plt.savefig(f'data/saved_plots/run{run}_corrb.png')

    # print(f'\nComparing {run}(a) to {run}(b):')
    # print(f'\tAverage: {np.mean(sims)}')
    # print(f'\tStandard. Dev.:{np.std(sims)}')

    print(f'{run}, {run}, {np.mean(sims)}, {np.std(sims)}')


# print('------')
# print('------')
print('------')

for i, run1 in enumerate(runs):
    for run2 in runs[i:]:

        if run1==run2:
            continue

        cor1 = CorrelationVol(fromfile=True, fname=f'data/dbins/cosine_sim/{run1}/qcor_all_peakmax150')
        cor2 = CorrelationVol(fromfile=True, fname=f'data/dbins/cosine_sim/{run2}/qcor_all_peakmax150')
        mask_cor = CorrelationVol(fromfile=True, fname='data/masks/radial_mask_iwr_qcor_qmax')

        # print(f'\nComparing {run1} (full) to {run2} (full):')
        # print(f'\tSimilarity: {corr_cosine_sim(cor1, cor2, mask=mask_cor, convolve=True)}')

        print(f'{run1}, {run2}, {corr_cosine_sim(cor1, cor2, convolve=True)}')

        if i==0:
            cor2.plot_q1q2()
            plt.title(f'Run: {run2}, full')
            plt.savefig(f'data/saved_plots/run{run2}_full.png')

# mask_cor.plot_q1q2()



# runs = [108,109, 110 ]
# for i, run1 in enumerate(runs):
    # for run2 in runs[i:]:

        # if run1==run2:
            # continue
        # padf = CorrelationVol(40, 90, 30)
        # x = np.fromfile(f'data/dbins/cosine_sim/{run1}/{run1}_padf_padf.dbin').reshape( (120,120,180))[20:60, 20:60, :90]
        # padf.cvol=x
        # padf.qmax /=2
        # # padf.plot_q1q2()
        # # plt.ylabel('r1=r2 [A]')

        # padf1 = CorrelationVol(40, 90, 30)
        # x = np.fromfile(f'data/dbins/cosine_sim/{run2}/{run2}_padf_padf.dbin').reshape( (120,120,180))[20:60, 20:60, :90]
        # padf1.cvol=x
        # padf1.qmax /=2
        # # padf1.plot_q1q2()
        # # plt.ylabel('r1=r2 [A]')


        # print(f'\nComparing {run1} (padf) to {run2} (padf):')
        # print(f'Similarity: {corr_cosine_sim(padf, padf1, convolve=True)}')

# #         if i==0:
            # # padf1.plot_q1q2()
            # # plt.ylabel('r1=r2 [A]')
            # # plt.title(f'Run: {run2}, padf')



# for run in runs:

    # sims = []
    # for seed in range(5):
        # corra = CorrelationVol(40, 90, 30)
        # x = np.fromfile(f'data/dbins/cosine_sim/{run}/seed{seed}_a_padf.dbin').reshape( (120,120,180))[20:60, 20:60, :90]
        # corra.cvol=x

        # corrb = CorrelationVol(40, 90, 30)
        # x = np.fromfile(f'data/dbins/cosine_sim/{run}/seed{seed}_b_padf.dbin').reshape( (120,120,180))[20:60, 20:60, :90]
        # corrb.cvol=x



        # sims.append(corr_cosine_sim(corra, corrb, convolve=True))

    # corra.plot_q1q2()
    # plt.title(f'{run}, (a)')
    # corrb.plot_q1q2()
    # plt.title(f'{run}, (b)')
    # print(f'\nComparing {run}(a) to {run}(b):')
    # print(f'\tAverage: {np.mean(sims)}')
    # print(f'\tStandard. Dev.:{np.std(sims)}')



