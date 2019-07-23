#!/usr/bin/env bash

anaconda () {
conda install -c conda-forge jupyter_contrib_nbextensions
conda install -c conda-forge jupyter_nbextensions_configurator
jupyter contrib nbextension install --user
}

pip () {
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
}