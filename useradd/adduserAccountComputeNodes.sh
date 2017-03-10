#!/bin/bash

# backup first!
cp /etc/passwd /etc/passwd.bac
cp /etc/shadow /etc/shadow.bac
cp /etc/group /etc/group.bac

function library () {

    for i in {1..12}; do
        echo copying passwd,shadow,group to node$i
        scp /etc/passwd node$i:/etc/passwd
        scp /etc/shadow node$i:/etc/shadow
        scp /etc/group  node$i:/etc/group
    done

    for i in {1..3}; do
        echo copying passwd,shadow,group to gpu$i
        scp /etc/passwd gpu$i:/etc/passwd
        scp /etc/shadow gpu$i:/etc/shadow
        scp /etc/group  gpu$i:/etc/group
    done

    cat /etc/passwd | tail -1
}

function biocat () {

    for i in {1..6}; do
        echo copying passwd,shadow,group to qc$i
        scp /etc/passwd qc$i:/etc/passwd
        scp /etc/shadow qc$i:/etc/shadow
        scp /etc/group  qc$i:/etc/group
    done

    for i in {1..12}; do
        echo copying passwd,shadow,group to dq$i
        scp /etc/passwd dq$i:/etc/passwd
        scp /etc/shadow dq$i:/etc/shadow
        scp /etc/group  dq$i:/etc/group
    done

    for i in {1..18}; do
        echo copying passwd,shadow,group to o$i
        scp /etc/passwd o$i:/etc/passwd
        scp /etc/shadow o$i:/etc/shadow
        scp /etc/group  o$i:/etc/group
    done

    for i in {1..4}; do
        echo copying passwd,shadow,group to gpu$i
        scp /etc/passwd gpu$i:/etc/passwd
        scp /etc/shadow gpu$i:/etc/shadow
        scp /etc/group  gpu$i:/etc/group
    done

    cat /etc/passwd | tail -1
}
