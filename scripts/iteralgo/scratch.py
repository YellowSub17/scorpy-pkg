#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





# Parameters



cif1 = scorpy.CifData(f'{scorpy.DATADIR}/cifs/1vds-full-sf.cif', qmax=1)

cif1.save(f'{scorpy.DATADIR}/cifs/1vds-qmax1-sf.cif')
cif1.save_hkl(f'{scorpy.DATADIR}/cifs/1vds-qmax1-sf.hkl')














