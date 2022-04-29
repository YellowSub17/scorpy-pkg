



import scorpy
import numpy as np
import sys






tag = f'agno3-d05'
recipe_path = scorpy.DATADIR / 'algo'/ 'RECIPES' / 'HIO120.txt'
a = scorpy.AlgoHandler(tag)

for sub_tag in 'abcdef':
    a.check_inputs()
    a.run_recon(sub_tag, f'{recipe_path}', verbose=99)





















