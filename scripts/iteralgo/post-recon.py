#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





tags_subtags = [

                # ('agno3-d03', 'a'),
                # ('agno3-d03', 'b'),
                # ('agno3-d03', 'c'),
                # ('agno3-d03', 'd'),
                # ('agno3-d03', 'e'),
                # ('agno3-d03', 'f'),
                # ('agno3-d03', 'g'),
                # ('agno3-d03', 'h'),
                ('agno3-d03', 'aER'),
                ('agno3-d03', 'bER'),
                ('agno3-d03', 'cER'),
                ('agno3-d03', 'dER'),
                ('agno3-d03', 'eER'),
                ('agno3-d03', 'fER'),
                ('agno3-d03', 'gER'),
                ('agno3-d03', 'hER'),

                # ('agno3-d05', 'a'),
                ('agno3-d05', 'b'),
                ('agno3-d05', 'c'),
                ('agno3-d05', 'd'),
                ('agno3-d05', 'e'),
                ('agno3-d05', 'f'),
                ('agno3-d05', 'g'),
                ('agno3-d05', 'h'),

                # ('agno3-d07', 'a'),
                # ('agno3-d07', 'b'),
                # ('agno3-d07', 'c'),
                ('agno3-d07', 'd'),
                ('agno3-d07', 'e'),
                ('agno3-d07', 'f'),
                ('agno3-d07', 'g'),
                ('agno3-d07', 'h'),



                # ('aluminophosphate-d05', 'a'),
                ('aluminophosphate-d05', 'b'),
                ('aluminophosphate-d05', 'c'),
#                 ('aluminophosphate-d05', 'd'),
                # ('aluminophosphate-d05', 'e'),
                # ('aluminophosphate-d05', 'f'),
                # ('aluminophosphate-d05', 'g'),
                # ('aluminophosphate-d05', 'h'),
                ('aluminophosphate-d05', 'aER'),
                ('aluminophosphate-d05', 'bER'),
                ('aluminophosphate-d05', 'cER'),
                ('aluminophosphate-d05', 'dER'),
                ('aluminophosphate-d05', 'eER'),
                ('aluminophosphate-d05', 'fER'),
                ('aluminophosphate-d05', 'gER'),
                ('aluminophosphate-d05', 'hER'),


                # ('tbcampmamp-d05', 'a'),
                # ('tbcampmamp-d05', 'b'),
                # ('tbcampmamp-d05', 'c'),
                # ('tbcampmamp-d05', 'd'),
                # ('tbcampmamp-d05', 'e'),
                # ('tbcampmamp-d05', 'f'),
                # ('tbcampmamp-d05', 'g'),
                # ('tbcampmamp-d05', 'h'),
                ('tbcampmamp-d05', 'aER'),
                ('tbcampmamp-d05', 'bER'),
                ('tbcampmamp-d05', 'cER'),
                ('tbcampmamp-d05', 'dER'),
                ('tbcampmamp-d05', 'eER'),
                ('tbcampmamp-d05', 'fER'),
                ('tbcampmamp-d05', 'gER'),
                ('tbcampmamp-d05', 'hER'),

]








counts = [i for i in range(121)]

for tag, subtag in tags_subtags:
    print(f'##### {tag}')
    a = scorpy.AlgoHandler(tag)
    a.run_shelx(subtag)
    a.run_shelx(subtag, count='targ')
    for count in counts:
        print(f'shelxl {count}', end='\r')
        a.run_shelx(subtag, count=count)

    a.save_rfs(subtag, verbose=99)
    a.save_dgeom(subtag, geometry='distances', verbose=99)
    a.save_dgeom(subtag, geometry='angles', verbose=99)
    a.save_dxyzs(subtag, verbose=99)
    print()
    print()




# #### NL study
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












