
import timeit
import scorpy
import numpy as np
np.random.seed(0)

print()


# ## CorrelationVols
# # names = ['3wct', '3wcu', '3wcv', '3wcw']
# names = ['1al1']

# for name in names:


    # cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif')
    # cor = scorpy.CorrelationVol(200,360, cif.qmax)

    # # cor.correlate(cif.scattering)

    # print(f'\n\nName: {name}, qmax: {cif.qmax}')
    # print(f'\n\nnq: {cor.nq}, ntheta: {cor.ntheta}')
    # print(f'Correlating {cif.scattering.shape[0]} vectors.')
    # t = timeit.timeit( 'cor.correlate(cif.scattering)', number=1, globals=globals())
    # print(f'Time taken: {t} seconds.')

    # cor.save_dbin(f'../data/dbins/{name}_qcor')



