#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





tags_subtags = [
                ('agno3-d03', 'a'),
                # ('agno3-d03', 'b'),
                # ('agno3-d03', 'c'),

                ('agno3-d05', 'a'),
                # ('agno3-d05', 'b'),
                # ('agno3-d05', 'c'),

                ('agno3-d07', 'a'),
                ('agno3-d07', 'b'),
                ('agno3-d07', 'c'),

                ('aluminophosphate-d05', 'a'),
                # ('aluminophosphate-d05', 'b'),
                # ('aluminophosphate-d05', 'c'),

                ('aluminophosphate-d07', 'a'),
                ('aluminophosphate-d07', 'b'),
                ('aluminophosphate-d07', 'c'),

                ('tbcampmamp-d07', 'a'),
                ('tbcampmamp-d07', 'b'),
                ('tbcampmamp-d07', 'c'),

                ('tbcampmamp-d05', 'a'),
                ('tbcampmamp-d05', 'b'),
                ('tbcampmamp-d05', 'c'),
               ]



# counts = [i for i in range(121)]

# for tag, subtag in tags_subtags:
    # print(f'##### {tag}')
    # a = scorpy.AlgoHandler(tag)
    # a.run_shelx(subtag)
    # a.run_shelx(subtag, count='targ')
    # for count in counts:
        # print(f'shelxl {count}', end='\r')
        # a.run_shelx(subtag, count=count)

    # a.save_rfs(subtag, verbose=99)
    # a.save_dgeom(subtag, geometry='distances', verbose=99)
    # a.save_dgeom(subtag, geometry='angles', verbose=99)
    # a.save_dxyzs(subtag, verbose=99)
    # print()
    # print()




# ##### NL study
# nls = [i for i in range(60, 181, 15)]
# counts = [i for i in range(111)]
# subtags = ['a','b','c','d']
# for nl in nls:
    # tag = f'agno3-nl{nl}'
    # print(f'##### {tag}')
    # a = scorpy.AlgoHandler(tag)
    # a.run_shelx(subtag)
    # a.run_shelx(subtag, count='targ')
    # for count in counts:
        # print(f'shelxl {count}', end='\r')
        # a.run_shelx(subtag, count=count)

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












