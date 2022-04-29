



import scorpy
import numpy as np
import sys






tag = f'agno3-rec'
a = scorpy.AlgoHandler(tag)

rec_fname = sys.argv[1]
a.check_inputs()
a.run_recon(rec_fname, f'{scorpy.DATADIR}/algo/RECIPES/{rec_fname}.txt', verbose=99)





















