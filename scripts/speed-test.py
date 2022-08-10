


import timeit



setup = 'import numpy as np;import scorpy;vol = np.random.random((100, 100, 180));corr = scorpy.CorrelationVol(100, 180, 1);corr.vol = vol[:]'

stm_npy = "corr.save('/home/pat/Desktop/x/x.npy')"
print('Timing npy...', end='')
t_npy = timeit.timeit(stm_npy, setup=setup, number=150)
print('Done.')


stm_dbin = "corr.save('/home/pat/Desktop/x/x.dbin')"
print('Timing dbin...', end='')
t_dbin = timeit.timeit(stm_dbin, setup=setup, number=150)
print('Done.')

print(f'\n\n{t_npy=}\n{t_dbin=}')


