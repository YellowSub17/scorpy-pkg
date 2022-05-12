



import scorpy
import numpy as np
import sys






tag = f'agno3-d07'
recipe_path = scorpy.DATADIR / 'algo'/ 'RECIPES' / 'HIO120.txt'
a = scorpy.AlgoHandler(tag)

a.check_inputs()
a.run_recon('a', f'{recipe_path}', verbose=99)





















