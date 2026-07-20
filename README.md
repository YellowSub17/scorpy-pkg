# SCORPY v2


Scattering CORrelation in PYthon

[Read the paper!](https://journals.iucr.org/m/issues/2024/04/00/it5033/index.html)

Citation:
    Adams, P., Greaves, T. L. & Martin, A. V. (2024). Crystal structure via fluctuation scattering. IUCrJ, 11.
    https://journals.iucr.org/m/issues/2024/04/00/it5033/index.html


## package requirements

    python 3.13.11
    numpy 2.3.5
    matplotlib 3.10.8
    h5py 3.15.1
    pyshtools 4.13.1
    pycifrw 5.0.1


## Conda Setup (Requirements)

Use the following commands to set up a conda environment.

    conda create -n scorpy python=3.13 numpy=2.3.5 matplotlib=3.10.8 h5py=3.15.1 conda-forge::pyshtools=4.13.1 conda-forge::pycifrw=5.0.1 --yes
    conda activate scorpy


## Installation 

To install scorpy, run the following commands to download the package, move into the directory and install an editable verision of the package.
This will create a link from your python site-package directory to an egg-info directory.

    git clone https://github.com/YellowSub17/scorpy-pkg.git
    cd scorpy-pkg
    pip install -e .   # For standard runtime usage:
    pip install -e .[docs] # OR for development and documentation tools (installs Sphinx + Theme):





## Editors Notes

Currently experimenting with potentially breaking changes to this code base. General clean up, docs and tests. If you want a working version, try a commit from circa 2019-2020.









