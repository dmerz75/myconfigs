#!/bin/bash

# CUDA_INSTALL_PATH   := /opt/cuda-6.5 # biocat gpu4
# export PATH=/opt/cuda-6.5/bin:$PATH
# export LD_LIBRARY_PATH=/opt/cuda-6.5/lib:/opt/cuda-6.5/lib64:$LD_LIBRARY_PATH


# to TURN on the GPU m870, technically -- permits device-query's to work
printf '\nCOMMAND: nvidia-smi\n\n'
nvidia-smi


# http://stackoverflow.com/questions/9727688/how-to-get-the-cuda-version

# As Jared mentions in a comment, from the command line:
# -- gives the CUDA compiler version (which matches the toolkit version).
printf '\nCOMMAND: nvcc --version\n\n'
nvcc --version


# --  From application code, you can query the runtime API version with --
# -- or the driver API version with
# cudaRuntimeGetVersion()
# cudaDriverGetVersion()


# As Daniel points out, deviceQuery is an SDK sample app that queries the above, along with device capabilities.
# If you have installed CUDA SDK, you can run "deviceQuery" to see the version of CUDA
# share|edit
# printf 'COMMAND: deviceQuery'  # !! does not work yet ...
# deviceQuery


# Apart from the ones mentioned above, your CUDA installations path (if not changed during setup) typically contains the version number
# doing a which nvcc should give the path and that will give you the version
printf '\nCOMMAND: which nvcc\n\n'
which nvcc


# After installing CUDA one can check the versions by: nvcc -V
# I have installed both 5.0 and 5.5 so it gives
# Cuda Compilation Tools,release 5.5,V5.5,0
printf '\nCOMMAND: nvcc -V\n\n'
nvcc -V


# run_device_query
printf '\nmake query\n'
printf '\nCOMMAND: ./device_query.exe\n'
./devicequery.exe
