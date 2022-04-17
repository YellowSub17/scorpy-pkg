



import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')






# qmax = 9
# nq = 100
# npsi = 360*32
# nl = 180

# rotk = [1,1,1]
# rottheta = np.radians(30)


tag = 'copy-time-test'
# sample = 'nacl'



# targ_ciffname = f'{scorpy.DATADIR}/xtal/{sample}/{sample}-sf.cif'
# targ_insfname = f'{scorpy.DATADIR}/xtal/{sample}/{sample}.ins'
# supp_ciffname= f'{scorpy.DATADIR}/xtal/{sample}/{sample}.cif'




# a = scorpy.AlgoHandler(tag=tag, nq=nq, qmax=qmax, npsi=npsi, nl=nl, rotk=rotk, rottheta=rottheta)
# a.make_target(targ_ciffname, targ_insfname, verbose=99)
# a.make_support(supp_ciffname, verbose=99)



# # a = scorpy.AlgoHandler(tag)
# # sphv_suppl = scorpy.SphericalVol(path=f'{a.path}/sphv_{a.tag}_supp_loose.dbin')
# # sphv_suppt = scorpy.SphericalVol(path=f'{a.path}/sphv_{a.tag}_supp_tight.dbin')

# # plt.figure()
# # plt.plot(sphv_suppt.vol.sum(axis=-1).sum(axis=-1))

# # sphv_suppl.plot_slice(0, 248)
# # sphv_suppt.plot_slice(0, 248)



# a.make_data(verbose=99)




a = scorpy.AlgoHandler(tag=tag)
a.run_recon('b', f'{scorpy.DATADIR}/algo/RECIPES/rec.txt', verbose=99)






















plt.show()

