#!/bin/bash


function nouveau_removal {


    # mkinitcpio -p linux
}


function manjaro_gpu {
    inxi -G
}
function manjaro_gpu_changes {
    # remove
    # sudo mhwd -r pci video-hybrid-intel-nvidia-bumblebee
    # sudo mhwd -r pci video-hybrid-intel-nvidia-bumblebee
    # Error: config 'video-hybrid-intel-nvidia-bumblebee' conflicts with config(s): video-hybrid-intel-nouveau-bumblebee
    sudo mhwd -r pci video-hybrid-intel-nouveau-bumblebee


    # If you have the Nouveau driver you can install the proprietary NVIDIA driver by
    # using the Manjaro Hardware Detection (MHWD) utility.
    # To do so, enter the following command into your terminal:
    sudo mhwd -a pci nonfree 0300

    # Once Complete, reboot your system to complete the process.
    # You can then confirm that the driver has been installed and is working by
    # entering the following command into your terminal:
    mhwd -li
}




function check_gpu_card {
    # check nouveau graphics:
    printf 'skipping ...'
    printf '\nCOMMAND: pacman -Ss nouveau\n\n'
    # pacman -Ss nouveau

    # check nvidia graphics:
    printf 'skipping ...'
    printf '\nCOMMAND: pacman -Ss nvidia\n\n'
    # pacman -Ss nvidia


    # http://superuser.com/questions/617350/cuda-5-5-on-ubuntu-12-04-not-running-on-nvidia-gf-630m
    # I have the same problem with you. This is what I've done to make it work properly:
    # Create new module blacklist
    # touch /etc/modprobe.d/nvidia-installer-disable-nouveau.conf
    # Now blacklist nouveau
    # echo -e "blacklist nouveau\noptions nouveau modeset=0" > /etc/modprobe.d/nvidia-installer-disable-nouveau.conf
    # Restart your PC / Laptop

    # check graphics card:
    printf '\nCOMMAND: lspci ...'
    lspci -k | grep -A 2 -i "VGA"

    # check cards
    xrandr --listproviders

    # Providers: number : 2
    # Provider 0: id: 0x7d cap: 0xb, Source Output, Sink Output, Sink Offload crtcs: 3 outputs: 4 associated providers: 1 name:Intel
    # Provider 1: id: 0x56 cap: 0xf, Source Output, Sink Output, Source Offload, Sink Offload crtcs: 6 outputs: 1 associated providers: 1 name:radeon

    # We can see that there are two graphic cards: Intel, the integrated card (id 0x7d), and Radeon, the discrete card (id 0x56), which should be used for GPU-intensive applications. We can see that, by default, Intel is always used:
    # glxinfo | grep "OpenGL renderer"


    # OpenGL renderer string: Mesa DRI Intel(R) Ivybridge Mobile
    # The command xrandr --setprovideroffloadsink provider sink can be used to make a render offload provider send its output to the sink provider (the provider which has a display connected). The provider and sink identifiers can be numeric (0x7d, 0x56) or a case-sensitive name (Intel, radeon). Example:
    xrandr --setprovideroffloadsink radeon Intel

    # Now, you can use your discrete card for the applications who need it the most (for example games, 3D modellers...):
    # $ DRI_PRIME=1 glxinfo | grep "OpenGL renderer"
    # OpenGL renderer string: Gallium 0.4 on AMD TURKS
}
