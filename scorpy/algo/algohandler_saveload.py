






class AlgoHandlerSaveLoad:


    def _read_log(self, fpath):
        '''
        '''
        assert type(fpath) == str, 'Argument fpath must be string'
        path = Path(fpath)


        parent = path.parent
        stem = path.stem
        ftype = path.suffix


        config = cfp.ConfigParser()
        config.read(f'{parent}/{stem}.log')


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






    def save(self, fpath):
        """
        scorpy.Vol.save(path):
            Save the current Vol to a dbin/npy/h5 array and log file.
        Arguments:
            path: path of the save location with file tag. The filename should exclude filetype.
        """


        path = Path(fpath)

        parent = path.parent
        stem = path.stem
        ftype = path.suffix

        assert path.suffix != '', 'Path now requires file type (npy or dbin)'

        if path.suffix == '.dbin':
            # write dbin
            flat_vol = self.vol.flatten()
            flat_vol.tofile(f'{path.parent}/{path.stem}.dbin')

        if path.suffix == '.npy':
            np.save(f'{path.parent}/{path.stem}.npy', self.vol)
        
        self.write_log(fpath)

    def write_log(self, fpath):

        path = Path(fpath)

        parent = path.parent
        stem = path.stem
        ftype = path.suffix


        # write log
        f = open(f'{parent}/{stem}.log', 'w')
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




    pass
