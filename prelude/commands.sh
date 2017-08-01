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

alsoworks () {

    cd personal

    ln -s ../personal_unstable/auto* . 

    ln -s ../personal_unstable/auto* .    # packages installed.
    ln -s ../personal_unstable/better-* . # ido-mode.
    ln -s ../personal_unstable/bash* . 
    ln -s ../personal_unstable/config_* . # coloration ..

    ln -s ../personal_unstable/default_* . 

    ln -s ../personal_unstable/dired* . 
    ln -s ../personal_unstable/fly* . 
    ln -s ../personal_unstable/replace* . 
    ln -s ../personal_unstable/openwith* .
    ln -s ../personal_unstable/prelude* .
    ln -s ../personal_unstable/make* .
    ln -s ../personal_unstable/ibuffer* .
}



testing () {

    echo


}

rm personal/*
# works
alsoworks
ls *
# testing
