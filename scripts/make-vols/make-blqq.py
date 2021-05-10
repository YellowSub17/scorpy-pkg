#!/usr/bin/env python3
'''
make-blqq.py

Make blqq vol objects.
'''

import scorpy
import numpy as np
np.random.seed(0)


names  = ['1al1']
nl = 11


# MAKE BLQQ FROM CIF CORRELATION
for name in names:
    cor = scorpy.CorrelationVol(path=f'../data/dbins/{name}_qcor')
    bl = scorpy.BlqqVol(nq=cor.nq, nl=nl, qmax=cor.qmax)

    bl.fill_from_corr(cor)

    bl.save_dbin(f'../data/dbins/{name}_blqq')
