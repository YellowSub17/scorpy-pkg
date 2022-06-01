
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')


import scorpy





fig, axes = plt.subplots(1,1, )



tag = 'agno3-d03'

sub_tags = 'abc'





a = scorpy.AlgoHandler(tag)
targ_vals, _ = a.get_geometry_vals(sub_tags[0], count='targ', geometry='angles')

vals, errs = [], []

for sub_tag in sub_tags:
    print(sub_tag)
    aval, aerr =  a.get_geometry_vals(sub_tag, geometry='angles')

    vals.append(aval)
    errs.append(aerr)

algo_vals = np.mean(vals, axis=0)
algo_errs = np.std(vals, axis=0)
shelx_errs = np.mean(errs, axis=0)

total_errs = algo_errs + shelx_errs


a._plot_errorbar(targ_vals, algo_vals, 0, 1*total_errs,
                    xlabel=f'Target Distance',  ylabel=f'Algo Distances',
                capsize=2, fig=fig, axes=axes)



axes.plot([targ_vals.min(), targ_vals.max()],[targ_vals.min(), targ_vals.max()], 'k-.')

plt.show()




