# from xfelcorrel import *
# from blqq import *

from scorpy import CorrelationVol
import json

# infile = open('../data/cxi/run_statistics.json', 'r')
# stats = json.load(infile)

import numpy as np

def cosine_sim(x,y):
    x_flat = x.flatten()
    y_flat = y.flatten()
    x_mag = np.linalg.norm(x_flat)
    y_mag = np.linalg.norm(y_flat)
    return np.dot(x_flat/x_mag, y_flat/y_mag)


def corr_cosine_sim(c1,c2, mask=None, convolve=False):
    ##take out lowest row (full of zeros in mask)
#     c1.cvol = c1.cvol[1:,1:,:]
    # c2.cvol = c2.cvol[1:,1:,:]
    # c1.nq -=1
    # c2.nq -=1

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
        c1.convolve(kern_L=7, kern_n=9, std_x=3.5, std_y=3.5, std_z=3.5)
        c2.convolve(kern_L=7, kern_n=9, std_x=3.5, std_y=3.5, std_z=3.5)



    for iq1 in range(c1.nq):
        for iq2 in range(c1.nq):

            ave1 = np.mean(c1.cvol[iq1, iq2, :])
            ave2 = np.mean(c2.cvol[iq1, iq2, :])
            c1.cvol[iq1, iq2, :] -= ave1
            c2.cvol[iq1, iq2, :] -= ave2
    return cosine_sim(c1.cvol, c2.cvol)



runs150 = [112,123,113,125,102,103,104,105]
runs144 = [118,108,119,109,120,110,121]
runs = runs150+runs144



# runs = [108, 109, 110]




numseeds = 20

con_bool = True


for run in runs:

    sims = []
    for seed in range(numseeds):
        corra = CorrelationVol( path=f'../data/dbins/cosine_sim/{run}/run{run}_seed{seed}a_qcor')
        corrb = CorrelationVol( path=f'../data/dbins/cosine_sim/{run}/run{run}_seed{seed}b_qcor')

        sims.append(corr_cosine_sim(corra, corrb, convolve=con_bool ))

    print(f'{run}, {run}, {np.mean(sims)}, {np.std(sims)}')


# print('------')
# print('------')
print('------')

for i, run1 in enumerate(runs):
    for run2 in runs[i:]:

        if run1==run2:
            continue

        cor1 = CorrelationVol( path=f'../data/dbins/cosine_sim/{run1}/run{run1}_qcor')
        cor2 = CorrelationVol( path=f'../data/dbins/cosine_sim/{run2}/run{run2}_qcor')


        print(f'{run1}, {run2}, {corr_cosine_sim(cor1, cor2, convolve=con_bool)}')





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



