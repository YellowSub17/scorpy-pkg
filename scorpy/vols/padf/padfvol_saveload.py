
from pathlib import Path

import configparser as cfp
from datetime import datetime
import numpy as np



class PadfVolSaveLoad:
 
    def _save_extra(self, f):
        f.write('[padf]\n')
        f.write(f'rmax = {self.rmax}\n')
        f.write(f'psimax = {np.pi}\n')
        f.write(f'nr = {self.nr}\n')
        f.write(f'npsi = {self.npsi}\n')
        f.write(f'dr = {self.dr}\n')
        f.write(f'dpsi = {self.dpsi}\n')
        f.write(f'nl = {self.nl}\n')
        f.write(f'wavelength = {self.wavelength}\n')

    def _load_extra(self, config):

        self._nl = float(config['padf']['nl'])
        self._wavelength = float(config['padf']['wavelength'])



