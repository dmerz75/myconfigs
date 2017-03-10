#!/bin/bash
# Passing arguments to a function
# delay: if 100 frames, use ~ 25

process () {
    mencoder mf:// on:w=800:h=600:fps=4 -ovc lavc -o output.avi \*.png
    mencoder -speed 1/10 output.avi -ovc copy -nosound -o slower.flv

    convert -delay 10 -loop 0 inputfiles*.png animation.gif
    # viewers
    # gifview - have to click
    gwenview - works

    # terminal modifier
    gifsicle --delay=10 --loop *.gif > anim.gif

    # Extracting frames from animations is easy too:
    gifsicle anim.gif '#0' > firstframe.gif

    # You can also edit animations by replacing, deleting, or inserting frames:
    gifsicle -b anim.gif --replace '#0' new.gif
}

make_animated_gif_by_type () {
    # start
    echo $1
    gifsicle --delay=10 --loop *.$1 > anim.gif
}

make_animated_gif_tga () {
    # start
    echo $1
    convert -delay 20 -loop 0 $1*.tga animation_$1.gif
    # gifsicle --delay=10 --loop *.$1 > anim.gif
}
# make_animated_gif_tga $1 # sometimes works.

make_animation () {
    # start
    echo $1
    echo $2
    convert -delay 20 -loop 0 $1*.$2 animation_$1.gif
    # gifsicle --delay=10 --loop *.$1 > anim.gif
}
# make_animated_gif_tga $1 # sometimes works.

make_animated_gif_dir () {
    # start
    echo $1
    echo $2
    echo $3
    convert -delay 20 -loop 0 $1/$2*.$3 animation_$2_$1.gif
    echo "animation_$2_$1.gif written."
    # gifsicle --delay=10 --loop *.$1 > anim.gif
}
make_animated_gif_with_background () {
    # Fails
    # COMMAND: make_animated_gif sm_sbd2v4 png
    # start
    echo "1:" $1
    echo "2:" $2

    filename1=$(basename "$2")
    extension="${filename1##*.}"
    filename2="${filename1%.*}"
    ending="_withbackground.gif"

    # echo $filename1
    echo $extension
    echo $filename2
    fout=$filename2$ending
    echo $fout

    # convert -dispose Background -delay 40 -loop 0 $1*.$2 animation_$1.gif
    # convert $1 $2 -loop 0 $filename2_withbackground.gif
    convert $1 $2 -loop 0 $fout
    # echo "$filename2" + "_withbackground.gif written with background."

}
make_animated_gif () {
    # COMMAND: make_animated_gif sm_sbd2v4 png
    # start
    echo $1
    echo $2
    # convert +adjoin -delay 40 -loop 0 $1*.$2 animation_$1.gif # combines (as in see all layers simul)
    convert -dispose Background -delay 40 -loop 0 $1*.$2 animation_$1.gif # (see 1 at a time)
    # convert -dispose previous -delay 40 -loop 0 $1*.$2 animation_$1.gif
    # convert -dispose previous -delay 40 -loop 0 $1*.$2 animation_$1.gif # combine

    # convert -dispose Background \
    #         -dispose previous \
    #         -delay 40 \
    #         -loop 0 $1*.$2 animation_$1.gif

    # convert -dispose none  -delay 0 \

    echo "animation_$1.gif written."
}
make_animated_gif $1 $2
# make_animated_gif_dir $1 $2

make_images_smaller () {
    # COMMAND: make_images_smaller sbd2v4 tga
    echo "beginning with:",$1
    echo "ending with:",$2

    for f in $1*.$2
    do
        filename1=$(basename "$f")
        extension="${filename1##*.}"
        filename2="${filename1%.*}"
        echo $f
        # echo $filename1 # same as $f
        # echo $filename2
        # echo $extension

        # convert -dither -colors 256 f f.$2
        # convert -dither $f $f.$2
        # convert $f -resize $size% $filename.smaller.$1 # fails to read "size"

        # 50%: from 49 MB tga became 300kb png
        # 40%: from 49 MB tga became 200kb png
        # convert $f -resize 50% -rotate 180 sm_$filename2.$2 # fails to read "size"
        # convert $f -transparent white -resize 50% -rotate 180 sm_$filename2.$2 # fails to read "size"
        convert $f -transparent white -flip -resize 50% sm_$filename2.$2 # fails to read "size"
        echo sm_$filename2.$2 "written by make_images_smaller!"
        # convert $filename.smaller.$1 $filename.converted.$2
        # rm $filename.smaller.$1
    done
}
make_images_ext () {
    # COMMAND: make_images_ext sm_sbd2v4 tga png
    echo "prefix ",$1 "ending ",$2
    echo $1
    echo $2
    echo $3
    for f in $1*.$2
    do
        filename1=$(basename "$f")
        extension="${filename1##*.}"
        filename2="${filename1%.*}"
        echo $f
        # echo $filename1 # same as $f
        # echo $filename2
        # echo $extension

        convert $f $filename2.$3
        echo $filename2.$3 "written by make_images_ext!"
    done
}
make_gif () {
    echo $1 # sbd2v4
    echo $2 # tga
    filename="sm_$1"
    echo $filename
    make_images_smaller $1 $2
    make_images_ext $filename "tga" "png"
    make_animated_gif $filename "png"
}
