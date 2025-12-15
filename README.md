# SCORPY


Scattering CORrelation in PYthon 

[Read the paper!](https://journals.iucr.org/m/issues/2024/04/00/it5033/index.html)

Citation:
    Adams, P., Greaves, T. L. & Martin, A. V. (2024). Crystal structure via fluctuation scattering. IUCrJ, 11.
    https://journals.iucr.org/m/issues/2024/04/00/it5033/index.html



## Conda Setup (Requirements)

Use the following commands to set up a conda environment.


    conda deactivate
    conda create -n scorpy python=3.13 --yes
    conda activate scorpy --yes
    conda install numpy --yes
    conda install matplotlib --yes
    conda install h5py --yes
    conda install scikit-image --yes
    conda install regex --yes
    conda install numba --yes
    conda install conda-forge::pyshtools --yes
    conda install conda-forge::pycifrw --yes



## Installation 

To install scorpy, run the following commands to download the package, move into the directory and install an editable verision of the package.
This will create a link from your python site-package directory to an egg-info directory.

    git clone https://github.com/YellowSub17/scorpy-pkg.git
    cd scorpy-pkg
    pip install -e .

## Example scripts

See this other repo for a collection of scripts demonstrating scorpy

    https://github.com/YellowSub17/scorpy-tute




