############################################################################
# cr            (C) Copyright 1995-2007 The Board of Trustees of the
# cr                        University of Illinois
# cr                         All Rights Reserved
############################################################################
# RCS INFORMATION:
#       $RCSfile: .vmdrc,v $
#       $Author: johns $        $Locker:  $                $State: Exp $
#       $Revision: 1.9 $      $Date: 2007/01/12 20:12:44 $
############################################################################
# VMD startup script
############################################################################

# Modified by Dale R. Merz Jr. (merz.drm@gmail.com) Cincinnati 2015.

# turn on lights 0 and 1
light 0 on
light 1 on
light 2 off
light 3 off
# new
display nearclip set 0

# background color
color Display Background white
color Display FPS black
color Axes Labels black
color Labels Bonds black

# position the stage and axes
#axes location lowerleft
axes location off
stage location off

#menu animate  on
#menu edit     on
#menu tracker  on
#menu display  on
#menu color    on
#menu labels   on
#menu renderer on
#menu molecule on

# # menus
# menu main on
# menu main move 3 24

# # display
# # display height 9
# # display distance 2
# # display reposition 925 800
# # display reposition 1550 8 # y x
# Display resize 750 600
# # display resize 600 600
# Display reposition 1000 5
# # display reposition 1000 2 # x y
# # display reposition 4 650
# # display resize 550 675
# stage location off
# display projection orthographic
# display depthcue off
# axes location lowerleft
# axes location Off
# display update

# # file open browser
# menu files on
# menu files move 3 260

# # graphics
# menu graphics on
# menu graphics move 1550 4
# # menu graphics move 1600 24

# position and turn on menus
# menu main     move 1681 512
# menu main     move 3    26
# menu animate  move 3    260
# menu edit     move 3    260
# menu tracker  move 3    260
# menu files    move 3    260
# menu display  move 300  26
# menu graphics move 1600 26
# menu color    move 125  225
# menu molecule move 3    552
# menu labels   move 661  29
# menu render   move 125  525
# menu sequence move 629  0

# menu main     on
# menu graphics on
# menu molecule on
# menu files    on
# display resize 750 600

#menu animate  on
#menu edit     on
#menu tracker  on

#menu color    on
#menu labels   on
#menu renderer on


# position and turn on menus
menu main     on
menu graphics on
menu files    on
menu molecule off

# menu display  on
# menu display  move 300  26 # display settings

# move
# menu main move 5 196
# menu files move 10 10
menu main     move 3    26
menu graphics move 1600 26
menu files    move 3    260
menu molecule move 10   600



# menu animate  move 3    260
# menu edit     move 3    260
# menu tracker  move 3    260
# menu color    move 125  225
# menu labels   move 661  29
# menu render   move 125  525
# menu sequence move 629  0
display resize 800 600

# newly loaded molecules/reps, etc
display projection orthographic
mol default selection all
mol default material Opaque


# colors:
color change rgb red2 1.0 0.4 0.4
color change rgb red3 0.98 0.02 0.078

after idle {
    # menu tkcon on
    if {![info exists env(VMDTEXT)]} {
        menu tkcon on
        # menu tkcon move 250 250
        # menu tkcon resize 600 300
        menu tkcon move 3 700
    }

    # /home/dale/.pylib/vmd_tcl:
    source ~/.pylib/vmd_tcl/animatepsf.tcl
    source ~/.pylib/vmd_tcl/load_molecules.tcl
    source ~/.pylib/vmd_tcl/colorize/colorize.tcl
    source ~/.pylib/vmd_tcl/colorize/colorize_spectrin.tcl
    source ~/.pylib/vmd_tcl/colorize/colorize_nbd_domains.tcl
    source ~/.pylib/vmd_tcl/colorize/colorize_sbd_domains.tcl
    source ~/.pylib/vmd_tcl/colorize/colorize_microtubules.tcl
    source ~/.pylib/vmd_tcl/colorize/colorize_protofilament.tcl
    # source ~/.pylib/vmd_tcl/colorize/colorize_protofilament.tcl
    source ~/.pylib/vmd_tcl/colorize/colorize_hsp110.tcl
    source ~/.pylib/vmd_tcl/colorize/colorize_tub.tcl
    source ~/.pylib/vmd_tcl/evaluate.tcl
    source ~/.pylib/vmd_tcl/take_picture.tcl


    # source ~/.pylib/vmd_tcl/make_movie.tcl
    # logfile current.vmd
    # colorize.tcl
    # colorize_spectrin.tcl
    # colorize_nbd_domains.tcl
    # colorize_sbd_domains.tcl
    # evaluate.tcl
    # make_movie.tcl
    # take_picture.tcl
    # colorize_hsp110.tcl
    # trajectory_movie_short_modified.tcl
    # gopython1.py
    # examples.tcl
    # animatepsf.tcl
    # load_force_frames.tcl
    # rmsd.tcl

    # from other people:
    source ~/.pylib/vmd_tcl/macdermaid_misc.tcl
}

proc write_vector { vec filename } {
    set fid [open $filename w]
    foreach elem $vec { puts $fid $elem }
    close $fid
}
proc fx { } {
    # Rotate (flip) protein 180 degrees around x axis
    set sel [atomselect top all]
    $sel move [transaxis x 180]
    $sel delete
}
proc fy { } {
    # Rotate (flip) protein 180 degrees around y axis
    set sel [atomselect top all]
    $sel move [transaxis y 180]
    $sel delete
}
proc fz { } {
    # Rotate (flip) protein 180 degrees around z axis
    set sel [atomselect top all]
    $sel move [transaxis z 180]
    $sel delete
}

## Rotate molecule to bring bond between id1, id2 along +/- x, y, or z
proc bondto {axis sel id1 id2} {
    set idx [$sel get index]
    set xyz [$sel get {x y z}]

    set v {}
    lappend v [lindex $xyz [lsearch -exact -integer $idx $id1]]
    lappend v [lindex $xyz [lsearch -exact -integer $idx $id2]]

    #Moves COM of the molecule to the origin
    $sel moveby [vecscale -1.0 [measure center $sel weight mass]]

    ## Rotate to bring along x
    set r [vecinvert [vecsub {*}$v]]
    $sel move [transvecinv $r]

    ## Check for +/- orientation along x
    set a [vecdot $r {1 0 0}]
    if {$a < 0.0} {
        $sel move [transaxis z 180]
    }

    switch -- $axis {
        x {}
        y {$sel move [transaxis z -90 deg]}
        z {$sel move [transaxis y 90 deg]}
        -x {$sel move [transaxis z 180 deg]}
        -y {$sel move [transaxis z 90 deg]}
        -z {$sel move [transaxis y -90 deg]}
        default {puts "axis must be x, y or z"}
    }
}


# +-------------------+
# |      Axel's hacks |
# +-------------------+
# if { 1 } {
#     # modified to include VMD Main
#     # define global variable to store X window id.
#     set vmd_opengl_wid -1
#     global vmd_opengl_wid
#     set vmd_main_wid -1
#     global vmd_main_wid

#     # callback function to be called when the top molecule changes
#     proc vmd_change_window_name {args} {
#         global vmd_main_wid
#         global vmd_opengl_wid
#         if {[molinfo num] < 1} return

#         if {[llength $args] == 0} {
#             set name [join [molinfo top get name]]
#         } else {
#             set name [lindex $args 0]
#             if { [string equal $name vmd_molecule] } {
#                 set name [join [molinfo top get name]]
#             }
#         }
#         if {$vmd_opengl_wid > 0} {
#             catch {exec xprop -id $vmd_opengl_wid \
#                        -set WM_NAME "VMD: $name"}
#             catch {exec xprop -id $vmd_opengl_wid \
#                        -set WM_ICON_NAME $name}
#         }
#         if {$vmd_main_wid > 0} {
#             catch {exec xprop -id $vmd_main_wid \
#                        -set WM_NAME "VMD Main: $name"}
#             catch {exec xprop -id $vmd_main_wid \
#                        -set WM_ICON_NAME $name}
#         }
#     }

#     # activate callback
#     trace variable vmd_molecule w vmd_change_window_name

#     # record window id for automatic title change
#     after idle {
#         global vmd_opengl_wid
#         if {![catch {exec xwininfo -name \
#                          "VMD [vmdinfo version] OpenGL Display"} val ]} {
#             set vmd_opengl_wid [lindex $val 3]
#         }
#         if {![catch {exec xwininfo -name \
#                          "VMD Main"} val ]} {
#             set vmd_main_wid [lindex $val 3]
#         }
#         vmd_change_window_name
#     }

# }

# USER ADD KEYS ************************
# n v c b k m o h W w q
user add key n {
    mol selection all
    mol representation Licorice .2 4
    mol color ResID
    mol addrep top
    mol delrep 0 top
    display update
}
user add key v {
    mol selection all
    mol representation VDW 1.2000 27.000000
    mol color Name
    mol material Opaque
    mol addrep top
    mol delrep 0 top
    display update
}
user add key c {
    mol selection all
    mol representation CPK {1.300000 0.600000 10 8}
    mol color Name
    mol addrep top
    mol delrep 0 top
    display update
}
user add key b {
    mol selection all
    mol representation Lines {2}
    mol color ResID
    mol addrep top
    mol delrep 0 top
    display update
}

user add key i {
    # new
    #Moves geometry center of the molecule to the origin
    set sel999 [atomselect top all]
    $sel999 moveby [vecscale -1.0 [measure center $sel999]]
    $sel999 delete
}

user add key k {
    mol selection {protein and resid 1 and name CA}
    mol representation VDW {1.2 27}
    mol color ResId
    mol addrep top
    mol delrep 0 top
    display update
}
user add key m {
    mol selection all
    mol representation NewCartoon {.28 16 4}
    mol color Structure
    mol addrep top
    mol delrep 0 top
    display update
}
user add key o {
    mol selection all
    mol representation Lines 1
    mol color Name
    mol addrep top
    mol delrep 0 top
    display update
}
user add key h {
    mol selection all
    mol representation Cartoon 2
    mol color structure
    mol addrep top
    mol delrep 0 top
    display update
}
user add key w {
    color Display Background white
}
user add key W {
    color Display Background black
}
user add key q {
    #switches depthcue on and off
    if {[string compare [display get depthcue] on] == 0} {
        display depthcue off
    } {
        display depthcue   on
        display cuestart   0.500000
        display cueend     10.000000
        display cuedensity 0.400000
        display cuemode    Exp2
    }

}
display depthcue off

# +-----------------+
# | REPRESENTATIONS |
# +-----------------+
# ----------------------------------------------------------------------
#Apply preselected graphical representation

set numreps 0
set selrep 0
set repstat 0
set numreptype 6

proc changerep {repstat} {
    global numreps selrep

    #   mol delrep $numreps top

    switch $repstat {
        0 {
            mol modstyle $selrep top Licorice 0.2 10 10
            mol modcolor $selrep top Name

        }
        1 {
            mol modstyle $selrep top NewRibbons 1.800000 6.000000 2.600000 0
            mol modcolor $selrep top Chain
        }
        2 {
            mol modstyle $selrep top Licorice 0.2 10 10
            mol modcolor $selrep top ResType
        }
        3 {
            mol modstyle $selrep top Trace 0.500000 6.000000
            mol modcolor $selrep top Index
        }
        4 {
            mol modstyle $selrep top vdw
            mol modcolor $selrep top ResType
        }
        5 {
            mol modstyle $selrep top lines
            mol modcolor $selrep top Name
        }
        6 {
            mol modstyle $selrep top QuickSurf
            mol modcolor $selrep top Name
        }
        7 {
        }
        default {
            mol modstyle $selrep top lines
            mol modcolor $selrep top Name
        }
    }

    if {$numreps < 0} {set numreps 0}
}

# ----------------------------------------------------------------------
user add key g {
    draw color red
    draw cylinder {-100 0 0} {100 0 0} radius 0.5
    draw cone {2 0 0} {5 0 0} radius 1 resolution 12
    draw color green
    draw cylinder {0 -100 0} {0 100 0} radius 0.5
    draw cone {0 2 0} {0 5 0} radius 1 resolution 12
    draw color blue
    draw cylinder {0 0 -100} {0 0 100} radius 0.5
    draw cone {0 0 2} {0 0 5} radius 1 resolution 12

    for {set i -100} {$i <= 100} {incr i} {
        draw color red
        set v1 "-1 $i 0"
        set v2 "1 $i 0"
        set v3 "-1 0 $i"
        set v4 "1 0 $i"
        draw cylinder $v1 $v2 radius 0.05
        draw cylinder $v3 $v4 radius 0.05
        draw color green
        set v1 "0 -1 $i"
        set v2 "0 1 $i"
        set v3 "$i -1 0"
        set v4 "$i 1 0"
        draw cylinder $v1 $v2 radius 0.05
        draw cylinder $v3 $v4 radius 0.05
        draw color blue
        set v1 "$i 0 -1"
        set v2 "$i 0 1"
        set v3 "0 $i -1"
        set v4 "0 $i 1"
        draw cylinder $v1 $v2 radius 0.05
        draw cylinder $v3 $v4 radius 0.05
    }

    for {set i -20} {$i <= 20} {incr i} {
        draw color red
        set v1 "-100 [expr ($i*5)] 0"
        set v2 "100 [expr ($i*5)] 0"
        set v3 "-100 0 [expr ($i*5)]"
        set v4 "100 0 [expr ($i*5)]"
        draw cylinder $v1 $v2 radius 0.1
        draw cylinder $v3 $v4 radius 0.1
        draw color green
        set v1 "0 -100 [expr ($i*5)]"
        set v2 "0 100 [expr ($i*5)]"
        set v3 "[expr ($i*5)] -100 0"
        set v4 "[expr ($i*5)] 100 0"
        draw cylinder $v3 $v4 radius 0.1
        draw cylinder $v1 $v2 radius 0.1
        draw color blue
        set v1 "[expr ($i*5)] 0 -100"
        set v2 "[expr ($i*5)] 0 100"
        set v3 "0 [expr ($i*5)] -100"
        set v4 "0 [expr ($i*5)] 100"
        draw cylinder $v3 $v4 radius 0.1
        draw cylinder $v1 $v2 radius 0.1
    }

    for {set i -10} {$i <= 10} {incr i} {
        draw color red
        set v1 "-100 [expr ($i*10)] 0"
        set v2 "100 [expr ($i*10)] 0"
        set v3 "-100 0 [expr ($i*10)]"
        set v4 "100 0 [expr ($i*10)]"
        draw cylinder $v1 $v2 radius 0.2
        draw cylinder $v3 $v4 radius 0.2
        draw color green
        set v1 "0 -100 [expr ($i*10)]"
        set v2 "0 100 [expr ($i*10)]"
        set v3 "[expr ($i*10)] -100 0"
        set v4 "[expr ($i*10)] 100 0"
        draw cylinder $v1 $v2 radius 0.2
        draw cylinder $v3 $v4 radius 0.2
        draw color blue
        set v1 "[expr ($i*10)] 0 -100"
        set v2 "[expr ($i*10)] 0 100"
        set v3 "0 [expr ($i*10)] -100"
        set v4 "0 [expr ($i*10)] 100"
        draw cylinder $v3 $v4 radius 0.2
        draw cylinder $v1 $v2 radius 0.2
    }
}

user add key {O} {
    #Reset Display
    display projection orthographic
}
user add key {P} {
    #Reset Display
    display projection perspective
}
user add key {*} {
    #Reset Display
    display resetview
}
user add key {=} {
    #goes to the next animation frame
    animate next
}

# user add key f {
#     #Flips  -  Rotates scene 180 degrees aroynd Y (vertical on screen) axis
#     rotate y by 180
# }
# user add key q {
#     #Rotates scene to make a view from X axis, z is up
#     mouse stoprotation
#     rotate x to -90
#     rotate y by -90
# }
# user add key w {
#     #Rotates scene to make a view from Y axis, z is up
#     mouse stoprotation
#     rotate z to 180
#     rotate x by -90
# }
# user add key e {
#     #Rotates scene to make a view from Z axis, x is to the left
#     mouse stoprotation
#     rotate z to 180
# }

user add key o {
    #draws coordinate cylinders in origin
    draw color red
    draw cylinder {-100 0 0} {100 0 0} radius 0.5
    draw cone {2 0 0} {5 0 0} radius 1 resolution 12
    draw color green
    draw cylinder {0 -100 0} {0 100 0} radius 0.5
    draw cone {0 2 0} {0 5 0} radius 1 resolution 12
    draw color blue
    draw cylinder {0 0 -100} {0 0 100} radius 0.5
    draw cone {0 0 2} {0 0 5} radius 1 resolution 12

}

user add key d {
    #removes all the graphics added
    draw delete all
}
# m/M are toggles m --> New Rep, M --> del Rep
user add key m {
    mol addrep top
    incr numreps
    if {$numreps > 0} { incr selrep }
}
user add key M {
    mol delrep $selrep top
    if {$numreps > -1} {
        set numreps [expr {$numreps - 1}]
        if {$selrep > 0} { set selrep [ expr {$selrep - 1} ] }
    }
}
# n/N are toggles N --> Next Rep, n --> Prev Rep
user add key n {
    if {$repstat <= 0} {
        set repstat $numreptype
    } else {
        set repstat [ expr {$repstat - 1} ]
    }
    changerep $repstat
}
user add key N {
    if {$repstat >= $numreptype} {
        set repstat 0
    } else {
        incr repstat
    }
    changerep $repstat
}
## Cycle Active Representations
user add key b {
    if {$selrep < $numreps} {
        incr selrep
    } else {
        set selrep 0
    }
    puts "Selection: $selrep"
}

user add key B {
    if {$selrep > 0} {
        set selrep [ expr {$selrep - 1} ]
    } elseif {$numreps <= 0} {
        set selrep 0
    } else {
        set selrep $numreps
    }
    puts "Selection: $selrep"
}

# user add key 0 {
#     mouse mode 4 0
#     menu labels on
# }


# user add key v {
#     #sets white background and exp2 depth cue
#     color Display {Background} white

#     display depthcue   on
#     display cuestart   0.500000
#     display cueend     10.000000
#     display cuedensity 0.400000
#     display cuemode    Exp2
# }

# user add key V {
#     #sets black background without depthcue
#     color Display {Background} black

#     display depthcue   off
# }

# user add key p {
#     #switches depthcue on and off
#     if {[string compare [display get depthcue] on] == 0} {
#         #Switch depthcue off
#         display depthcue off
#     } {
#         #Switch depthcue on
#         display depthcue   on
#         #       display cuestart   0.500000
#         #       display cueend     10.000000
#         #       display cuedensity 0.400000
#         #       display cuemode    Exp2
#     }

# }


# user add key u {
#     #makes the selections of the top molecule to auto update each frame
#     set n [molinfo top get numreps]
#     for {set i 0} {$i < $n} {incr i} {
#         mol selupdate $i top on
#     }
# }


# MATERIALS:
# ----------------------------------------------------------------------
# define a new, very transparent material 'Glass'
material add Glass
material change ambient   Glass 0.00
material change specular  Glass 0.50
material change diffuse   Glass 0.65
material change shininess Glass 0.53
material change opacity   Glass 0.15

# define a new, semitransparent strictly white material 'Slice', for making protein crossection pictures
material add Slice
material change ambient   Slice 1.00
material change specular  Slice 0.00
material change diffuse   Slice 1.00
material change shininess Slice 0.00
material change opacity   Slice 0.75

# define a new, non-shiny white material 'Gypsum', for making BW protein pictures
material add Gypsum
material change ambient Gypsum 0.000000
material change specular Gypsum 1.000000
material change diffuse Gypsum 1.000000
material change shininess Gypsum 0.000000
material change opacity Gypsum 1.000000

# define a new, non-shiny gray material 'Smog', for making BW protein crossections
material add Smog
material change ambient Smog 0.400000
material change specular Smog 0.000000
material change diffuse Smog 0.000000
material change shininess Smog 0.000000
material change opacity Smog 1.000000
# ----------------------------------------------------------------------
