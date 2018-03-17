#!/bin/bash


remove_audio ()
{
    # call function with 1 mp4 file.

    # to copy video stream and 2nd audio stream to new_file.mp4
    ffmpeg -i $1 -map 0:0 -map 0:0 -acodec copy -vcodec copy $2

}

remove_audio $1 $2
