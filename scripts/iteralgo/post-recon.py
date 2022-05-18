#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')







tags = ['agno3-d05', 'agno3-d03' ]



# nqs = [i for i in range(25,251, 25)]

# for nq in nqs:


    # if nq==150:
        # tag = 'agno3-nl180'
    # elif nq==200:
        # tag = 'agno3-random-starts'
    # else:
        # tag = f'agno3-nq{nq}'


    # a = scorpy.AlgoHandler(tag)

    # a.save_dgeom('a', geometry='distances', verbose=99)
    # a.save_dgeom('a', geometry='angles', verbose=99)
    # a.save_dxyzs('a', verbose=99)




# nls = [i for i in range(60, 181, 15)]
# for nl in nls:
    # a = scorpy.AlgoHandler(f'agno3-nl{nl}')
    # a.save_dgeom('a', geometry='distances', verbose=99)
    # a.save_dgeom('a', geometry='angles', verbose=99)
    # a.save_dxyzs('a', verbose=99)




# counts = [i for i in range(121)]


# a = scorpy.AlgoHandler(f'aluminophosphate-d05')
# print(f'{a.tag} shelx')
# a.run_shelx('a')
# a.run_shelx('a', count='targ')
# for count in counts:
    # print(f'{count}', end='\r')
    # a.run_shelx('a', count=count)

# a.save_dgeom('a', geometry='distances', verbose=99)
# a.save_dgeom('a', geometry='angles', verbose=99)
# a.save_dxyzs('a', verbose=99)

# a = scorpy.AlgoHandler(f'tbcampmamp-d05')
# print(f'{a.tag} shelx')
# a.run_shelx('a')
# a.run_shelx('a', count='targ')
# for count in counts:
    # print(f'{count}', end='\r')
    # a.run_shelx('a', count=count)
# a.save_dgeom('a', geometry='distances', verbose=99)
# a.save_dgeom('a', geometry='angles', verbose=99)
# a.save_dxyzs('a', verbose=99)



a = scorpy.AlgoHandler(f'aluminophosphate-d05')
a.save_rfs('a', verbose=99)
a = scorpy.AlgoHandler(f'tbcampmamp-d05')
a.save_rfs('a', verbose=99)
