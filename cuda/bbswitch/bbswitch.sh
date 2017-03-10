#!/bin/bash

# CUDA without Bumblebee
# You can use CUDA without bumblebee. All you need to do is ensure that the nvidia card is on:
function bbswitch_on {
    sudo tee /proc/acpi/bbswitch <<< ON
}
# Now when you start a CUDA application it is going to automatically load all the necessary modules.
# To turn off the nvidia card after using CUDA do:
function bbswitch_off_modules {
    rmmod nvidia_uvm
    rmmod nvidia
    sudo tee /proc/acpi/bbswitch <<< OFF
}
function bbswitch_off {
    # rmmod nvidia_uvm
    # rmmod nvidia
    sudo tee /proc/acpi/bbswitch <<< OFF
}
function bbswitch_off_bumblebee {
    sudo rmmod nvidia_uvm && sudo systemctl restart bumblebeed.service
}
function bbswitch_status {
    cat /proc/acpi/bbswitch
}
function bbswitch_dmesg {
    dmesg | tail -10
}
# nota bene:
# [dale~/opt/bbswitch]$dmesg | tail -10
# [  327.118282] ACPI Warning: \_SB_.PCI0.PEG0.PEGP._DSM: Argument #4 type mismatch - Found [Buffer], ACPI requires [Package] (20131218/nsarguments-95)
# [  327.237958] ACPI Warning: \_SB_.PCI0.PEG0.PEGP._DSM: Argument #4 type mismatch - Found [Buffer], ACPI requires [Package] (20131218/nsarguments-95)
# [  336.070481] bbswitch: device 0000:01:00.0 is in use by driver 'nvidia', refusing OFF
# [  376.791301] bbswitch: device 0000:01:00.0 is in use by driver 'nvidia', refusing OFF
