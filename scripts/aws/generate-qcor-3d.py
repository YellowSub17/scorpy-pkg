

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import subprocess
import h5py
import scipy as sp
import time

corr = scorpy.CorrelationVol(nq=256, npsi=360, qmax=1.5, qmin=0.2, cos_sample=False)


cif = scorpy.CifData('/home/ec2-user/corr/data/xtal/193l-sf.cif', qmax=1.5)

corr.fill_from_cif(cif, verbose=99)

corr.save('/home/ec2-user/corr/data/qcor/193l-3d-qcor.dbin')









