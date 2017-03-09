#!/bin/bash

#mkdir dat dcd output structures topologies

#/usr/local/cuda-5.0/samples/SOP-GPU_1.07/sop-top tub_H1_equil.sop --make-top

/usr/local/cuda-5.0/samples/SOP-GPU_1.07/sop-gpu-nj tub_H1_equil.sop >& LOG_equil.dat

/usr/local/cuda-5.0/samples/SOP-GPU_1.07/sop-gpu-nj tub_H1_pull.sop >& LOG_pull.dat
