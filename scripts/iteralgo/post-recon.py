#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')








# #### recipe study
# counts = [i for i in range(121)]


# subtags = ['ER120', 
            # 'HIO10ER10',
            # 'HIO20ER20',
            # 'HIO30ER30',
            # 'HIO60ER60',
            # 'HIO120',
           # ]






# for subtag in subtags:
    # tag = f'agno3-rec'
    # print(f'##### {tag}')
    # a = scorpy.AlgoHandler(tag)
# #     a.run_shelx(subtag)
    # # a.run_shelx(subtag, count='targ')
    # # for count in counts:
        # # print(f'shelxl {count}', end='\r')
        # # a.run_shelx(subtag, count=count)

    # a.save_rfs(subtag, verbose=99)
    # a.save_dgeom(subtag, geometry='distances', verbose=99)
    # a.save_dgeom(subtag, geometry='angles', verbose=99)
    # a.save_dxyzs(subtag, verbose=99)

    # print()
    # print()









# #### NL study
# nls = [i for i in range(60, 181, 15)]
# counts = [i for i in range(111)]
# subtags = ['a','b','c','d']

# for subtag in subtags:
    # for nl in nls:
        # tag = f'agno3-nl{nl}'
        # print(f'##### {tag}')
        # a = scorpy.AlgoHandler(tag)
# #         a.run_shelx(subtag)
        # # a.run_shelx(subtag, count='targ')
        # # for count in counts:
            # # print(f'shelxl {count}', end='\r')
            # # a.run_shelx(subtag, count=count)

        # a.save_rfs(subtag, verbose=99)
        # a.save_dgeom(subtag, geometry='distances', verbose=99)
        # a.save_dgeom(subtag, geometry='angles', verbose=99)
        # a.save_dxyzs(subtag, verbose=99)

    # print()
    # print()





# ##### NQ study

# nqs = [i for i in range(25,251, 25)]
# for nq in nqs:
    # if nq==150:
        # tag = 'agno3-nl180'
    # elif nq==200:
        # tag = 'agno3-random-starts'
    # else:
        # tag = f'agno3-nq{nq}'
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

    # print()
    # print()


# print(time.asctime())
# print(time.asctime())












