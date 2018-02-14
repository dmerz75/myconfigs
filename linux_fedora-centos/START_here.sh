#/bin/bash

DNF="dnf install"

repos () {
    rpm -ivh https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm 
    # rpm -ivh https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-26.noarch.rpm
    rpm -ivh https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

    # rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
    # rpm -Uvh http://dl.atrpms.net/all/atrpms-repo-7-7.el7.x86_64.rpm
    dnf repolist
}
defaults () {
    dnf update
    dnf repolist
    $DNF epel-release
    $DNF NetworkManager-tui # nmtui
    $DNF intltool
}
packages_cuda_before () {
    $DNF dkms
    $DNF kernel-headers-$(uname -r)
    $DNF kernel-devel-$(uname -r)
    $DNF gcc g++ cpp
    $DNF wget make gcc-c++ freeglut-devel libXi-devel libXmu-devel mesa-libGLU-devel
    $DNF xorg-x11-drv-nvidia-libs xorg-x11-drv-nvidia-libs.i686
}

packages_cuda_before_2 () {
    $DNF xorg-x11-drv-nvidia
    $DNF akmod-nvidia
    $DNF xorg-x11-drv-nvidia-cuda
}

# dnf groupinstall "Development Tools"
# install nvidia-driver
# systemctl stop gdm
# alt-F2
# blacklist nouveau (/etc/modprobe.d/nvidia-installer-disable-nouveau.conf)
#   # generated by nvidia-installer
#   blacklist nouveau
#   options nouveau modeset=0

packages_cuda_after () {
    # download nvidia-driver
    # cuda.run separately.
    mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.bak
    dracut -v /boot/initramfs-$(uname -r).img $(uname -r)
}



fedora_2_bumblebee () {
  dnf -y --nogpgcheck install http://install.linux.ncsu.edu/pub/yum/itecs/public/bumblebee/fedora$(rpm -E %fedora)/noarch/bumblebee-release-1.2-1.noarch.rpm
  dnf -y --nogpgcheck install http://install.linux.ncsu.edu/pub/yum/itecs/public/bumblebee-nonfree/fedora$(rpm -E %fedora)/noarch/bumblebee-nonfree-release-1.2-1.noarch.rpm
  $DNF bumblebee-nvidia bbswitch-dkms VirtualGL.x86_64 VirtualGL.i686 primus.x86_64 primus.i686 kernel-devel 
}

packages_general () {
    $DNF vim emacs terminator vlc gimp
    $DNF geeqie python2-numpy python3-numpy pidgin
    $DNF unzip icedtea-web java-openjdk
    $DNF qbittorrent youtube-dl simple-scan
}



# repos
# defaults
# packages_cuda_before
# packages_cuda_before_2
# packages_cuda_after

fedora_2_bumblebee # for laptops.
# packages_general



# now, install Nvidia driver, then reboot
# ./NVIDIA-Linux-x86_64-384.90.run 
# ./cuda_9.0.176_384.81_linux.run 
# systemctl get-default
# systemctl set-default multi-user.target
# ping -c 3 8.8.8.8
# nmtui
# /etc/modprobe.d/nvidia-installer-disable-nouveau.conf
# sudo update-initramfs -u
# 77  dnf search initramfs
# 78  dnf install dracut
# 79  dracut -v
