



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
exps_raw = scorpy.utils.utils.grep(s, r'(?<=[AGSONC]+\d+.*)(-?\d+\.\d+)|((?<=\s{9}.*)(?<!W.*)-?\d\.\d+)', fn=None)
# exps_raw = scorpy.utils.utils.grep(s, r'(?<=[PAlONC]+\d+.*)(-?\d+\.\d+)|((?<=\s{9}.*)(?<!W.*)-?\d\.\d+)', fn=None)


## for each expression, get the float
exps = []
for exp in exps_raw:
    if exp[0] == '':
        exps.append(float(exp[1]))
    else:
        exps.append(float(exp[0]))



## initialize array to store structre values
value_storage = np.zeros( (len(subtags), len(exps)))



#repeat for each subtag
for subtag_i, subtag in enumerate(subtags):
    print(subtag)
#do first to work out lengths
    final_res_file = f'{scorpy.DATADIR}/algo/{tag}/{subtag}/shelx/{tag}_{subtag}.res'


    s = scorpy.utils.utils.concat_file(final_res_file)
    exps_raw = scorpy.utils.utils.grep(s, r'(?<=[AGSONC]+\d+.*)(-?\d+\.\d+)|((?<=\s{9}.*)(?<!W.*)-?\d\.\d+)', fn=None)
    # exps_raw = scorpy.utils.utils.grep(s, r'(?<=[PAlONC]+\d+.*)(-?\d+\.\d+)|((?<=\s{9}.*)(?<!W.*)-?\d\.\d+)', fn=None)

    exps = []

    for exp in exps_raw:
        if exp[0] == '':
            exps.append(float(exp[1]))
        else:
            exps.append(float(exp[0]))


    value_storage[subtag_i,:] = exps


#average the strcutres
mean_struct = value_storage.mean(axis=0)



#get atoms
atoms_exps = scorpy.utils.utils.grep(s, r'[ABCDEFGHIJKLMNOPRSTUVWXYZ]+\d+\s+\d', fn=None)


print(atoms_exps)





for atom_i, atom in enumerate(atoms_exps):

    first_line = f'{atom}'
    for value_i in range(3):
        first_line += '%12.6f' %mean_struct[10*atom_i+value_i]
    
    first_line+=' '
    for value_i in range(3):
        first_line += '%11.5f' %mean_struct[10*atom_i+value_i+3]
    first_line +=' ='

    second_line = ' '*5
    for value_i in range(4):
        second_line += '%11.5f' %mean_struct[10*atom_i+value_i+6]



    print(first_line)
    print(second_line)

















