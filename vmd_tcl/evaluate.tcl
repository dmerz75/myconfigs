# evaluate.tcl

# Examples:
# draw line {0 0 0} {0 2 0} style dashed

proc generalloop { {molid 0} args } {
    puts "usage: contacts <molid> args(optional)"
    puts "begin code evaluation: ..."

    # Molecule VMD information.
    set top_mol [molinfo top]
    set first_mol [molinfo index 0]
    set num_mol [molinfo num]
    set lst_molid [molinfo list]

    puts "the top moleculeid is $top_mol"
    puts "the first molecule loaded is $first_mol"
    puts "there are $num_mol loaded."
    puts "they are: $lst_molid"
    puts "evaluating $molid"

    # Molecule major properties.
    set mol_sel [atomselect $molid "not chain M and not chain T"]
    set num_atoms_total [molinfo $molid get numatoms]
    set num_atoms [$mol_sel num]
    set num_frames [molinfo $molid get numframes]

    puts "the total num_atoms_total: $num_atoms_total"
    puts "the num_atoms: $num_atoms"
    puts "the num_frames: $num_frames"

    # outfiles.
    set string1 [join $args "_"]
    puts "$string1"
    set filename "contactinfo_$string1.out"
    set fp [open $filename w]
    puts $fp "maxframe $num_frames"
    puts $fp "frames $string1"

    # puts $fp "reffilename mt.ref.pdb mt.rev.pdb"
    # puts $fp "run      100     -> $string1"
    # puts $fp "numsteps 900 mil -> 600 mil"
    # puts $fp "DeltaX   0.00004 -> 0.00008"
    # puts $fp "Chip, Tip, Direction"
    # puts $fp "coordinates mt.pdb -> frame$args.pdb"
    # puts -nonewline $fp $data
    # puts $fp "more data"

    # return

    # set us [lindex [time $someTclCode] 0]
    # puts [format "%.2f seconds to execute" [expr {$us / 1e6}]]

    # Cantilever Properties.
    set t1 [atomselect $molid "chain T and resid 1"]
    set t2 [atomselect $molid "chain T and resid 2"]

    # for loop.
    puts "the list: $args"
    for {set i 0} {$i < $num_frames} {incr i} {
        set value [lsearch $args $i]
        if {$value < 0} {
            # echo
        } {
            animate goto $i
            set pos1 [$t1 get {x y z}]
            set pos2 [$t2 get {x y z}]
            set x1 [$t1 get {x}]
            set y1 [$t1 get {y}]
            set z1 [$t1 get {z}]
            set x2 [$t2 get {x}]
            set y2 [$t2 get {y}]
            set z2 [$t2 get {z}]

            puts "frame $i of $num_frames :> $value"
            puts "t1: $pos1"
            puts "t2: $pos2"

            # file write
            puts $fp "frame $i of $num_frames"
            # puts $fp "t1 $pos1"
            # puts $fp "t2 $pos2"

            puts [format "chip t1   %7.3f %7.3f %7.3f" $x1 $y1 $z1]
            puts $fp [format "chip t1   %7.3f %7.3f %7.3f" $x1 $y1 $z1]
            puts [format "tip  t2   %7.3f %7.3f %7.3f" $x2 $y2 $z2]
            puts $fp [format "tip  t2   %7.3f %7.3f %7.3f" $x2 $y2 $z2]

            $mol_sel writepdb frame$i.pdb
        }
    }
    # end for loop.

    # close file.
    close $fp

}

proc general_list { {molid 0} {rep Tube} } {

    # NOT IMPLEMENTED

    # colorize the SBD of Hsp70 in the tube

    # residue segments
    # alternatively replace 383 with 397
    # set lst_resids {{383 412} {413 419} {420 427} {428 434} {435 443} {444 450} {451 460} {461 470} {471 501} {502 508} {509 557} {558 579} {580 603}}
    # set lst_resids {{383 396} {397 412} {413 419} {420 427} {428 432} {433 443} {444 450} {451 460} {461 470} {471 501} {502 508} {509 522} {523 556} {557 579} {580 595} {596 603}}
    set lst_resids {{383 396} {397 412} {413 419} {420 427} {428 432} {433 443} {444 450} {451 460} {461 470} {471 500} {501 509} {510 522} {523 556} {557 579} {580 595} {596 603}}
    set lst_colors {13 18 13 17 13 12 13 12 13 3 1 0 10 0 10 0}
    set len_resids [llength $lst_resids]

    set num_frames [molinfo $molid get numframes]

    for {set f 0} {$f < $num_frames} {incr f} {

        for {set i 1} {$i <= $len_resids} {incr i} {

            # information
            # puts "loop: $i"
            set index [expr $i - 1]
            set resid1 [expr [lindex $lst_resids $index 0]]
            set resid2 [expr [lindex $lst_resids $index 1]]
            # puts "indices $index $i"
            # puts "numbers $resid1 $resid2"


            # color, selection, material
            set color_num [lindex $lst_colors $index]
            puts $color_num
            mol color ColorID $color_num
            mol selection resid $resid1 to $resid2
            mol material Opaque

            # Info) mol color ColorID 2
            # Info) mol representation Tube 0.500000 100.000000
            # Info) mol selection resid 491 to 500
            # Info) mol material Opaque
            # Info) mol addrep 1

            if {$color_num == 13} {
                # mol representation $rep 4.7 0.5 10.0 8.0
                mol representation Tube 0.5 100.0
                mol modstyle $i $id Tube 0.5 100.0
            } else {
                mol representation Tube 0.9 100.0
                mol modstyle $i $id Tube 0.9 100.0
            }

            mol addrep $id
        }
        colorize_sbd_hsa $id
    }
}

proc get_pdb_property { } {


}

proc load_pdbs { } {

    set infiles [glob */*.ent]

    # puts $infiles
    set start 0
    set stop [llength $infiles]

    for {set i $start} {$i < $stop} {incr i} {

        set pdbfile [lindex $infiles $i]
        # puts "$i [lindex $infiles $i]"
        puts "$i $pdbfile"

        mol new
        mol addfile $pdbfile
        set molecule1 [atomselect top "all"]
        puts [$molecule1 num]
        puts $molecule1 molindex
        $molecule1 delete
        mol delete [$molecule1 molindex]
        puts "molecule deleted."
    }
}

proc draw_bond { first last sel_color } {
    # provide resid

    # select color
    # graphics top color $sel_color
    # set color $sel_color
    draw color $sel_color

    # get CA
    set ca1 [atomselect top "resid $first and name CA"]
    set ca2 [atomselect top "resid $last and name CA"]

    # get atom index of CA
    set atom1 [$ca1 get index]
    set atom2 [$ca2 get index]

    # draw bond line
    # 0/1 0/3217
    # label add Atoms 0/$first
    # label add Atoms 0/$last
    # label add Bonds 0/$first 0/$last
    # label add Atoms 0/$atom1
    # label add Atoms 0/$atom2


    # add label
    # label textsize 2.00
    # label textthickness 2.70

    # label color $sel_color
    # color Labels Bonds black
    label add Bonds 0/$atom1 0/$atom2
}
proc draw_cone { x y z {size 1.0} {sel_color red}} {
    # provide resid
    # select color
    # graphics top color $sel_color
    # set color $sel_color
    draw color $sel_color
    set X [expr $x-$size]
    set Y [expr $y-$size]
    set Z [expr $z-$size]
    puts "$X $Y $Z"
    # puts {X Y Z}
    # draw cone {X Y Z} {$x $y $z} radius 0.15
    draw cone "$X $Y $Z" "$x $y $z" radius 1.0

}
proc draw_dashed_line { resfirst reslast {sel_color black}} {
    # DON'T USE - can't erase

    # set top
    # set $id top

    # and draw the lines
    draw materials off
    draw color $sel_color

    # draw a black dashed line
    # get CA
    set ca1 [atomselect top "resid $resfirst and name CA"]
    set ca2 [atomselect top "resid $reslast and name CA"]

    # get atom index of CA
    # set atom1 [$ca1 get index]
    # set atom2 [$ca2 get index]

    # get {x y z}
    set coords1 [$ca1 get {x y z}]
    set coords2 [$ca2 get {x y z}]

    # get vectors
    set pos_begin [measure center $ca1]
    set pos_end   [measure center $ca2]

    # subtract vectors; $end - $begin for vecsub
    set vector12 [vecsub $pos_end $pos_begin]
    set distance12 [veclength $vector12]

    puts $vector12
    puts $distance12

    # mol load graphics dashed_line
    # graphics top list
    # graphics $id color $sel_color
    # graphics 0 line $pos_begin $vector12 width 8 style dashed
    # graphics $id line $pos_begin $pos_end width 8 style dashed

    draw line $pos_begin $pos_end width 8 style dashed


    # graphics top delete $id
    # graphics top info $id


    # graphics top line {0 0 0} {3 0 0} style dashed
    # graphics $id line $pos_begin $pos_end width 8 style dashed


    # foreach i $coords2 j $coords1 {
    #     set xdist [vecsub $i $j]
    #     lappend xyz $xdist
    # }
}



proc box_molecule { {molid 0} } {
    # get the min and max values for each of the directions
    # (I'm not sure if this is the best way ... )
    set sel [atomselect top all]

    set coords [lsort -real [$sel get x]]
    set minx [lindex $coords 0]
    set maxx [lindex [lsort -real -decreasing $coords] 0]

    set coords [lsort -real [$sel get y]]
    set miny [lindex $coords 0]
    set maxy [lindex [lsort -real -decreasing $coords] 0]

    set coords [lsort -real [$sel get z]]
    set minz [lindex $coords 0]
    set maxz [lindex [lsort -real -decreasing $coords] 0]

    # and draw the lines
    draw materials off
    draw color blue
    draw line "$minx $miny $minz" "$maxx $miny $minz"
    draw line "$minx $miny $minz" "$minx $maxy $minz"
    draw line "$minx $miny $minz" "$minx $miny $maxz"

    draw line "$maxx $miny $minz" "$maxx $maxy $minz"
    draw line "$maxx $miny $minz" "$maxx $miny $maxz"

    draw line "$minx $maxy $minz" "$maxx $maxy $minz"
    draw line "$minx $maxy $minz" "$minx $maxy $maxz"

    draw line "$minx $miny $maxz" "$maxx $miny $maxz"
    draw line "$minx $miny $maxz" "$minx $maxy $maxz"

    draw line "$maxx $maxy $maxz" "$maxx $maxy $minz"
    draw line "$maxx $maxy $maxz" "$minx $maxy $maxz"
    draw line "$maxx $maxy $maxz" "$maxx $miny $maxz"
}

proc clear_drawings {} {
    draw delete all
    # display resetview
    # draw materials off
    # display update
}
proc get_graphics { } {
    mol load graphics testing
    # Loading new molecule ...
    graphics top list

    graphics top delete 1
    graphics top exists 0
    graphics top exists 1
    graphics top info 0
    # sphere {0.100000 0.200000 0.300000} radius 0.400000 resolution 6
    # graphics top replace 0
    # graphics top point {3.3 2.2 1.1}
    graphics top info 0
    # point {3.300000 2.200000 1.100000}


    # graphics top sphere {0.1 0.2 0.3} radius 0.4
    # graphics top cylinder {-1 -1 -1} {2.6 2.5 2.4} resolution 3
    # graphics top line {0 0 0} {3 0 0} style dashed

}
proc calc_distance { first last } {
    # provide resid (CA will be selected)

    # get CA
    set ca1 [atomselect top "resid $first and name CA"]
    set ca2 [atomselect top "resid $last and name CA"]

    # get {x y z}
    set coords1 [$ca1 get {x y z}]
    set coords2 [$ca2 get {x y z}]

    # set vector12 [vecsub [lindex $coordinates2] [lindex $coordinates1]]
    set pos_begin [measure center $ca1]
    set pos_end   [measure center $ca2]

    # get the protein vector; $end - $begin for vecsub
    set vector12 [vecsub $pos_end $pos_begin]
    set distance12 [veclength $vector12]

    # print
    puts $vector12
    puts $distance12
}

proc geometric_center {selection} {
    # set the geometrical center to 0
    set gc [veczero]
    # [$selection get {x y z}] returns a list of {x y z}
    #    values (one per atoms) so get each term one by one
    foreach coord [$selection get {x y z}] {
        # sum up the coordinates
        set gc [vecadd $gc $coord]
    }
    # and scale by the inverse of the number of atoms
    return [vecscale [expr 1.0 /[$selection num]] $gc]
}

proc center_of_mass {selection} {
    # some error checking
    if {[$selection num] <= 0} {
        error "center_of_mass: needs a selection with atoms"
    }
    # set the center of mass to 0
    set com [veczero]
    # set the total mass to 0
    set mass 0
    # [$selection get {x y z}] returns the coordinates {x y z}
    # [$selection get {mass}] returns the masses
    # so the following says "for each pair of {coordinates} and masses,
    #  do the computation ..."
    foreach coord [$selection get {x y z}] m [$selection get mass] {
        # sum of the masses
        set mass [expr $mass + $m]
        # sum up the product of mass and coordinate
        set com [vecadd $com [vecscale $m $coord]]
    }
    # and scale by the inverse of the number of atoms
    if {$mass == 0} {
        error "center_of_mass: total mass is zero"
    }
    # The "1.0" can't be "1", since otherwise integer division is done
    return [vecscale [expr 1.0/$mass] $com]
}
proc get_mass {selection} {
    # some error checking
    if {[$selection num] <= 0} {
        error "get_mass: needs a selection with atoms"
    }
    # set the center of mass to 0
    set com [veczero]
    # set the total mass to 0
    set mass 0
    # [$selection get {x y z}] returns the coordinates {x y z}
    # [$selection get {mass}] returns the masses
    # so the following says "for each pair of {coordinates} and masses,
    #  do the computation ..."
    foreach coord [$selection get {x y z}] m [$selection get mass] {
        # sum of the masses
        set mass [expr $mass + $m]
        # sum up the product of mass and coordinate
        # set com [vecadd $com [vecscale $m $coord]]
    }
    # and scale by the inverse of the number of atoms
    if {$mass == 0} {
        error "get_mass: total mass is zero"
    }
    # The "1.0" can't be "1", since otherwise integer division is done
    # return [vecscale [expr 1.0/$mass] $com]
    return $mass
}

proc move_over { {molid 0} {x 0.0} {y 0.0}  {z 0.0} } {

    puts "setting xyz"
    # set x [lindex args 0]
    # set y [lindex args 1]
    # set z [lindex args 2]

    set num_frames [molinfo $molid get numframes]
    puts "num_frames: $num_frames"
    puts "x:$x y:$y z:$z"

    set everything [atomselect $molid all]

    $everything moveby {$x $y $z}
    # for {set i 0} {$i < $num_frames} {incr i} {
    #     $everything moveby {$x $y $z}
    # }
}
