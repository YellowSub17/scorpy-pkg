#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')




# tags = os.listdir(scorpy.DATADIR / 'algo')


# for tag in tags:

    # #make algo handler
    # a = scorpy.AlgoHandler(tag)

    # # get subtags
    # subtags = os.listdir(scorpy.DATADIR / 'algo' / tag)

    # for subtag in subtags:

        # #skip files, just do subtags
        # if not os.path.isdir(scorpy.DATADIR / 'algo' / tag / subtag):
            # continue

        
        # a.run_shelx(subtag)
        # a.run_shelx(subtag, count='targ')

        # count_max = len(os.listdir(scorpy.DATADIR / 'algo' / tag / subtag/ 'hkls'))


        # counts = [i for i in range(count_max)]

        # print()
        # print(f'######## {tag} {subtag} {count_max}')
        # print()
        # for count in counts:
            # print(f'shelxl {count}', end='\r')
            # a.run_shelx(subtag, count=count)

        # a.save_rfs(subtag, verbose=99)
        # a.save_dgeom(subtag, geometry='distances', verbose=99)
        # a.save_dgeom(subtag, geometry='angles', verbose=99)
        # a.save_dxyzs(subtag, verbose=99)
























