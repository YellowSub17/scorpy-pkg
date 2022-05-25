#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')







# tags = ['aluminophosphate-d07', 'tbcampmamp-d07']
# counts = [i for i in range(121)]


# for tag in tags:
    # print(f'##### {tag}')
    # a = scorpy.AlgoHandler(tag)
    # a.run_shelx('a')
    # a.run_shelx('a', count='targ')
    # for count in counts:
        # print(f'shelxl {count}', end='\r')
        # a.run_shelx('a', count=count)

    # a.save_rfs('a', verbose=99)
    # a.save_dgeom('a', geometry='distances', verbose=99)
    # a.save_dgeom('a', geometry='angles', verbose=99)
    # a.save_dxyzs('a', verbose=99)





sub_tags =['a', 'b', 'c']
counts = [i for i in range(121)]


for sub_tag in sub_tags:
    print(f'##### {sub_tag}')
    a = scorpy.AlgoHandler('aluminophosphate-d07')
    a.run_shelx(f'{sub_tag}')
    a.run_shelx(f'{sub_tag}', count='targ')
    for count in counts:
        print(f'shelxl {count}', end='\r')
        a.run_shelx(f'{sub_tag}', count=count)

    a.save_rfs(f'{sub_tag}', verbose=99)
    a.save_dgeom(f'{sub_tag}', geometry='distances', verbose=99)
    a.save_dgeom(f'{sub_tag}', geometry='angles', verbose=99)
    a.save_dxyzs(f'{sub_tag}', verbose=99)






###### NQ study

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



###### NL study

# nls = [i for i in range(60, 181, 15)]
# for nl in nls:
    # a = scorpy.AlgoHandler(f'agno3-nl{nl}')
    # a.save_dgeom('a', geometry='distances', verbose=99)
    # a.save_dgeom('a', geometry='angles', verbose=99)
    # a.save_dxyzs('a', verbose=99)






