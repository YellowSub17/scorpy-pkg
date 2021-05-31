import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')


nseeds = 25
ns = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]


aves = []
stds = []

for n in ns:

    sims = np.zeros((nseeds, nseeds)) + 1.234567e-27
    for i in range(nseeds):
        corr1 = scorpy.CorrelationVol(path=f'../data/dbins/ensemble_peaks/ensemble_n{n}_{i}.dbin')
        corr1.sub_t_mean()
        for j in range(i + 1, nseeds):
            corr2 = scorpy.CorrelationVol(path=f'../data/dbins/ensemble_peaks/ensemble_n{n}_{j}.dbin')
            corr2.sub_t_mean()

            print('n:', n, 'i:', i, 'j:', j)

            sim = scorpy.utils.cosinesim(corr1.vol, corr2.vol)
            sims[i, j] = sim
            sims[j, i] = sim

    loc = np.where(sims != 1.234567e-27)

    print()
    print()
    print('n:', n)
    print('Average Sim (Sub T mean):', np.mean(sims))
    print('STD Sim (Sub T mean):', np.std(sims))
    print()
    print()

    aves.append(np.mean(sims[loc]))
    stds.append(np.std(sims[loc]))

    plt.figure()
    plt.imshow(sims)
    plt.title(f'Cosine Sim n:{n} (Sub T mean)')
    plt.xlabel('Seed')
    plt.ylabel('Seed')
    plt.colorbar()


plt.figure()
plt.errorbar(ns, aves, yerr=stds, fmt='b.', barsabove=True)
plt.title('Average similarity (Sub T mean)')


plt.show()
