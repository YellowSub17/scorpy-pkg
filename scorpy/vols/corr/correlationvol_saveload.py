

class CorrelationVolSaveLoad:

    def _save_extra(self, f):
        f.write('[corr]\n')
        f.write(f'qmax = {self.qmax}\n')
        f.write(f'nq = {self.nq}\n')
        f.write(f'npsi = {self.npsi}\n')
        f.write(f'dq = {self.dq}\n')
        f.write(f'dpsi = {self.dpsi}\n')
        f.write(f'cos_sample = {self.cos_sample}\n')

    def _load_extra(self, config):
        self._cos_sample = config.getboolean('corr', 'cos_sample')



