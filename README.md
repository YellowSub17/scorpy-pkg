# SCORPY



Scattering CORrelation in PYthon 


## Conda Setup

Use the following commands to set up a conda environment.

    conda deactivate
    conda create -n phd python==3.9 --yes
    conda activate phd
    conda install -c conda-forge ipython --yes
    conda install -c conda-forge numpy --yes
    conda install -c conda-forge matplotlib --yes
    conda install -c conda-forge pyshtools --yes
    conda install -c conda-forge h5py --yes
    conda install -c conda-forge pycifrw --yes
    conda install -c conda-forge scipy --yes
    conda install -c conda-forge scikit-image

To setup auto reload in ipython.

    ipython profile create
    echo 'c.InteractiveShellApp.extensions = ["autoreload"]' >> ~/.ipython/profile_default/ipython_config.py
    echo 'c.InteractiveShellApp.exec_lines = ["%autoreload 2"]' >> ~/.ipython/profile_default/ipython_config.py

    
## Installation 

To install scorpy, run the following commands to download the package, move into the directory and install an editable verision of the package.
This will create a link from your python site-package directory to an egg-info directory.

    git clone https://github.com/YellowSub17/scorpy-pkg.git
    cd scorpy-pkg
    pip install -e .


