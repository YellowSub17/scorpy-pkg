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



tag = 'agno3-largerqmax'


sub_tag = 'testing'


recipe_fname =  'testing.txt'
sphv_init = None




# make sub directory for saving iters
os.mkdir(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}')
os.mkdir(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/plots')

shutil.copyfile(f'{scorpy.DATADIR}/algo/RECIPES/{recipe_fname}',
                 f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/recipe_{tag}_{sub_tag}.txt')





# Load inputs 
blqq_data =scorpy.BlqqVol(path=f'{scorpy.DATADIR}/algo/{tag}/blqq_{tag}_data.dbin')
sphv_supp =scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')
sphv_targ =scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
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


        _,_, step = scheme(**kwargs)
        count +=1



        sphv_integrated = a.sphv_iter.copy()
        sphv_integrated.integrate_peaks(mask_vol=sphv_targ, dpix=2)

        plt.figure()
        plt.scatter(sphv_targ.vol[sphv_targ.vol>0]/sphv_targ.vol.sum(),
                    sphv_integrated.vol[sphv_targ.vol>0]/sphv_integrated.vol.sum(), c=np.where(sphv_targ.vol>0)[1], cmap='seismic')
        plt.plot([0, sphv_targ.vol.max()/sphv_targ.vol.sum()], [0, sphv_targ.vol.max()/sphv_targ.vol.sum()])

        plt.title(f'Itarg vs Icalc (Coloured by Theta) count:{count}')
        plt.xlabel('Itarg')
        plt.ylabel('Icalc')
        plt.colorbar()
        plt.savefig(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/plots/ItargIcalc_{tag}_{sub_tag}_count{count}.png')
        a.sphv_iter.plot_slice(0, 140, title=f'q shell=140, count={count}', xlabel='phi', ylabel='theta')
        plt.savefig(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/plots/aiter140_{tag}_{sub_tag}_count{count}.png')

        a.sphv_iter.plot_slice(0, 63, title=f'q shell=63, count={count}', xlabel='phi', ylabel='theta')
        plt.savefig(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/plots/aiter63_{tag}_{sub_tag}_count{count}.png')


  #       iqlm_x = a.iqlm_iter.copy()
        # iqlm_x.set_val(140,0,0,0)
        # iqlm_x.plot_q(140)
        # plt.savefig(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/plots/iqlm_q140_{tag}_{sub_tag}_count{count}.png')



        plt.close('all')

        step_file = open(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/steps_{tag}_{sub_tag}.txt','a')
        step_file.write(f'{step},\t\t#{tag}_{sub_tag}_{count}\n')
        step_file.close()

        rfactor_file = open(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/rfactor_{tag}_{sub_tag}.txt','a')
        rf = scorpy.utils.rfactor(sphv_integrated.vol/sphv_integrated.vol.sum(), sphv_targ.vol/sphv_targ.vol.sum())
        rfactor_file.write(f'{rf},\t\t#{tag}_{sub_tag}_{count}\n')
        rfactor_file.close()

        dist_file = open(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/dist_{tag}_{sub_tag}.txt','a')
        dist = np.linalg.norm( np.abs( sphv_targ.vol - sphv_integrated.vol))
        dist_file.write(f'{dist},\t\t#{tag}_{sub_tag}_{count}\n')
        dist_file.close()

        a.sphv_iter.save(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')



a.sphv_iter.save(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')



print(f'Finished: {time.asctime()}')
print()





