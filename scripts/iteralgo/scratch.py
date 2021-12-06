#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





# Parameters



cif1 = scorpy.CifData(f'{scorpy.DATADIR}/cifs/test.cif')

cif2a = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif')
cif2b = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-rand-sf.cif')







