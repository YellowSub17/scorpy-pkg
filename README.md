# SCORPY



Scattering CORrelation in PYthon (WIP).


## Conda Setup

Use the following commands to set up a conda environment.

    conda deactivate
    conda create -n phd python==3.9 --yes
    conda activate phd
    conda install -c anaconda ipython --yes
    conda install -c conda-forge numpy --yes
    conda install -c conda-forge matplotlib --yes
    conda install -c conda-forge pyshtools --yes
    conda install -c conda-forge healpy --yes
    conda install -c conda-forge h5py --yes
    conda install -c conda-forge pycifrw --yes
    conda install -c conda-forge scipy --yes


    
## Installation 

1. Download the source
2. cd into the directory scorpy-pkg
3. Run the command `pip install -e .`


This will create a link from your python site-package directory to an egg-info directory.

## Testing

Test scripts can be found in `tests`. Use the command `py.test -v tests/` to run all tests.

