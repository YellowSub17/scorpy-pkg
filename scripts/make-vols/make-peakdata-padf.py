
import numpy as np
import scorpy

# p = scorpy.PadfVol(600,360,60)

# p.fill_from_corr('../data/dbins/3wct_qcor.dbin', nl=33)


runs150 = [112,123,113,125,102,103,104,105]
runs144 = [118,108,119,109,120,110,121]
runs = runs150+runs144


for run in runs[:1]:
    padf = scorpy.PadfVol(250,360,15)
    cor = scorpy.CorrelationVol(path=f'../data/dbins/cosine_sim/{run}/run{run}_qcor')

    padf.fill_from_corr(f'../data/dbins/cosine_sim/{run}/run{run}_qcor.dbin', nl=96)




