#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import os
plt.close('all')




# plt.figure()

# plt.ylabel('Rf')
# plt.xlabel('iteration')

# a = scorpy.AlgoHandler('bbceap-ag-obs')
# counts = [i for i in range(0, 352, 4)]
# rfs = []
# for count in counts:
    # print(count)
    # rfs.append(a.get_rf('a', count=count))
# plt.plot(counts, rfs, 'r.', label=a.tag)





# a = scorpy.AlgoHandler('bbceap-ag')
# counts = [i for i in range(0, 118, 4)]
# counts += [i for i in range(120, 700, 20)]
# rfs = []
# for count in counts:
    # print(count)
    # rfs.append(a.get_rf('a', count=count))
# plt.plot(counts, rfs, 'g.', label=a.tag)


# a = scorpy.AlgoHandler('triclinic')
# counts = [i for i in range(0, 118, 4)]
# counts += [i for i in range(120, 700, 20)]
# rfs = []
# for count in counts:
    # print(count)
    # rfs.append(a.get_rf('a', count=count))
# plt.plot(counts, rfs, 'b.', label=a.tag)

# plt.legend()









# plt.figure()
# plt.ylabel('Rf')
# plt.xlabel('iteration')

# a = scorpy.AlgoHandler('tbcampmamp')
# counts = [i for i in range(0, 200, 1)]
# counts += [i for i in range(200, 700, 20)]
# rfs = []
# for count in counts:
    # print(count)

    # rfs.append(a.get_rf('a', count=count))
# plt.plot(counts, rfs, 'b.', label=a.tag)


# a = scorpy.AlgoHandler('tetracyclinehydrochloride')
# counts = [i for i in range(0, 300, 4)]
# rfs = []
# for count in counts:
    # print(count)
    # rfs.append(a.get_rf('a', count=count))
# plt.plot(counts, rfs, 'r.', label=a.tag)

# plt.legend()




# a = scorpy.AlgoHandler('bbceap-ag-obs')


# a.intensity_xy_plot('dm', count=0)
# a.intensity_xy_plot('dm', count=4)
# a.intensity_xy_plot('dm', count=8)
# a.intensity_xy_plot('dm', count=9)
# a.intensity_xy_plot('dm', count=10)





# qq = 99

# a = scorpy.AlgoHandler('triclinic')
# sphv_iter = scorpy.SphericalVol(path=a.sphv_iter_path('a'))
# sphv_iter.plot_slice(0, qq)

# sphv_init= scorpy.SphericalVol(path=a.sphv_init_path('a'))
# sphv_init.plot_slice(0, qq)

# sphv_init= scorpy.SphericalVol(path=a.sphv_supp_loose_path())
# sphv_init.plot_slice(0, qq)



# a = scorpy.AlgoHandler('agno3-random-starts')

# counts = [i for i in range(0, 111)]
# plt.figure()

# for sub_tag in 'abcde':
    # # a.run_shelxl(sub_tag)
    # # a.run_shelxl(sub_tag, count='targ')

    # rfs = []
    # for count in counts:
        # print(sub_tag, count)
        # # a.run_shelxl(sub_tag, count=count)

        # rf = a.get_rf(sub_tag, count=count)
        # rfs.append(rf)

    # plt.plot(counts, rfs, marker='.', ls='', label=sub_tag)

# plt.legend()
# plt.xlabel('iteration')
# plt.ylabel('Rf (shelx)')








# fig, axes = plt.subplots(2,2)

# a = scorpy.AlgoHandler('agno3-nl180')
# a.intensity_xy_plot('a', fig=fig, axes=axes[0,0], title=a.tag)

# a = scorpy.AlgoHandler('agno3-nl150')
# a.intensity_xy_plot('a', fig=fig, axes=axes[0,1], title=a.tag)

# a = scorpy.AlgoHandler('agno3-nl120')
# a.intensity_xy_plot('a', fig=fig, axes=axes[1,0], title=a.tag)

# a = scorpy.AlgoHandler('agno3-nl90')
# a.intensity_xy_plot('a', fig=fig, axes=axes[1,1], title=a.tag)





nls = [180, 165, 150, 135, 120, 105, 90, 75, 60]

colors = cm.jet(np.linspace(0, 1, len(nls)))

counts = [i for i in range(0, 111, 1)]


plt.figure()
for color, nl in zip(colors, nls):
    a = scorpy.AlgoHandler(f'agno3-nl{nl}')
    rfs = []
    for count in counts:
        print(nl, 'a', count, end= '\r')
        rf = a.get_rf('a', count=count)
        rfs.append(rf)
    print('')
    plt.plot(counts,  rfs, marker='.', ls='', label=f'{nl}')
plt.xlabel('Iteration')
plt.ylabel('Rf (shelx)')
plt.legend()





nls = [180, 120, 90, 60]
sub_tags = ['a','b','c','d']

colors = cm.jet(np.linspace(0, 1, len(sub_tags)))

counts = [i for i in range(0, 111, 1)]

for nl in nls:
    a = scorpy.AlgoHandler(f'agno3-nl{nl}')
    plt.figure()
    for color, sub_tag in zip(colors, sub_tags):
        rfs = []
        for count in counts:
            print(nl, sub_tag, count, end= '\r')
            rf = a.get_rf(sub_tag, count=count)

            rfs.append(rf)
        print('')

        plt.plot(counts,  rfs, marker='.', ls='', label=f'{sub_tag}')

    plt.title(f'nl{nl}')
    plt.xlabel('Iteration')
    plt.ylabel('Rf (shelx)')
    plt.legend()













plt.show()














