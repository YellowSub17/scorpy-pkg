# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

project = 'scorpy'
copyright = '2026, Patrick Adams'
author = 'Patrick Adams'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.napoleon',
        'sphinx.ext.viewcode',
        'sphinx_rtd_theme',
        ]

templates_path = ['_templates']
exclude_patterns = []

# import importlib.metadata
# # Get a list of ALL installed packages in your active environment
# all_packages = [dist.metadata['Name'] for dist in importlib.metadata.distributions()]
# # Filter out 'scorpy' and 'sphinx' so they don't accidentally get mocked
# autodoc_mock_imports = [
    # pkg for pkg in all_packages
    # if pkg.lower() not in [ 'sphinx', 'sphinx_rtd_theme']
# ]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
