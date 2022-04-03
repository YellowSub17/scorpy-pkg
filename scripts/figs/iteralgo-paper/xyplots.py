
import scorpy
import numpy as np

import matplotlib.pyplot as plt
plt.close('all')



savetodir = '/home/pat/Documents/cloudstor/phd/writing/iteralgopaper/figs'

tag = 'nacl'
sub_tag = 'testing'



st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
cif_t = scorpy.CifData(path=f'{scorpy.DATADIR}/algo/{tag}/{tag}_targ-sf.cif', rotk=[1,1,1], rottheta=np.radians(30), qmax=9)


sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')

si = sf.copy()
si.integrate_peaks(mask_vol=st, dpix=2)


cif_f = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/nacl/nacl.cif', rotk=[1,1,1], rottheta=np.radians(30))
cif_f.fill_from_sphv(si, bragg_xyz=cif_t.scat_bragg[:,:3])



qs = np.unique(cif_f.scat_sph[:,0])
intens_t = []
intens_ave = []
intens_std = []

for q in qs:
    loc = np.where(cif_f.scat_sph[:,0]==q)

    intensf_loc = cif_f.scat_sph[loc,-1]/np.sum(cif_f.scat_sph[:,-1])
    intens_ave.append(intensf_loc.mean())
    intens_std.append(intensf_loc.std())

    intenst_loc = cif_t.scat_sph[loc,-1]/np.sum(cif_t.scat_sph[:,-1])
    intens_t.append(intenst_loc.mean())










plt.figure()
plt.tight_layout()
plt.scatter(cif_t.scat_bragg[:,-1]/cif_t.scat_bragg[:,-1].sum(),
            cif_f.scat_bragg[:,-1]/cif_f.scat_bragg[:,-1].sum(),color='black',marker='.', label='Bragg Intenisty')
plt.xlabel('Target Intensity')
plt.ylabel('Reconstructed Intensity')
plt.plot( [0,cif_t.scat_bragg[:,-1].max()/cif_t.scat_bragg[:,-1].sum() ],
          [0,cif_t.scat_bragg[:,-1].max()/cif_t.scat_bragg[:,-1].sum()],'k--', label='y=x')


plt.errorbar(intens_t, intens_ave, yerr=intens_std, color='red',marker='x',linestyle='', label='Average')

plt.legend()
plt.title('NaCl')







plt.savefig(f'{savetodir}/nacl-Ia-vs-It.png')


plt.show()













