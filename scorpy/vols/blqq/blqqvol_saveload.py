
from pathlib import Path

import configparser as cfp
from datetime import datetime
import numpy as np



class BlqqVolSaveLoad:



    def _save_extra(self, f):
        f.write('[blqq]\n')
        f.write(f'qmax = {self.qmax}\n')
        f.write(f'nq = {self.nq}\n')
        f.write(f'nl = {self.nl}\n')
        f.write(f'dq = {self.dq}\n')
        f.write(f'inc_odds = {self.inc_odds}\n')


    def _load_extra(self, config):
        self._inc_odds = config.getboolean('blqq', 'inc_odds')



