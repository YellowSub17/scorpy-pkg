



import sys
from pathlib import Path


if sys.platform =='linux':

    SCORPYDIR = Path('/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/')
    PADFDIR = Path('/home/pat/Documents/cloudstor/phd/python_projects/padf/')
    # DATADIR = SCORPYDIR / 'data'
    DATADIR = Path('/media/pat/datadrive/scorpy-data')


elif sys.platform =='win32':
    SCORPYDIR = Path('C:\\Users\\s3826109\\Documents\\scorpy-pkg')
    DATADIR = Path('C:\\Users\\s3826109\\Documents\\scorpy-data')
    PADFDIR = Path('NO\\WINDOWS\\PATH\\FOR\\PADF')




