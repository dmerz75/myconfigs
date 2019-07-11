#!/bin/bash
echo running script:   $0
echo num_arguments: $#

if [ "$#" -lt 3 ]; then
    echo "COMMAND:  az vm  <function> {create, start, stop, deallocate}   <resource-group>  <name>"
    echo "USE:  ./vm_commands.sh   vm_{create, start, stop, deallocate}   <resource-group>  <name>"
else
    VMCOMMAND=$1
    RG=$2
    VM=$3
    DISTRO=$4
    echo resource-group: $RG   vm-name:  $VM   distro: $DISTRO
fi

vm_create () {
    az vm create --resource-group $RG --name $VM --image $DISTRO --admin-username azureuser --generate-ssh-keys
}
vm_start () {
    ## Start the VM
    az vm start --name $VM --resource-group $RG
}
vm_stop () {
    ## Stop the VM
    az vm stop --name $VM --resource-group $RG
}
vm_deallocate () {
    ## Stop the VM
    az vm deallocate --name $VM --resource-group $RG
}

$VMCOMMAND