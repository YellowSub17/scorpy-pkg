from xfelcorrel import *
import numpy as np








def write_file(name='ccc',\
               a=1,b=1,c=1, \
               alpha=90,beta=90,gamma=90,
               space_group='P 1',\
               h_max=10,k_max=10,l_max=10):

    # Initialize file with settings
    fname = f'data/xtal/{name}-sf.cif'

    file = open(fname, 'w')

    file.write(f'data_{name}sf\n')
    file.write(f'#\n')
    file.write(f'#\n')
    file.write(f'_cell.entry_id\t{name}\n')
    file.write(f'_cell.length_a\t{a}\n')
    file.write(f'_cell.length_b\t{b}\n')
    file.write(f'_cell.length_c\t{c}\n')
    file.write(f'_cell.angle_alpha\t{alpha}\n')
    file.write(f'_cell.angle_beta\t{beta}\n')
    file.write(f'_cell.angle_gamma\t{gamma}\n')
    file.write(f'#\n')
    file.write(f'#\n')
    file.write(f'_entry.id\t{name}\n')
    file.write(f'#\n')
    file.write(f'_exptl_crystal.id\t1\n')
    file.write(f'#\n')
    file.write(f'_reflns_scale.group_code\t1\n')
    file.write(f'#\n')
    file.write(f'_symmetry.entry_id\t{name}\n')
    file.write(f'_symmetry.space_group_name_H-M\t\'{space_group}\'\n')
    file.write(f'#\n')
    file.write(f'#\n')
    file.write(f'loop_\n')
    file.write(f'_refln.index_h\n')
    file.write(f'_refln.index_k\n')
    file.write(f'_refln.index_l\n')
    file.write(f'_refln.intensity_meas\n')




    # range of indices that span +/- max index
    h_range = range(-h_max, h_max+1)
    k_range = range(-k_max, k_max+1)
    l_range = range(-l_max, l_max+1)

    # cartesian product of sets of points for hkl
    points = itertools.product(h_range,k_range,l_range)

    # make the generator object points into a list
    miller_refls = np.array([list(i) for i in points])


    ccc_loc = np.where(miller_refls==miller_refls)

    # bcc: sum of hkl must be even
    bcc_loc = np.where(np.sum(miller_refls, axis=1)%2 ==0)


    # fcc: all of hkl must be odd or even
    fcc_even_cond = np.all(miller_refls%2==0, axis=1)
    fcc_odd_cond = np.all(miller_refls%2==1, axis=1)
    fcc_loc = np.where(fcc_even_cond + fcc_odd_cond)


    # select fcc or bcc reflections
    if name=='fcc':
        loc = fcc_loc  # write reflections to file
        for refl in miller_refls[loc]:
            file.write(f'{refl[0]}\t{refl[1]}\t{refl[2]}\t1\n')


    elif name=='bcc':
        loc = bcc_loc
        for refl in miller_refls[loc]:
            file.write(f'{refl[0]}\t{refl[1]}\t{refl[2]}\t1\n')
    else:
        # write reflections to file
        for refl in miller_refls:
            file.write(f'{refl[0]}\t{refl[1]}\t{refl[2]}\t1\n')


    file.close()













for i in range(100):
    print(i)



    a=1+i*0.01
    b=1
    c=1

    write_file('fcc', a=a, b=b, c=c)
    qmax=6


    ccc_cif = CifData(f'data/xtal/fcc-sf.cif')
    ccc_correl = CorrelationVol(256, 360,qmax)
    ccc_correl.correlate(ccc_cif.scattering)
    ccc_q1q2 = ccc_correl.getq1q2()




    fig, ax = plt.subplots(1,1)
    plt.suptitle(f'a={a}, b={b}, c={c}')

    ax.imshow(np.log10(ccc_q1q2+1), cmap='hot', origin='lower', aspect='auto', extent=[0,180,0,ccc_correl.qmax])
    ax.set_title('FCC')
    ax.set_xlabel('$\\theta$')
    ax.set_ylabel('q1=q2')

    fig.savefig(f'data/saved_plots/fcc/{i}.png')
    plt.close('all')






plt.show()







