



import scorpy
import numpy as np


#read the last shelx results for subtags and averages the atomic positions



tag = 'aluminophosphate-d05'
# tag = 'agno3-d03'



a = scorpy.AlgoHandler(tag)

subtags = 'abcdefgh'



# do first subtag to work out lengths

final_res_file = f'{scorpy.DATADIR}/algo/{tag}/{subtags[0]}/shelx/{tag}_{subtags[0]}.res'

s = scorpy.utils.utils.concat_file(final_res_file)
exps = scorpy.utils.utils.grep(s, r'(?<=[PALONC]+\d+.*)(-?\d+\.\d+)', fn=float)



## initialize array to store structre values
value_storage = np.zeros( (len(subtags), len(exps)))



#repeat for each subtag
for subtag_i, subtag in enumerate(subtags):
    print(subtag)
#do first to work out lengths
    final_res_file = f'{scorpy.DATADIR}/algo/{tag}/{subtag}/shelx/{tag}_{subtag}.res'


    s = scorpy.utils.utils.concat_file(final_res_file)
    exps = scorpy.utils.utils.grep(s, r'(?<=[PALONC]+\d+.*)(-?\d+\.\d+)', fn=None)

    value_storage[subtag_i,:] = exps


#average the strcutres
mean_struct = value_storage.mean(axis=0)



#get atoms
atoms_exps = scorpy.utils.utils.grep(s, r'[PALONC]+\d+\s+\d', fn=None)


print(atoms_exps)
print(mean_struct)




for atom_i, atom in enumerate(atoms_exps):

    first_line = f'{atom}'
    for value_i in range(3):
        first_line += '%12.6f' %mean_struct[5*atom_i+value_i]
    
    first_line+=' '
    for value_i in range(2):
        first_line += '%11.5f' %mean_struct[5*atom_i+value_i+3]

 

    print(first_line)

















