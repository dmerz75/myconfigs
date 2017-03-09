# take_picture.tcl

proc make_my_movie { {name "pictures"} {start 0} {stop 0} {step 1} args} {
    puts "make_my_movie name start stop step"
    puts "turned tga off .."
    # make movie screen, height/width 550
    # display resize 550 550

    # get the number of frames in the movie
    # set num [molinfo top get numframes]

    # set y file isdirectory movies
    if {[file isdirectory movies]} {
        # the directory 'movies' exists
        puts "directory exists .."
    } else {
        # create the directory
        file mkdir movies
    }

    # loop through the frames
    for {set i $start} {$i <= $stop} {incr i $step} {
        # go to the given frame
        puts $i
        animate goto $i

        set result [lsearch $args $i]
        puts $result

        # for the display to update
        # display update

        # --- name the picture ---
        # set filename movies/$name.[format "%06d" $i]
        # set filenamed movies/$name.[format "%06d" $i].dat
        # set filename1 movies/$name.[format "%06d" $i].pov
        set filename2 movies/$name.[format "%06d" $i].tga
        set filename4 movies/$name.[format "%06d" $i].png
        # set filename3 movies/$name.[format "%06d" $i].ps

        # render snapshot $filename
        # render snapshot $filename display %s # pauses, puts up display

        # works               # povray +W%w +H%h -I%s -O%s.tga +D +X +A +FT
        # render POV3 $filename povray +W%w +H%h -I%s -O%s.tga +D +X +A +FT
        # render POV3 $filename +W%w +H%h -I%s -O%s.tga +D +X +A +FT
        # render POV3 $filename -I%s -O%s.tga +D +X +A +FT
        # render POV3 $filename -I%s -O%s

        # +D +X +A +FT +Q10
        #                         $+H500 +W400 -I%s -O%s.tga +D +X +A +FT

        # --- RENDER the picture ---
        # render POV3 $filename1 -I%s -O%s
        # tachyon  -aasamples 12 %s -format TARGA -o %s.tga
        # render Tachyon $filename2 "/usr/bin/tachyon -aasamples 12 %s -format Targa -res 1024 1024 -o %s"
        # render Tachyon $filename2 "/usr/bin/tachyon -aasamples 12 %s -format TARGA -res 1024 1024 -o %s"
        # render Tachyon $filename4 "/usr/bin/tachyon %s -format PNG -res 1024 1024 -o %s"


        # USE THIS!
        # render Tachyon $filename2 "/usr/bin/tachyon -aasamples 12 %s -format TARGA -res 512 512 -o %s"
        render Tachyon $filename4 "/usr/bin/tachyon %s -format PNG -res 1024 768 -o %s"


        # render Tachyon $filename2 "/usr/bin/tachyon -aasamples 12 %s -format TARGA -res 2048 2048 -o %s"
        # render Tachyon $filename4 "/usr/bin/tachyon %s -format PNG -res 2048 2048 -o %s"



        # render Tachyon $filename2 "/usr/bin/tachyon -aasamples 12 %s -format Targa -res 2048 2048 -o %s"


        ### From >>> /usr/bin/tachyon
        # Output Options:
        # -res Xres Yres  override scene-defined output image size
        # -o outfile.tga  set output file name
        # -clamp          clamp pixel values to [0 to 1) (** default)
        # -normalize      normalize pixel values to [0 to 1)
        # -gamma val      normalize apply gamma correction
        # -format BMP     24-bit Windows BMP  (uncompressed)
        # -format JPEG    24-bit JPEG         (compressed, but lossy)
        # -format PNG     24-bit PNG          (compressed, lossless)
        # -format PPM     24-bit PPM          (uncompressed)
        # -format PPM48   48-bit PPM          (uncompressed)
        # -format PSD48   48-bit PSD          (uncompressed)
        # -format RGB     24-bit SGI RGB      (uncompressed)
        # -format TARGA   24-bit Targa        (uncompressed) **

        # render POV3 $filename1 -I%s -O%s
        # render Tachyon $filename "/usr/bin/tachyon -aasamples 12 %s -format TGA -res 4096 4096 -o %s.tga"

        # povray +H500 +W400 -I%s -O%s.tga +D +X +A +FT
        # also works
        # render Tachyon $filenamed tachyon -mediumshade %s -o %s.tga
        # render Tachyon scene.dat "/Users/username/tachyon_MACOSXX86 -aasamples 12 %s -format TGA -res 1024 1024 -o %s.tga"

        # testing
        # render < %s -sgi %s.rgb; ipaste %s.rgb

        # render Tachyon $filenam2 tachyon -mediumshade %s -o %s.tga
        # render Tachyon $filenam2 -mediumshade %s -o %s.tga
        # render Tachyon $molec$t tachyon -aasamples 4 -trans_vmd -mediumshade %s
        # -format TARGA -o %s.tga
        # testing -fails
        # render Tachyon $filename tachyon -mediumshade %s -o %s.tga
        # no ghostview program
        # ghostview $filenam3 &
        # maybe
        # render POV3 $filenam2 povray +W%w +H%h -I%s -O%s.tga +D +X +A +FT

    }
}
proc take_movie_pics_rgb { {start 0} {stop 0} {step 1} {name "movie"}} {
    # make movie screen, height/width 550
    # display resize 550 550

    # get the number of frames in the movie
    # set num [molinfo top get numframes]

    # set y file isdirectory movies
    if {[file isdirectory movies]} {
        # the directory 'movies' exists
        puts "directory exists .."
    } else {
        # create the directory
        file mkdir movies
    }

    # loop through the frames
    for {set i $start} {$i <= $stop} {incr i $step} {

        # puts step
        puts $i

        # go to the given frame
        animate goto $i

        # for the display to update
        display update


        # take the picture
        # set filename snap.[format "%04d" [expr $i/$step]].rgb
        set filename movies/$name.[format "%06d" $i].rgb
        render snapshot $filename
    }
}
proc make_movie1 {delay {name "movie"}} {
    # proc convert_to_movie {args} {}
    # exec {*}[auto_execok ls] {*}$args
    # exec {*}[auto_execok convert] {*}$args
    # convert   -delay 20   -loop 0   sphere*.gif   animatespheres.gif
    exec {*}[convert -delay $delay $name.*.rgb animation.gif]
}

proc make_trajectory_movie {start stop step} {

    # get the number of frames in the movie
    # set num [molinfo top get numframes]


    # loop through the frames
    for {set i $start} {$i < $stop} {incr i $step} {

        # go to the given frame
        animate goto $i

        # for the display to update
        display update


        # take the picture
        set filename snap.[format "%04d" [expr $i/$step]].rgb
        render snapshot $filename

    }
}

proc take_povray_picture { {file_name "pic1"} } {
    # render POV3 $file_name.pov povray +W%w +H%h -I%s -O%s.tga +D +X +A +FT
    render POV3 $file_name.pov povray +W%w +H%h -I%s -O%s.tga +D +X +A +FT
}
proc rotating_movie { file_name } {
    # render POV3 nbd1.pov povray +W%w +H%h -I%s -O%s.tga +D +X +A +FT
    # proc make_rotation_movie_files {} {
    # }

    set frame 0
    for {set i 0} {$i < 360} {incr i 4} {
        set filename snap.[format "%04d" $frame].rgb
        render snapshot $filename
        # render POV3 $file_name.pov povray +W%w +H%h -I%s -O%s.tga +D +X +A +FT
        incr frame
        rotate y by 4
    }
}

proc take_picture {args} {
  global take_picture

  # when called with no parameter, render the image
  if {$args == {}} {
    set f [format $take_picture(format) $take_picture(frame)]
    # take 1 out of every modulo images
    if { [expr $take_picture(frame) % $take_picture(modulo)] == 0 } {
      render $take_picture(method) $f
      # call any unix command, if specified
      if { $take_picture(exec) != {} } {
        set f [format $take_picture(exec) $f $f $f $f $f $f $f $f $f $f]
        eval "exec $f"
       }
    }
    # increase the count by one
    incr take_picture(frame)
    return
  }
  lassign $args arg1 arg2
  # reset the options to their initial stat
  # (remember to delete the files yourself
  if {$arg1 == "reset"} {
    set take_picture(frame)  0
    set take_picture(format) "./animate.%04d.rgb"
    set take_picture(method) snapshot
    set take_picture(modulo) 1
    set take_picture(exec)    {}
    return
  }
  # set one of the parameters
  if [info exists take_picture($arg1)] {
    if { [llength $args] == 1} {
      return "$arg1 is $take_picture($arg1)"
    }
    set take_picture($arg1) $arg2
    return
  }
  # otherwise, there was an error
  error {take_picture: [ | reset | frame | format  | \
  method  | modulo ]}
}
# to complete the initialization, this must be the first function
# called.  Do so automatically.
take_picture reset


proc make_movie {} {
    set num [molinfo top get numframes]
    # loop through the frames
    for {set i 0} {$i < $num} {incr i} {
        # go to the given frame
        animate goto $i
        # force display update
        display update
        # take the picture
        take_picture
        }
}
