

import regex as re


def strerr2floaterrr(s):

    val, err = s.split('(')[0], s.split('(')[1][:-1]

    units = val.split('.')[0]
    # print(units)

    if units==val:
        err= float(err)
    else:
        ndeci = len(val.split('.')[1])
        err = float('0.'+(ndeci-1)*'0'+'1')*float(err)


    return float(val), float(err)






def concat_file(f):
    # print(f'Concantenating file: {f}')
    single_file_str = ''
    with open(f, 'r') as f:
        for line in f:
            single_file_str +=line

    return single_file_str




def grep(s, reg, fn=None):
    # print(f'greping reg: {reg}')
    found = re.findall(reg, s)
    if fn is not None:
        found = list(map(fn, found))
    return found



