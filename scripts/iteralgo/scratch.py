



import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')






qmax = 9
nq = 100
npsi = 360*32
nl = 180

rotk = [1,1,1]
rottheta = np.radians(30)


tag = 'triclinic'
sample = 'agno3'



targ_ciffname = f'{scorpy.DATADIR}/xtal/{sample}/{sample}-sf.cif'
targ_insfname = f'{scorpy.DATADIR}/xtal/{sample}/{sample}.ins'
supp_ciffname= f'{scorpy.DATADIR}/xtal/{sample}/{sample}.cif'




a = scorpy.AlgoHandler(tag=tag, nq=nq, qmax=qmax, npsi=npsi, nl=nl, rotk=rotk, rottheta=rottheta)
a.make_target(targ_ciffname, targ_insfname, verbose=99)
a.make_support(supp_ciffname, verbose=99)



# sphv_supp = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp_loose.dbin')
# sphv_targ = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')

# plt.figure()
# plt.plot(sphv_supp.vol.sum(axis=-1).sum(axis=-1))

# plt.figure()
# plt.plot(sphv_targ.vol.sum(axis=-1).sum(axis=-1))


# qloc = np.unique((np.where(sphv_targ.vol>0))[0])


# qq = 25
# sphv_supp.plot_slice(0, qloc[0])
# sphv_supp.plot_slice(0, qq)
# sphv_supp.plot_sumax(0)


a.make_data(verbose=99)



# a = scorpy.AlgoHandler(tag=tag)
a.run_recon('a', f'{scorpy.DATADIR}/algo/RECIPES/rec.txt', verbose=99)



a = scorpy.AlgoHandler(tag=tag)
a.integrate_final('a')
# a.It_vs_Ia('a')

a.prep_shelxl('a')























plt.show()

