



import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')














cif = scorpy.CifData(f'{scorpy.DATADIR}/xtal/test.cif', rotk=[1,1,1], rottheta=np.radians(30))




# x = np.array([
      # [ 0, 0, 1],
      # [ 0, 1, 0],
      # [ 1, 0, 0],
      # [ 1, 1, 1],
      # [ 0, 2, 0],
    # ])

# y = np.array([
      # [ 0, 0, 1],
      # [ 0, 1, 0],
      # [ 1, 0, 0],
      # [ 1, 1, 1],
      # [ 0, 0, 2],
      # [ 0, 2, 0],
      # [ 2, 0, 0],
      # [ 2, 2, 2],
    # ])



# for pty in y:
    # print( np.where((x == pty).all(axis=1)))
# # np.where((vals == (0, 1)).all(axis=1))

# for pt in y:
    # if np.all(pt in x):
        # print('y', pt)
    # else:
        # print('n', pt)



# cif.fill_from_vhkl(f'{scorpy.DATADIR}/xtal/nacl/nacl.vhkl')




