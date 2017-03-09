
function install_pycscope {
    # apt-get install cscope
    # pacman -S cscope pycscope
    # pip install pycscope
}

function scope_py {
    # in project base dir:
    find . -name '*.py' > cscope.files
    cscope -R

}
