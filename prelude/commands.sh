#!/bin/bash


works () {
    cp personal_unstable/auto* personal/    # packages installed.
    cp personal_unstable/better-* personal/ # ido-mode.
    cp personal_unstable/bash* personal/
    cp personal_unstable/config_* personal/ # coloration ..

    cp personal_unstable/default_* personal/

    cp personal_unstable/dired* personal/
    cp personal_unstable/fly* personal/
    cp personal_unstable/replace* personal/
    cp personal_unstable/openwith* personal/
    cp personal_unstable/prelude* personal/
    cp personal_unstable/make* personal/
    cp personal_unstable/ibuffer* personal/

}



testing () {

    echo


}

rm personal/*
works
ls *
# testing
