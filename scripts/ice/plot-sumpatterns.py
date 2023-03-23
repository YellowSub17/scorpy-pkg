

import numpy as np
import matplotlib.pyplot as plt






sizes=['1000nm', '500nm', '250nm', '125nm']

fig, axes = plt.subplots(2,2, sharex=True, sharey=True, figsize=(16/2.54, 16/2.54))


for i_size, size in enumerate(sizes):
    im = np.zeros( (1000,1000) )

    for i in range(4):
        p = np.load(f'/media/pat/datadrive/ice/sim/patterns/sums/hex-ice-{size}-19MPz18-10k-{i}.npy')
        im+=p

    axes.flatten()[i_size].imshow(im, clim=(0,1000000))

    axes.flatten()[i_size].set_title(f'{size}')

plt.tight_layout()
plt.show()


