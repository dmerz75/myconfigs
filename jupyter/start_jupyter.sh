#!/usr/bin/env bash

basic_example ()
{
    echo "Loading Jupyter settings!"
    kinit
    # Jupyter Command:
    # jupyter-notebook --help
    jupyter-notebook \
    --no-mathjax \
    --ip=bdbu-zli021.cloud-pg.com
    # --port=55752
}

bu_cluster ()
{
    echo "Loading Jupyter settings!"
    kinit
    # Jupyter Command:
    # jupyter-notebook --help
    jupyter-notebook \
    --no-mathjax \
    --ip=bdbu-zli021.cloud-pg.com
    # --port=55752
}