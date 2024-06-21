# SCORPY


Scattering CORrelation in PYthon 

[Read the paper!](https://journals.iucr.org/m/issues/2024/04/00/it5033/index.html)

Citation:
    Adams, P., Greaves, T. L. & Martin, A. V. (2024). Crystal structure via fluctuation scattering. IUCrJ, 11.
    https://journals.iucr.org/m/issues/2024/04/00/it5033/index.html



## Conda Setup (Requirements)

Use the following commands to set up a conda environment.

    conda deactivate
    conda create -n phd python==3.9 --yes
    conda activate phd
    #conda install -c conda-forge ipython --yes
    conda install -c conda-forge numpy==1.26.4 --yes
    conda install -c conda-forge matplotlib==3.8.4 --yes
    conda install -c conda-forge pyshtools=4.12.2 --yes
    conda install -c conda-forge h5py==3.11 --yes
    conda install -c conda-forge pycifrw==4.4.6 --yes
    conda install -c conda-forge scipy==1.13.1 --yes
    conda install -c conda-forge scikit-image==0.24.0 --yes
    conda install -c conda-forge regex==2024.5.15 --yes
    conda install -c conda-forge numba==0.60.0 --yes

## Installation 

To install scorpy, run the following commands to download the package, move into the directory and install an editable verision of the package.
This will create a link from your python site-package directory to an egg-info directory.

    git clone https://github.com/YellowSub17/scorpy-pkg.git
    cd scorpy-pkg
    pip install -e .





