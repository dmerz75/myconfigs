#!/bin/bash

# (0) Variables
RUN_NUM=0

# (1) Preparation
mkdir -p dat dcd output structures topologies

# xx_jobname_xx : jobid
# xxuserxx : user
# xxmy_dirxx : cwd
# xxjob_dir_namexx : job_dir_name
# xxjob_path_localxx : job_path_local
# xxjob_path_runxx : job_path_run
# xxcompleted_dirxx : completed_dir
# xxsubnamexx : job_type

# (2) Topology
# (3) Equilibration stage
# (4) Pulling stage

# ------------SAMPLE-------------------
# bashrc
# export PATH=/usr/local/cuda-6.0/bin:$PATH
# export LD_LIBRARY_PATH=/usr/local/cuda-6.0/lib64:/usr/local/cuda-6.0/lib:$LD_LIBRARY_PATH
# $HOME/sop_dev/gsop107/sop-gpu-65 equil.sop --make-top
# $HOME/sop_dev/gsop107/sop-gpu-65 equil.sop > LOG_equil_$RUN_NUM.dat
# $HOME/sop_dev/gsop107/sop-gpu-65 pull.sop > LOG_pull_$RUN_NUM.dat


# ------------WORKS--------------------
# bashrc
export PATH=/opt/cuda-6.5/bin:$PATH
export LD_LIBRARY_PATH=/opt/cuda-6.5/lib64:/opt/cuda-6.5/lib:$LD_LIBRARY_PATH
# $HOME/sop_dev/gsop107/sop-gpu-65 equil.sop --make-top
$HOME/sop_dev/gsop107/sop-gpu-65 equil.sop > LOG_equil_$RUN_NUM.dat
# $HOME/sop_dev/gsop107/sop-gpu-65 pull.sop > LOG_pull_$RUN_NUM.dat

# m870
# export LD_LIBRARY_PATH=/opt/cuda/lib64:$LD_LIBRARY_PATH
# $HOME/sop_dev/gsop107/sop-top equil.sop --make-top
# $HOME/sop_dev/gsop107/sop-gpu-65 equil.sop >& LOG_equil_$RUN_NUM.dat
# $HOME/sop_dev/gsop107/sop-gpu-65 pull.sop >& LOG_pull_$RUN_NUM.dat



# ------------OTHER--------------------
# library cluster
# export LD_LIBRARY_PATH=/usr/local/cuda-5.0/lib64:$LD_LIBRARY_PATH    # MUST USE!
# $HOME/sop_dev/gsop107/sop-gpu-d5 equil.sop --make-top
# $HOME/sop_dev/gsop107/sop-gpu-d5 equil.sop >& LOG_equil$RUN_NUM.dat
# $HOME/sop_dev/gsop107/sop-gpu-d5 pull.sop >& LOG_pull$RUN_NUM.dat

# gpu47
# /root/NVIDIA_GPU_Computing_SDK/C/bin/linux/release/gsop_1e_correct_fec run1_equil.sop  --make-top
# /root/NVIDIA_GPU_Computing_SDK/C/bin/linux/release/gsop_1e_correct_fec run_equil.sop >& LOG_equil$RUN_NUM.dat
# /root/NVIDIA_GPU_Computing_SDK/C/bin/linux/release/gsop_1e_correct_fec run_pull.sop >& LOG_pull$RUN_NUM.dat

# gpu105 - previously works
# /usr/local/cuda-5.0/samples/SOP-GPU_1.07/sop-top run1_equil.sop  --make-top
# /usr/local/cuda-5.0/samples/SOP-GPU_1.07/sop-gpu run_equil.sop >& LOG_equil$RUN_NUM.dat
# /usr/local/cuda-5.0/samples/SOP-GPU_1.07/sop-gpu run_pull.sop >& LOG_pull$RUN_NUM.dat

# gpu105 - testing
# export LD_LIBRARY_PATH=/usr/local/cuda-5.0/lib64:$LD_LIBRARY_PATH    # MUST USE!
# $HOME/sop_dev/gsop107/sop-gpu-d5 equil.sop --make-top
# $HOME/sop_dev/gsop107/sop-gpu-d5 equil.sop >& LOG_equil$RUN_NUM.dat
# $HOME/sop_dev/gsop107/sop-gpu-d5 pull.sop >& LOG_pull$RUN_NUM.dat

# ------------Testing------------------
# export PATH=$PATH:/opt/cuda/bin
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/cuda/lib:/opt/cuda/lib64
# echo 'export PATH=$PATH:/opt/cuda/bin' >> ~/.bash_profile
# echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/cuda/lib:/opt/cuda/lib64' >> ~/.bash_profile
# .bashrc
# export PATH=/opt/cuda/bin:$PATH
# export LD_LIBRARY_PATH=/opt/cuda/lib:/opt/cuda/lib64:$LD_LIBRARY_PATH
# uninstall
# rm -r ~/NVIDIA_GPU_Computing_SDK
# sudo rm -r /opt/cuda

# ------------FAILS--------------------
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
# library cluster
# export LD_LIBRARY_PATH=/usr/local/cuda/6.0/opt/cuda/lib64:$LD_LIBRARY_PATH
# /usr/local/cuda-5.0/SOP-GPU_1.07/sop-top equil.sop --make-top
# /usr/local/cuda-5.0/SOP-GPU_1.07/sop-gpu equil.sop >& LOG_equil$RUN_NUM.dat
# /usr/local/cuda-5.0/SOP-GPU_1.07/sop-gpu pull.sop >& LOG_pull$RUN_NUM.dat

# ------------GSOP2.0--------------------
# m870
# GSOP2DIR=~/SOP-GPU-master/src
# TOP2=$GSOP2DIR/sop-top
# TOP22=$GSOP2DIR/sop-top2
# GSOP2=$GSOP2DIR/sop-gpu
# export PATH=/opt/cuda/bin:$PATH
# export LD_LIBRARY_PATH=/opt/cuda/lib64:/opt/cuda/lib:$LD_LIBRARY_PATH
# export PATH=/opt/cuda-6.5/bin:$PATH
# export LD_LIBRARY_PATH=/opt/cuda-6.5/lib64:/opt/cuda-6.5/lib:$LD_LIBRARY_PATH
# $GSOP2DIR/sop-gpu equil.sop > LOG_equil_$RUN_NUM.dat
# $GSOP2DIR/sop-gpu pull.sop > LOG_pull_$RUN_NUM.dat

# cluster paths
# export PATH=$PATH:/root/cuda-5.0/gSOP_1.04/bin # biocat
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/cuda-5.0/lib64 # biocat
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/cuda-5.0/lib # fails
# export PATH=$PATH:/usr/local/cuda/6.0/opt/cuda # library
