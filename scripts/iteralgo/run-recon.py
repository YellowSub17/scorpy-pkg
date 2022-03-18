#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import shutil
plt.close('all')

import sys




# Parameters



tag = 'nicotineamide-dres1-loose-supp-bigpsi-crop-poles'


# sub_tag=sys.argv[1]
sub_tag='er10'


recipe_fname =  'rec.txt'
sphv_init = None




# make sub directory for saving iters
os.mkdir(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}')

shutil.copyfile(f'{scorpy.DATADIR}/algo/RECIPES/{recipe_fname}',
                 f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/recipe_{tag}_{sub_tag}.txt')





# Load inputs 
blqq_data =scorpy.BlqqVol(path=f'{scorpy.DATADIR}/algo/{tag}/blqq_{tag}_data.dbin')
sphv_supp =scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')
recipe_file = open(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/recipe_{tag}_{sub_tag}.txt')



# Set up algorithm
a = scorpy.AlgoHandler(blqq_data, sphv_supp, sphv_init=sphv_init,
                       lossy_sphv=True, lossy_iqlm=True, rcond=1e-15)


print()
print(f'Name: {tag}_{sub_tag}')
print(f'Starting: {time.asctime()}')


a.sphv_iter.save(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_init.dbin')

count = 0
for line in recipe_file:

    terms = line.split()
    if terms == [] or line[0]=='#':
        continue
    niter = int(terms[0])
    scheme = eval('a.'+terms[1])

    kwargs = {}
    for kwarg in terms[2:]:
        kwargs[kwarg.split('=')[0]] = eval(kwarg.split('=')[1])



    print(f'Running: {line[:-1]}')
    for iter_num in range(niter):
        print(f'{iter_num}', end='\r')


        _,_, err = scheme(**kwargs)
        count +=1

        err_file = open(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/errs_{tag}_{sub_tag}.txt','a')
        err_file.write(f'{err},\t\t#{tag}_{sub_tag}_{count}\n')
        err_file.close()

        a.sphv_iter.save(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')

        # if count in [1, 2, 4, 8, 16, 32, 59, 60, 61, 62, 64, 68, 76]:
        if count in [1,2,3,4,5,6,7,8,9,10]:
            a.sphv_iter.save(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_c{count}.dbin')




a.sphv_iter.save(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')



print(f'Finished: {time.asctime()}')
print()





