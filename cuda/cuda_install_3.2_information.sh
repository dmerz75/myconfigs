#!/bin/bash

# ========================================

# * Please make sure your PATH includes /opt/cuda-3.2/cuda/bin
# * Please make sure your LD_LIBRARY_PATH
# *   for 32-bit Linux distributions includes /opt/cuda-3.2/cuda/lib
# *   for 64-bit Linux distributions includes /opt/cuda-3.2/cuda/lib64:/opt/cuda-3.2/cuda/lib
# * OR
# *   for 32-bit Linux distributions add /opt/cuda-3.2/cuda/lib
# *   for 64-bit Linux distributions add /opt/cuda-3.2/cuda/lib64 and /opt/cuda-3.2/cuda/lib
# * to /etc/ld.so.conf and run ldconfig as root

# * Please read the release notes in /opt/cuda-3.2/cuda/doc/

# * To uninstall CUDA, delete /opt/cuda-3.2/cuda
# * Installation Complete

# root@gpu0:/home/dmerz3/Dropbox/uptake#


# SETUP
export PATH=/opt/cuda-3.2/cuda/bin:$PATH
export LD_LIBRARY_PATH=/opt/cuda-3.2/cuda/lib64:$LD_LIBRARY_PATH
