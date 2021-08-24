#!/usr/bin/env/ python3
'''
espk-cosine-sim.py

Complete cosine similarity across correlation volumes of ensemble peak data (simulated crystals)
'''
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')


nseeds = 10
ns = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]


aves = []
stds = []

for n in ns:

    sims = np.zeros((nseeds, nseeds)) + 1.234567e-27
    for i in range(nseeds):
        corr1 = scorpy.CorrelationVol(path=f'{scorpy.__DATADIR}/espk/espk-dbins/ensemble_n{n}_{i}')

        for j in range(i + 1, nseeds):
            corr2 = scorpy.CorrelationVol(path=f'{scorpy.__DATADIR}/espk/espk-dbins/ensemble_n{n}_{j}')

            print('n:', n, 'i:', i, 'j:', j)

            sim = scorpy.utils.cosinesim(corr1.vol, corr2.vol)
            sims[i, j] = sim
            sims[j, i] = sim

    loc = np.where(sims != 1.234567e-27)

    print()
    print()
    print('n:', n)
    print('Average Sim:', np.mean(sims))
    print('STD Sim:', np.std(sims))
    print()
    print()

    aves.append(np.mean(sims[loc]))
    stds.append(np.std(sims[loc]))

    plt.figure()
    plt.imshow(sims)
    plt.title(f'Cosine Sim n:{n}')
    plt.xlabel('Seed')
    plt.ylabel('Seed')
    plt.colorbar()
    # plt.savefig(f'/home/pat/Documents/cloudstor/phd/latex/scorpy-script-reports/figs/espk-cossim-n{n}.png')


plt.figure()
plt.errorbar(ns, aves, yerr=stds, fmt='b.', barsabove=True)
plt.title('Cosine Similarity of Simulated Hits')
plt.xlabel('# of hits per run')
plt.ylabel('Similarity')
# plt.savefig('/home/pat/Documents/cloudstor/phd/latex/scorpy-script-reports/figs/espk-cossim-ave.png')



plt.show()
