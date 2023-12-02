
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

from ..vols.sphv.sphericalvol import SphericalVol
from ..iqlm.iqlmhandler import IqlmHandler



from ..utils.env import DATADIR
import os
import shutil
from pathlib import Path


class AlgoHandler(AlgoHandlerOperators, AlgoHandlerSchemes,AlgoHandlerPaths, AlgoHandlerRunRecon, AlgoHandlerSetupRecon, AlgoHandlerPostRecon, AlgoHandlerPlot):


    def __init__(self, tag, path=None, nq=256, qmax=None, npsi=360*32, nl=180, lcrop=45,
                 dxsupp=2, pinv_rcond=0.1, eig_rcond=1e-15, lossy_iqlm=True, lossy_sphv=True,
                 rotk=[1,1,1], rottheta=np.radians(30), overwrite=0):


        self.tag = tag

        if path is None:
            path = DATADIR / 'algo'

        self.path = Path(f'{path}/{tag}')

        self.nq = nq
        self.qmax = qmax
        self.npsi = npsi
        self.nl = nl
        self.lcrop = lcrop
        self.dxsupp = dxsupp
        self.pinv_rcond = pinv_rcond
        self.eig_rcond = eig_rcond
        self.lossy_iqlm = lossy_iqlm
        self.lossy_sphv = lossy_sphv
        self.rotk = rotk
        self.rottheta = rottheta



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
        f = open(f'{self.path}/algo_{self.tag}_params.txt', 'w')
        f.write('##Scorpy Algo Config File\n')
        f.write(f'## Created: {datetime.now().strftime("%Y/%m/%d %H:%M")}\n\n')
        f.write('[algo]\n')
        f.write(f'nq = {self.nq}\n')
        f.write(f'qmax = {self.qmax}\n')
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
        config.read(f'{self.path}/algo_{self.tag}_params.txt')

        self.nq = int(config['algo']['nq'])

        qmax = config['algo']['qmax']
        if qmax == "None":
            self.qmax = None
        else:
            self.qmax = float(config['algo']['qmax'])
        self.npsi = int(config['algo']['npsi'])
        self.nl = int(config['algo']['nl'])
        self.lcrop = int(config['algo']['lcrop'])
        self.dxsupp = int(config['algo']['dxsupp'])

        self.rotk = eval(config['algo']['rotk'])
        self.rottheta = float(config['algo']['rottheta'])
        self.pinv_rcond = float(config['algo']['pinv_rcond'])
        self.eig_rcond = float(config['algo']['eig_rcond'])

        self.lossy_iqlm = config.getboolean('algo', 'lossy_iqlm')
        self.lossy_sphv = config.getboolean('algo', 'lossy_sphv')





