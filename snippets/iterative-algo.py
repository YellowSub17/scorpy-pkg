



import scorpy
import matplotlib.pyplot as plt
import timeit

cif1 = scorpy.CifData('../data/xtal/worm_hemo/3wct-sf.cif')
cif = scorpy.CifData('../data/xtal/1al1-sf.cif')


# # iv = scorpy.SphInten(200,2**7, qmax=cif.qmax)

# # iv.fill_from_cif(cif)
# # iv.plot_sphere(50)




# sph = scorpy.SphHarmHandler(100,15,cif.qmax)
# sph.fill_from_cif(cif)



# plt.figure()
# plt.plot(sph.vals_lnm[0])
# plt.figure()
# plt.plot(sph.vals_lnm[2][:,0])
# plt.show()
# # iv.fill_from_sph(sph)

# iv.plot_sphere(50)

# plt.show()

# for q_ind, pixel, inten in zip(q_inds, pixels, cif.spherical[:,-1]):
            # self.ivol[q_ind, pixel] += inten

