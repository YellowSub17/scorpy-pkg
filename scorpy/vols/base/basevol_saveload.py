
from pathlib import Path

import configparser as cfp
from datetime import datetime
import numpy as np



class BaseVolSaveLoad:


    def _read_log(self, fpath):


        fpath = Path(fpath)

        logpath = Path(fpath.parent) / f'{fpath.stem}.log'

        config = cfp.ConfigParser()
        config.read(logpath)


        self._nx = int(config['vol']['nx'])
        self._ny = int(config['vol']['ny'])
        self._nz = int(config['vol']['nz'])

        self._xmin = float(config['vol']['xmin'])
        self._ymin = float(config['vol']['ymin'])
        self._zmin = float(config['vol']['zmin'])

        self._xmax = float(config['vol']['xmax'])
        self._ymax = float(config['vol']['ymax'])
        self._zmax = float(config['vol']['zmax'])

        self._xwrap = config.getboolean('vol', 'xwrap')
        self._ywrap = config.getboolean('vol', 'ywrap')
        self._zwrap = config.getboolean('vol', 'zwrap')

        self._comp = config.getboolean('vol', 'comp')
        self._load_extra(config)

    def _load(self, fpath, logpath=None):
        # print('loading')

        fpath = Path(fpath)

        assert fpath.is_file(), f'File {fpath} not found'

        if logpath is None:
            self._read_log(fpath)
        else:
            self._read_log(logpath)



        if fpath.suffix =='.dbin':

            if self.comp:
                file_vol = np.fromfile(fpath, dtype=np.complex64)
            else:
                file_vol = np.fromfile(fpath)


            # print(file_vol)
            self._vol = file_vol.reshape((self.nx, self.ny, self.nz))


        elif fpath.suffix =='.npy':
            coo_arr = np.load(fpath)
            self._vol = np.zeros( (self.nx, self.ny, self.nz) )
            xi, yi, zi = coo_arr[:,0].astype(int), coo_arr[:,1].astype(int),coo_arr[:,2].astype(int),
            self._vol[xi, yi, zi] = coo_arr[:,-1]

            





    def save(self, fpath):

        fpath = Path(fpath)


        if fpath.suffix == '.dbin':
            flat_vol = self.vol.flatten()
            flat_vol.tofile(fpath)

        elif fpath.suffix == '.npy':

            coo_loc = np.where(self.vol>0)
            # coo_arr = np.zeros( (coo_loc[0].shape[0], 4) )
            coo_arr = np.array( [ coo_loc[0], coo_loc[1], coo_loc[2], self.vol[coo_loc] ]).T

            np.save(fpath, coo_arr)




        
        self.write_log(fpath)

    def write_log(self, fpath):

        fpath = Path(fpath)


        logpath = Path(fpath.parent) / f'{fpath.stem}.log'

        # write log
        f = open(logpath, 'w')
        f.write('##Scorpy Vol Config File\n')
        f.write(f'## Created: {datetime.now().strftime("%Y/%m/%d %H:%M")}\n\n')
        f.write('[vol]\n')
        f.write(f'nx = {self.nx}\n')
        f.write(f'ny = {self.ny}\n')
        f.write(f'nz = {self.nz}\n')
        f.write(f'xmin = {self.xmin}\n')
        f.write(f'ymin = {self.ymin}\n')
        f.write(f'zmin = {self.zmin}\n')
        f.write(f'xmax = {self.xmax}\n')
        f.write(f'ymax = {self.ymax}\n')
        f.write(f'zmax = {self.zmax}\n')
        f.write(f'xwrap = {self.xwrap}\n')
        f.write(f'ywrap = {self.ywrap}\n')
        f.write(f'zwrap = {self.zwrap}\n')
        f.write(f'dx = {self.dx}\n')
        f.write(f'dy = {self.dy}\n')
        f.write(f'dz = {self.dz}\n')
        f.write(f'comp = {self.comp}\n')
        f.write('\n')
        self._save_extra(f)
        f.close()





    def _save_extra(self, f):

        pass

    def _load_extra(self, config):

        pass



