#!/bin/bash
echo running script:   $0
echo num_arguments: $#

if [ "$#" -ne 3 ]; then
    echo "az vm  <function> {create, start, stop, deallocate}   <resource-group>  <name>"
    echo "source vm_commands.sh && vm_ {create, start, stop, deallocate}   <resource-group> $1  <name> $2"
else
    VMCOMMAND=$1
    RG=$2
    VMNAME=$3
    echo resource-group: $RG   vm-name:  $VMNAME
fi

vm_create () {
    az vm create --resource-group myResourceGroup --name myVM --image UbuntuLTS --admin-username azureuser --generate-ssh-keys
}
vm_start () {
    ## Start the VM
    az vm start --name myVM --resource-group myResourceGroup
}
vm_stop () {
    ## Stop the VM
    az vm stop --name myVM --resource-group myResourceGroup
}
vm_deallocate () {
    ## Stop the VM
    az vm deallocate --name myVM --resource-group myResourceGroup
}

$VMCOMMAND