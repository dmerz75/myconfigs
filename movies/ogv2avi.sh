#!/bin/bash
# ogv to avi
# Call this with multiple arguments
# for example : ls *.{ogv,OGV} | xargs ogv2avi

# [dale~]$ls out-1.ogv | xargs ~/.pylib/movies/ogv2avi.sh out-1.ogv
# ffmpeg -i out-1.ogv -vcodec mpeg4 -acodec libmp3lame global_align.avi

N=$#;
echo “Converting $N files !”
for ((i=0; i<=(N-1); i++))
do
    echo “converting” $1
    filename=${1%.*}
    ffmpeg -i $1 -vcodec mpeg4 -acodec libmp3lame $filename.avi
    shift 1
done
