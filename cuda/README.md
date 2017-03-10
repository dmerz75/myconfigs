
README.md

# graphics:
## general:
### check_graphics_settings.sh
## modprobe.d:
### etc_modprobe.d_nouveau_blacklist.conf
Use etc_modprobe.d_nouvea_blacklist.conf to switch to nvidia by blacklisting nouveau
### etc_modprobe.d_modprobe.conf
### etc_modprobe.d_blacklist.conf
### etc_modprobe.d_mhwd-bbswitch.conf
## X11:
### etc_X11_xorg.conf_1
### etc_X11_xorg.conf.d_10-nvidia.conf
### etc_X11_xorg.conf.d_20-nvidia.conf
### etc_X11_mhwd.d_intel.conf
## /usr:
### usr_lib_modprobe.d_nvidia.conf-nvidia-installer-disable-nouveau.conf


## changes for graphics:
1. remove 20-nvidia - did it.
2. remove mhwd.d_intel - bad idea!
3. edited modprobe.d/mhwd-bbswitch.conf, 1,1
4. now using bbswitch. seems to be working!

## current:
1. set mhwd-bbswitch.conf, 0,0

## long term development: (testing)
1. turn back to 0 (turn off) discrete graphics
2. turn on computer, turn on card, load nvidia
3. unload nvidia, turn off card
4. turn on card, reload nvidia
3. (repeat)
4. (repeat)


# maintenance:
## cuda_run_version.sh
Get output for the following commands:
COMMAND: nvidia-smi
COMMAND: nvcc --version
COMMAND: which nvcc
COMMAND: nvcc -V
<!-- builds run_device_query.exe by: nvcc cuda_device_query.cu -o run_device_query.exe -->
make query
COMMAND: ./run_device_query.exe
## Makefile
## cuda_device_query.cu
## run_device_query.exe*


# maintenance-cornell:
An alternate device query option.
## devicequery
## devicequery.cu
## Makefile


# onswitch:
Consider running:
    lsmod
    source cuda_without_bumblebee.sh
## cuda_without_bumblebee.sh
