



import scorpy
import sys



tag = sys.argv[1]
sub_tag= sys.argv[2]

a = scorpy.AlgoHandler(tag)
a.run_recon(sub_tag, f'{scorpy.DATADIR}/algo/RECIPES/HIOER110.txt', verbose=99)














