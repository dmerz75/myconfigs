#!/bin/bash

# (0) Variables
RUN_NUM=0

# cluster paths
# export PATH=$PATH:/root/cuda-5.0/gSOP_1.04/bin # biocat
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/cuda-5.0/lib64 # biocat
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/cuda-5.0/lib # fails
# export PATH=$PATH:/usr/local/cuda/6.0/opt/cuda # library


# (1) Preparation
mkdir -p dat dcd output structures topologies

# sbd_ : jobid
# dale : user
# /home/dale/sop_dev/projects_gsop/2khosbd : cwd
# sbd__2khosbd__118_5061798__10-30-2014_1512 : job_dir_name
# /home/dale/sop_dev/projects_gsop/2khosbd/sbd__2khosbd__118_5061798__10-30-2014_1512 : job_path_local
# /scratch/dale/sbd__2khosbd__118_5061798__10-30-2014_1512 : job_path_run
# /home/dale/completed/sbd__2khosbd__118_5061798__10-30-2014_1512 : completed_dir
# gsop : job_type

# (2) Topology
# (3) Equilibration stage
# (4) Pulling stage

# biocat
# /root/cuda-5.0/gSOP_1.04/bin/gsop_1.04 run_equil.sop >& LOG_equil$RUN_NUM.dat # biocat
# /root/cuda-5.0/gSOP_1.04/bin/gsop_1.04 run_pull.sop >& LOG_pull$RUN_NUM.dat # biocat

# library cluster
# $HOME/sop_dev/gsop/bin/gsop_1.04 equil.sop --make-top
# $HOME/sop_dev/gsop/bin/gsop_1.04 equil.sop >& LOG_equil$RUN_NUM.dat
# $HOME/sop_dev/gsop/bin/gsop_1.04 pull.sop >& LOG_pull$RUN_NUM.dat

# library cluster
# export LD_LIBRARY_PATH=/usr/local/cuda/6.0/opt/cuda/lib64:$LD_LIBRARY_PATH
# $HOME/sop_dev/gsop107/sop-top equil.sop --make-top
# $HOME/sop_dev/gsop107/sop-gpu equil.sop >& LOG_equil$RUN_NUM.dat
# $HOME/sop_dev/gsop107/sop-gpu pull.sop >& LOG_pull$RUN_NUM.dat

# m870
export LD_LIBRARY_PATH=/opt/cuda/lib64:$LD_LIBRARY_PATH
$HOME/sop_dev/gsop107/sop-top equil.sop --make-top
# $HOME/sop_dev/gsop107/sop-gpu equil.sop >& LOG_equil$RUN_NUM.dat
# $HOME/sop_dev/gsop107/sop-gpu pull.sop >& LOG_pull$RUN_NUM.dat

# gpu47 - works!
# /root/NVIDIA_GPU_Computing_SDK/C/bin/linux/release/gsop_1e_correct_fec run1_equil.sop  --make-top
# /root/NVIDIA_GPU_Computing_SDK/C/bin/linux/release/gsop_1e_correct_fec run_equil.sop >& LOG_equil$RUN_NUM.dat
# /root/NVIDIA_GPU_Computing_SDK/C/bin/linux/release/gsop_1e_correct_fec run_pull.sop >& LOG_pull$RUN_NUM.dat

# gpu105 - testing.. -failed so far
# /usr/local/cuda-5.0/samples/SOP-GPU_1.07/sop-top equil.sop  --make-top
# /usr/local/cuda-5.0/samples/SOP-GPU_1.07/sop-gpu equil.sop >& LOG_equil$RUN_NUM.dat
# /usr/local/cuda-5.0/samples/SOP-GPU_1.07/sop-gpu pull.sop >& LOG_pull$RUN_NUM.dat

# gpu105 - testing..
# /usr/local/cuda-5.0/samples/SOP-GPU_1.07/sop-top equil.sop  --make-top
# /usr/local/cuda-5.0/samples/SOP-GPU_1.07/sop-gpu-dale equil.sop >& LOG_equil$RUN_NUM.dat
# /usr/local/cuda-5.0/samples/SOP-GPU_1.07/sop-gpu-dale pull.sop >& LOG_pull$RUN_NUM.dat
