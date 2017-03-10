#!/bin/bash

build_project_scope () {
    cd /
    # $1: is the full path to project directory.
    find $1 -name '*.cpp' >/my/cscope/dir/cscope.files
    find $1 -name '*.h' >/my/cscope/dir/cscope.files
}
