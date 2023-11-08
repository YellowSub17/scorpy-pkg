

import numpy as np
import matplotlib.pyplot as plt


import glob




sizes = ['1000nm', '500nm', '250nm', '125nm']


# stds = [-99900 ]
# stds += [i for i in range(0, 151, 25)]

stds = [i for i in range(0, 151, 25)]



for size in sizes:

    im = np.zeros( (1000, 1000) )
    for std_i, std in enumerate(stds[:-1]):

        p = np.load(f'/media/pat/datadrive/ice/sim/patterns/sums/hex-ice-{size}-std{std}-{stds[std_i+1]}-a.npy')
        im +=p
    print(im.max())

    plt.figure(figsize=(8/2.54, 8/2.54), dpi=300)
    plt.imshow(np.log10(im+1))
    # plt.colorbar()
    plt.tight_layout()
    plt.title(f'{size}, {im.max():.2g}')

# plt.savefig('/home/pat/Documents/phd/figs/ice/ice-sumpattern.png')
plt.show()





