
import numpy as np
import matplotlib.pyplot as plt
import copy
import configparser as cfp
from datetime import datetime




from .algohandler_operators import AlgoHandlerOperators
from .algohandler_schemes import AlgoHandlerSchemes
from .algohandler_plot import AlgoHandlerPlot
from .algohandler_paths import AlgoHandlerPaths
from .algohandler_runrecon import AlgoHandlerRunRecon
from .algohandler_setuprecon import AlgoHandlerSetupRecon
from .algohandler_postrecon import AlgoHandlerPostRecon
from .algohandler_shelx import AlgoHandlerShelx
from .algohandler_props import AlgoHandlerProps

# from ..vols.sphv.sphericalvol import SphericalVol
# from ..iqlm.iqlmhandler import IqlmHandler



import os
import shutil
# from pathlib import Path


class AlgoHandler(AlgoHandlerOperators, AlgoHandlerSchemes,
                  AlgoHandlerPaths, AlgoHandlerProps,
                  AlgoHandlerRunRecon, AlgoHandlerSetupRecon, AlgoHandlerPostRecon,
                  AlgoHandlerShelx,
                  AlgoHandlerPlot):




    def __init__(self, tag, path, nq=256, qmax=1, qmin=0, npsi=360*32, nl=180, lcrop=45,
                 dxsupp=2, pinv_rcond=0.1, eig_rcond=1e-15, lossy_iqlm=True, lossy_sphv=True,
                 rotk=[1,1,1], rottheta=np.radians(30), overwrite=0):


        self._tag = tag
        self._path = f'{path}/{tag}'

        self._nq = nq
        self._qmax = qmax
        self._qmin = qmin
        self._npsi = npsi
        self._nl = nl
        self._lcrop = lcrop
        self._dxsupp = dxsupp
        self._pinv_rcond = pinv_rcond
        self._eig_rcond = eig_rcond
        self._lossy_iqlm = lossy_iqlm
        self._lossy_sphv = lossy_sphv
        self._rotk = rotk
        self._rottheta = rottheta




        if not os.path.exists(self.path):
            os.mkdir(f'{self.path}')
            self.save_params()
            return

        elif os.path.exists(self.path) and overwrite==2:
            shutil.rmtree(f'{self.path}')
            os.mkdir(f'{self.path}')
            self.save_params()
            return

        elif os.path.exists(self.path) and overwrite==1:
            print(f'Algo path {self.path} exists. Overwrite? (y/n)')
            query = input('>> ')
            if query=='y':
                shutil.rmtree(f'{self.path}')
                os.mkdir(f'{self.path}')
                self.save_params()
                return
            else:
                self.load_params()

        else:
            self.load_params()







    def save_params(self):
        f = open(self.algo_params_path(), 'w')
        f.write('##Scorpy Algo Config File\n')
        f.write(f'## Created: {datetime.now().strftime("%Y/%m/%d %H:%M")}\n\n')
        f.write('[algo]\n')
        f.write(f'nq = {self.nq}\n')
        f.write(f'qmax = {self.qmax}\n')
        f.write(f'qmin = {self.qmin}\n')
        f.write(f'npsi = {self.npsi}\n')
        f.write(f'nl = {self.nl}\n')
        f.write(f'lcrop = {self.lcrop}\n')
        f.write(f'rotk = {self.rotk}\n')
        f.write(f'rottheta = {self.rottheta}\n')
        f.write(f'dxsupp = {self.dxsupp}\n')
        f.write(f'pinv_rcond = {self.pinv_rcond}\n')
        f.write(f'eig_rcond = {self.eig_rcond}\n')
        f.write(f'lossy_iqlm = {self.lossy_iqlm}\n')
        f.write(f'lossy_sphv = {self.lossy_sphv}\n')
        f.close()


    def load_params(self):

        config = cfp.ConfigParser()
        config.read(self.algo_params_path())

        self._nq = int(config['algo']['nq'])

        qmax = config['algo']['qmax']
        if qmax == "None":
            self._qmax = None
        else:
            self._qmax = float(config['algo']['qmax'])

        qmin = config['algo']['qmin']
        if qmin == "None":
            self._qmin = None
        else:
            self._qmin = float(config['algo']['qmin'])
        self._npsi = int(config['algo']['npsi'])
        self._nl = int(config['algo']['nl'])
        self._lcrop = int(config['algo']['lcrop'])
        self._dxsupp = int(config['algo']['dxsupp'])

        self._rotk = eval(config['algo']['rotk'])
        self._rottheta = float(config['algo']['rottheta'])
        self._pinv_rcond = float(config['algo']['pinv_rcond'])
        self._eig_rcond = float(config['algo']['eig_rcond'])

        self._lossy_iqlm = config.getboolean('algo', 'lossy_iqlm')
        self._lossy_sphv = config.getboolean('algo', 'lossy_sphv')





