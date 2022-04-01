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



tag = 'nacl'


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

cif_targ = scorpy.CifData(path=f'{scorpy.DATADIR}/algo/{tag}/{tag}_targ-sf.cif')



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

        cif_f = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/nacl.cif', rotk=[1,1,1], rottheta=np.radians(30))
        cif_f.fill_from_sphv(sphv_integrated, bragg_xyz=cif_targ.scat_bragg[:,:3])


        plt.figure()
        plt.scatter(cif_targ.scat_bragg[:,-1]/cif_targ.scat_bragg[:,-1].sum(),
                    cif_f.scat_bragg[:,-1]/cif_f.scat_bragg[:,-1].sum(), c=cif_targ.scat_sph[:,1])
        plt.xlabel('Itarg')
        plt.ylabel('Ialgo')
        plt.plot( [0,cif_targ.scat_bragg[:,-1].max()/cif_targ.scat_bragg[:,-1].sum() ],
                  [0,cif_targ.scat_bragg[:,-1].max()/cif_targ.scat_bragg[:,-1].sum()])
        cb = plt.colorbar()
        cb.set_label('theta')

        plt.savefig(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/plots/ItargIcalc_{tag}_{sub_tag}_count{count}.png')

        plt.close('all')

        step_file = open(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/steps_{tag}_{sub_tag}.txt','a')
        step_file.write(f'{step},\t\t#{tag}_{sub_tag}_{count}\n')
        step_file.close()

        rfactor_file = open(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/rfactor_{tag}_{sub_tag}.txt','a')
        rf = cif_f.rfactor(cif_targ)
        rfactor_file.write(f'{rf},\t\t#{tag}_{sub_tag}_{count}\n')
        rfactor_file.close()


        a.sphv_iter.save(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')



a.sphv_iter.save(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')

# sphv_integrated = a.sphv_iter.copy()
# sphv_integrated.integrate_peaks(mask_vol=sphv_targ, dpix=2)
# cif_f = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/nacl.cif', rotk=[1,1,1], rottheta=np.radians(30))
# cif_f.fill_from_sphv(sphv_integrated, bragg_xyz=cif_targ.scat_bragg[:,:3])



print(f'Finished: {time.asctime()}')
print()





