



import scorpy
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil


#read the last shelx results for subtags and averages the atomic positions



tag = 'aluminophosphate-d05'
meansubtag = 'means'



a = scorpy.AlgoHandler(tag)


subtags = 'abcdefgh'


mean_final_sphv = scorpy.SphericalVol(a.nq, a.nl*2, a.nl*4, a.qmax)

for subtag in subtags:
    print('subtag', subtag)

    sub_final_sphv = scorpy.SphericalVol(path=a.sphv_final_path(subtag))
    print(sub_final_sphv.vol.max())
    mean_final_sphv.vol += sub_final_sphv.vol





mean_final_sphv.vol /= len(subtags)


if not os.path.exists(f'{a.path}/{meansubtag}/'):
    os.mkdir(f'{a.path}/{meansubtag}/')

mean_final_sphv.save(f'{a.path}/{meansubtag}/sphv_{tag}_{meansubtag}.dbin')


cif_integrated = scorpy.CifData(a.cif_targ_path(), rotk=a.rotk, rottheta=a.rottheta)
cif_integrated.fill_from_sphv(mean_final_sphv)
cif_integrated.save(f'{a.path}/{meansubtag}/{tag}_{meansubtag}-sf.cif')


if not os.path.exists(f'{a.path}/{meansubtag}/shelx/'):
    os.mkdir(f'{a.path}/{meansubtag}/shelx/')
cif_integrated.save_hkl(f'{a.path}/{meansubtag}/shelx/{tag}_{meansubtag}.hkl')

shutil.copyfile(f'{a.path}/{a.tag}.ins', f'{a.path}/{meansubtag}/shelx/{tag}_{meansubtag}.ins' )






cwd = os.getcwd()
os.chdir(f'{a.path}/{meansubtag}/shelx/')
os.system(f'shelxl {a.tag}_{meansubtag} > shelxl.log')

os.chdir(f'{cwd}')


























