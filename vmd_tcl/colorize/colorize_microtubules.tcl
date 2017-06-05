# example!
# proc clear_drawings {} {
#     draw delete all
#     # display resetview
#     # draw materials off
#     # display update
# }

# my stuff starts here! ----------

puts "available functions include: get_plate_vector, orient_mt, colorize_mt, see_cantilever, colorize_plate, draw_indent_vector"

# Globals
# plate is chain M
# set mchain [atomselect top "chain M"]
# set mt [atomselect top "not chain M or not chain T"]
# set mt [atomselect top "chain A or chain B"]
# puts "t1, t2, mchain, mt are available with t1_resid,t2_resid: $t1_resid, $t2_resid"




proc describe_mt { } {
    puts "alpha tubulin 439"
    puts "alphas = minus(-) end"
    puts "generally, orange/longitudinal South"
    puts "beta tubulin 427"
    puts "betas = plus(+) end"
    puts "generally, cyan-blue/longitudinal North"
}

proc mtinfo { {molid 0} args } {

    puts "usage: mtinfo <molid> args(optional)"
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
    set filename "mtinfo_retraction_$string1.out"
    set fp [open $filename w]
    puts $fp "maxframe $num_frames"
    puts $fp "frames $string1"

    puts $fp "reffilename mt.ref.pdb mt.rev.pdb"
    puts $fp "run      100     -> $string1"
    puts $fp "numsteps 900 mil -> 600 mil"
    puts $fp "DeltaX   0.00004 -> 0.00008"
    puts $fp "Chip, Tip, Direction"
    puts $fp "coordinates mt.pdb -> frame$args.pdb"
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
    # return




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



    # for {set i 0} {$i < $num_frames} {incr i} {
    #     set value [lsearch $args $i]
    #     if {$value < 0} {
    #         # echo
    #     } {
    #         animate goto $i
    #         # set pos1 [$t1 get {x y z}]
    #         # set pos2 [$t2 get {x y z}]
    #         # set x1 [$t1 get {x}]
    #         # set y1 [$t1 get {y}]
    #         # set z1 [$t1 get {z}]
    #         # set x2 [$t2 get {x}]
    #         # set y2 [$t2 get {y}]
    #         # set z2 [$t2 get {z}]

    #         # puts "frame $i of $num_frames :> $value"
    #         # puts "t1: $pos1"
    #         # puts "t2: $pos2"

    #         # # file write
    #         # puts $fp "frame $i of $num_frames"
    #         # # puts $fp "t1 $pos1"
    #         # # puts $fp "t2 $pos2"

    #         # puts [format "chip t1   %7.3f %7.3f %7.3f" $x1 $y1 $z1]
    #         # puts $fp [format "chip t1   %7.3f %7.3f %7.3f" $x1 $y1 $z1]
    #         # puts [format "tip  t2   %7.3f %7.3f %7.3f" $x2 $y2 $z2]
    #         # puts $fp [format "tip  t2   %7.3f %7.3f %7.3f" $x2 $y2 $z2]

    #         $mol_sel writepdb frame$i.pdb
    #     }
    # }
    # # end for loop.
}

# proc see_mt { {molid 0} } {
proc see_mt { } {

    set molid [molinfo num]
    # puts "usage: see_mt id=$molid"
    puts "usage: see_mt"
    puts "loading $molid"

    # $ >>>$ load('psf','alanin.psf','dcd','alanin.dcd')
    # num(): Returns the number of loaded molecules.
    # listall(): Returns the molid's of the all the loaded molecules.
    # exists(molid): Returns true if the molid corresponds to an existing molecule.
    # new(name): Creates a new empty molecule with the given name and returns its id.
    # load(structure, sfname, coor, cfname): Load a molecule with structure type
    # structure and filename sfname. Additionally, a separate coordinate file
    # may be provided, of type coor and name cfname. New in VMD 1.8: All frames
    # from cfname will be processed before the function returns. If successful,
    # the function will return the id of the new molecule.

    mol new
    set fpdb [glob *.ref.pdb]
    puts $fpdb
    mol addfile $fpdb

    # mol addfile mt.ref.pdb [catch {exec xmgrace -dpipe 0 << $input &} msg]
    # try { mol addfile mt.ref.pdb }
    # on error { }
    # {
    #     mol addfile MT.ref.pdb
    # }
    # mol addfile mt.ref.pdb
    # return

    # mol addfile {mt.ref.pdb} type {pdb} first 0 last -1 step 1 waitfor 1 3
    # mol addfile ./dcd/mt_d100_indent.dcd waitfor all
    set dcdfile [glob -type f dcd/*.dcd]
    mol addfile $dcdfile waitfor all
    # puts "$dcdfile"
    # return


    set curdir [pwd]
    # puts "curdir $curdir"
    set dirlength [llength [file split $curdir]]
    # puts "$dirlength"
    set dirlength1 [expr {$dirlength - 1}]
    # puts "$dirlength $dirlength1"
    set curdirname [lrange [file split $curdir] $dirlength1 end]
    puts "cwd $curdirname"
    set dirnamelength [string length $curdirname]
    set minus10 [expr {$dirnamelength - 13}]
    set new_mol_name [string range $curdirname $minus10 $dirnamelength]
    # puts "$dirnamelength $minus10 $new_mol_name"
    # return
    mol rename $molid $new_mol_name




    # animate style Loop
    # mol addfile {./dcd/mt_d100_indent.dcd} type {dcd} first 0 last -1 step 1 waitfor -1 3
    animate goto 0
    display resetview
    set all [atomselect top "all"]
    see_cantilever $molid
    colorize_mt $molid
    # colorize_plate $molid
    draw_indent_vector $molid
    display resetview
    animate goto end
    rotate x by 30.00
    rotate y by 15.00
    rotate z by 30.00
}

proc see_mtball { } {
    # Uses colorize_mtball to render microtubule as a large set of
    # spheres.

    set molid [molinfo num]
    puts "usage: see_mt"
    puts "loading $molid"

    mol new
    mol addfile mt.ref.pdb
    set dcdfile [glob -type f dcd/*.dcd]
    mol addfile $dcdfile waitfor all


    set curdir [pwd]
    set dirlength [llength [file split $curdir]]
    set dirlength1 [expr {$dirlength - 1}]
    set curdirname [lrange [file split $curdir] $dirlength1 end]
    puts "cwd $curdirname"
    set dirnamelength [string length $curdirname]
    set minus10 [expr {$dirnamelength - 10}]
    set new_mol_name [string range $curdirname $minus10 $dirnamelength]
    mol rename $molid $new_mol_name

    # animate style Loop
    animate goto 0
    display resetview
    set all [atomselect top "all"]
    see_cantilever $molid
    # colorize_mt $molid
    colorize_mtball $molid
    # draw_indent_vector $molid
    draw_indent_vector250 $molid
    display resetview
    animate goto end
    rotate x by 30.00
    rotate y by 15.00
    rotate z by 30.00
}


proc see_cantilever { {id 0} { res1 -1 } { res2 -1 } } {
    # global t1_resid t2_resid

    set t1 [atomselect $id "chain T and resid 1"]
    set t2 [atomselect $id "chain T and resid 2"]
    set t1_resid [$t1 get resid]
    set t2_resid [$t2 get resid]


    # puts "$t1_resid and $t2_resid"
    # puts "$res1 and $res2"
    if {$res1 == -1 } {
        set res1 $t1_resid
        # puts "res1 is now $res1"
    }

    if {$res2 == -1 } {
        set res2 $t2_resid
        # puts "res2 is now $res2"
    }
    # add VDW balls of color gray:first and blue:last
    # mol delete all - deletes everything

    # set rep_count [molinfo $id get numreps]
    # puts $rep_count
    # set new_rep1 [expr $rep_count]
    # set new_rep2 [expr $rep_count + 1]

    # mol addrep 0
    mol selection resid $res1 and chain T
    # mol representation VDW 33.000 40.0000
    mol representation Beads 10.00000 30.000000
    mol color ColorID 11
    # Gray
    # mol material Opaque
    mol material Transparent
    mol addrep $id

    # mol addrep 0
    mol selection resid $res2 and chain T
    # mol representation VDW 79.0000 40.0000
    mol representation Beads 99.00000 30.000000
    # mol modstyle 1 0 Beads 10.000000 30.000000
    mol color ColorID 2
    # Blue
    # mol material Opaque
    mol material Transparent
    mol addrep $id
}

proc rotate_mt_long { {id 0} {deg 180} } {
    # X axis
    # global mt

    set mt [atomselect $id "chain A or chain B"]

    # global mchain
    # puts "original 30.01 35.37 107.58"
    measure minmax $mt

    set orig_pos [lindex [measure minmax $mt] 0]
    # puts "lindexed first $orig_pos"
    set x1 [lindex $orig_pos 0]
    set y1 [lindex $orig_pos 1]
    set z1 [lindex $orig_pos 2]
    # puts "$x1 $y1 $z1"
    set orig_pos_2f [format "%0.2f %0.2f %0.2f" $x1 $y1 $z1]
    puts "original position: $orig_pos_2f"

    # COM
    set com [measure center $mt weight mass]
    set matrix [transaxis x $deg]

    $mt moveby [vecscale -1.0 $com]
    $mt move $matrix
    $mt moveby $com

    # measure minmax $mchain
    measure minmax $mt

    # write rotated position
    set new_pos [lindex [measure minmax $mt] 0]
    # puts "lindexed first $new_pos"
    # set nx1 [lindex $new_pos 0]
    # set ny1 [lindex $new_pos 1]
    # set nz1 [lindex $new_pos 2]
    # set new_pos_2f [format "%0.2f %0.2f %0.2f" $nx1 $ny1 $nz1]
    # puts "the new position: $new_pos_2f"
    puts "the new position: $new_pos"

    # move back into original position
    set vector_orig_new [vecsub $new_pos $orig_pos]
    puts "translate by: $vector_orig_new"
    set v1 [vecinvert $vector_orig_new]
    puts "opp translate: $v1"
    $mt moveby $v1
    measure minmax $mt
}

proc rotate_mt_lat { {id 0} {deg 180} } {
    # Z axis
    # global mt
    set mt [atomselect $id "chain A or chain B"]
    measure minmax $mt

    set orig_pos [lindex [measure minmax $mt] 0]
    set x1 [lindex $orig_pos 0]
    set y1 [lindex $orig_pos 1]
    set z1 [lindex $orig_pos 2]
    set orig_pos_2f [format "%0.2f %0.2f %0.2f" $x1 $y1 $z1]
    puts "original position: $orig_pos_2f"

    # COM
    set com [measure center $mt weight mass]
    set matrix [transaxis z $deg]

    $mt moveby [vecscale -1.0 $com]
    $mt move $matrix
    $mt moveby $com

    # measure minmax $mchain
    measure minmax $mt

    # write rotated position
    set new_pos [lindex [measure minmax $mt] 0]
    puts "the new position: $new_pos"

    # move back into original position
    set vector_orig_new [vecsub $new_pos $orig_pos]
    puts "translate by: $vector_orig_new"
    set v1 [vecinvert $vector_orig_new]
    puts "opp translate: $v1"
    $mt moveby $v1
    measure minmax $mt
}

proc translate_mt_x { {id 0} {vmove {1.0 0.0 0.0} } } {
    set t1 [atomselect $id "chain T and resid 1"]
    set t2 [atomselect $id "chain T and resid 2"]

    set t2coord [lindex [$t2 get {x y z}] 0]
    # $t1 get {x y z}
    puts $t2coord

    # nudge along x
    # global mt

    set mt [atomselect $id "chain A or chain B"]
    measure minmax $mt

    set orig_pos [lindex [measure minmax $mt] 0]
    set x1 [lindex $orig_pos 0]
    set y1 [lindex $orig_pos 1]
    set z1 [lindex $orig_pos 2]
    set orig_pos_2f [format "%0.2f %0.2f %0.2f" $x1 $y1 $z1]
    puts "original position: $orig_pos_2f"

    measure minmax $mt

    # # COM
    # # set com [measure center $mt weight mass]
    # # set matrix [transaxis z $deg]

    # # $mt moveby [vecscale -1.0 $com]
    # # $mt move $matrix
    # # $mt moveby $com

    # # set newcoords {}
    # # foreach coord [$sel get {x y z}] {
    # #     lvarpush newcoords [vecadd $coord $vmove]
    # # }
    # $sel set $newcoords
    # # $mt moveby {}


    # # measure minmax $mchain
    # measure minmax $mt

    # # write rotated position
    # set new_pos [lindex [measure minmax $mt] 0]
    # puts "the new position: $new_pos"

    # # move back into original position
    # # set vector_orig_new [vecsub $new_pos $orig_pos]
    # # puts "translate by: $vector_orig_new"
    # # set v1 [vecinvert $vector_orig_new]
    # # puts "opp translate: $v1"
    # # $mt moveby $v1
    # # measure minmax $mt
}

proc rotate_90 { {id 0} {vmove {0.0 0.0 0.0}} } {

    set sel [atomselect $id "chain A or chain B"]

    set matrix [transaxis y 90]
    $sel move $matrix
    $sel moveby $vmove
}

proc place_upper_mt { sel } {
    puts "did you rotate_90 first?"

    # TO USE: ----
    # set id5 [atomselect top all]
    # rotate_90 $id5
    # place_upper_mt $id5
    # ------------

    # global mt
    # global mchain
    # $mt moveby { 0.0 -1.56 0.0 }

    # fails ...
    # {-217.416015625 307.36700439453125 375.24200439453125} {586.447021484375 575.717041015625 649.9010009765625}
    # {-75.0 0.0 -75.0} {665.0 390.0 993.0}
    # set v0 {-75 -0 -75}

    # mtonly_seamdown
    # {-200.0 280.0 285.0} {603.863037109375 548.3499755859375 559.6589965820313}
    set v0 {-200.0 280.0 285.0}

    set sel [atomselect top all]
    measure minmax $sel
    set new_pos [lindex [measure minmax $sel] 0]

    set vector_new [vecsub $new_pos $v0]
    set vector_inew [vecinvert $vector_new]
    $sel moveby $vector_inew
    measure minmax $sel
}

proc move_mt { {vmove {0.0 0.0 0.0}} } {
    global mt
    global mchain
    # $mt moveby { 0.0 -1.56 0.0 }

    set matrix [transaxis y 90]
    # $mt move $matrix
    $mt moveby $vmove

}

# proc draw_vector_to_plate { {molid 0} {sel 0 } }  {
proc draw_indent_vector { {molid 0} }  {
    # get the min and max values for each of the directions
    # (I'm not sure if this is the best way ... )
    # set sel [atomselect top all]
    set sel [atomselect $molid "chain T and resid 2"]
    puts $sel

    set sel_coords [$sel get {x y z}]
    puts $sel_coords

    set coords [lsort -real [$sel get x]]
    set minx [lindex $coords 0]
    set maxx [lindex [lsort -real -decreasing $coords] 0]

    set coords [lsort -real [$sel get y]]
    set miny [lindex $coords 0]
    set maxy [lindex [lsort -real -decreasing $coords] 0]

    set coords [lsort -real [$sel get z]]
    set minz [lindex $coords 0]
    set maxz [lindex [lsort -real -decreasing $coords] 0]

    puts $minx
    puts $maxx
    puts $miny
    puts $maxy
    puts $minz
    puts $maxz

    # global mchain
    set mchain [atomselect $molid "chain M"]
    set mcoords [lsort -real [$mchain get y]]
    set mminy [lindex $mcoords 0]
    set mmaxy [lindex [lsort -real -decreasing $mcoords] 0]
    # puts $mminy
    # puts $mmaxy

    # and draw the lines
    draw materials off
    draw color red
    # draw line $pos_begin $pos_end
    draw line "$minx $miny $minz" "$maxx $mminy $minz" width 20 style dashed
}
proc draw_indent_vector250 { {molid 0} { ylow 0.0 } }  {

    mol top $molid

    set sel [atomselect $molid "chain T and resid 2"]
    set pos1 [expr [$sel get {x y z}]]

    set x1 [expr [$sel get {x}]]
    set y1 [expr [$sel get {y}]]
    set y1 $ylow
    set z1 [expr [$sel get {z}]]

    # and draw the lines
    draw materials off
    draw color red
    draw line "$x1 $y1 $z1" $pos1 width 20 style dashed
}

proc get_plate_vector {} {
    # global mchain
    set mchain [atomselect top "chain M"]

    # make list
    set mlist [$mchain get index]

    # get index: first & last
    set m_start [lindex $mlist 0]
    set m_stop [lindex $mlist end]

    # select atoms
    set c1 [atomselect top "index $m_start"]
    set c2 [atomselect top "index $m_stop"]

    # make vector
    set pos_start [measure center $c1]
    set pos_stop [measure center $c2]

    # get plate vector
    set vector [vecsub $pos_stop $pos_start]
    set distance [veclength $vector]

    # print
    puts $vector
    puts $distance

    return $vector
}

proc orient_mt { vector {orient 1.5} } {
    puts "this moves the molecule ..."
    display resetview
    set all [atomselect top "all"]
    $all move [transvecinv $vector]

    rotate y by 14
    rotate z by 5
    rotate x by 30
    scale by $orient
}

proc colorize_plate { {id 0} {color 2} } {
    # plate is chain M
    # global mchain
    set mchain [atomselect $id "chain M"]

    # make list
    set mlist [$mchain get index]

    # get index: first & last
    set m_start [lindex $mlist 0]
    set m_stop [lindex $mlist end]

    set rep_count [molinfo $id get numreps]
    puts $rep_count
    # return

    # add rep to molecule id eventually ...
    set new1 [expr $rep_count]

    # set str_vdw "mol modstyle $new1 $id VDW 2.000000 12.000000"
    # new0 - plate
    puts $color
    set m_select "chain M and index $m_start to $m_stop"
    mol selection $m_select
    mol representation Beads 9.0 10.0
    mol material Opaque
    mol modselect $new1 $id $m_select
    mol color ColorID $color
    mol addrep $id
}

proc colorize_mt { {id 0} {color 2} } {
    # colorize mt

    # # plate is chain M
    # global mchain
    set mchain [atomselect $id "chain M"]

    # make list
    set mlist [$mchain get index]

    # get index: first & last
    set m_start [lindex $mlist 0]
    set m_stop [lindex $mlist end]

    set rep_count [molinfo $id get numreps]
    puts $rep_count
    # return

    # add rep to molecule id eventually ...
    set new1 [expr $rep_count]
    set new2 [expr $rep_count + 1]
    set new3 [expr $rep_count + 2]
    # puts "the value of the new reps are: $new1 $new2 $new3"

    set str_vdw "mol modstyle $new1 $id VDW 2.000000 12.000000"

    # PLATE
    # # new0 - plate
    # puts $color
    # set m_select "chain M and index $m_start to $m_stop"
    # mol selection $m_select
    # # mol representation VDW 2.0 12.0
    # mol representation Beads 9.0 10.0
    # mol material Opaque
    # mol modselect $new1 $id $m_select
    # mol color ColorID $color
    # # puts $str_vdw
    # # eval $str_vdw
    # # mol modcolor $new1 $id ColorID $color
    # mol addrep $id
    # PLATE

    # new1 - mt
    # set str_lin2 "mol modstyle $new2 $id Lines 1.000000"
    mol selection "chain A"
    # mol representation Lines 3.0
    mol representation Points 9.0 # 5-9
    # mol representation Beads 2.0
    mol material Opaque
    mol color ColorID 3
    # puts $str_lin2
    # eval $str_lin2
    # mol modcolor $new2 $id ColorID 0
    mol addrep $id

    # new2 - mt
    # set str_lin2 "mol modstyle $new2 $id Lines 1.000000"
    mol selection "chain B"
    # mol representation Lines 3.0
    mol representation Points 9.0 # 5-9
    # mol representation Beads 2.0
    mol material Opaque
    mol color ColorID 10
    # puts $str_lin2
    # eval $str_lin2
    # mol modcolor $new3 $id ColorID 1
    mol addrep $id

}


proc colorize_mtball { {id 0} } {
    # colorize mt
    mol showrep $id 0 0

    # 259, 15, 204, 387, 235, 270
    # 16,
    # 169
    # A-202
    # B-199

    # mol selection "chain A and resid 200"
    # mol selection "chain A and resid 198"
    mol selection "chain A and resid 202"
    # mol representation Points 80.0
    mol representation VDW 21.0 10.0
    mol material Opaque
    mol color ColorID 3
    mol addrep $id

    # mol selection "chain B and resid 200"
    # mol selection "chain B and resid 198"
    mol selection "chain B and resid 199"
    # mol representation Points 80.0
    mol representation VDW 21.0 10.0
    mol material Opaque
    mol color ColorID 10
    mol addrep $id
}

# colorize_mt 0 vdw


# my stuff ends here! ------------



# http://musingsonsoftware.blogspot.com/2013_08_01_archive.html
# Contact Maps using VMD
# Contact maps are a quick way to identify residues of a protein (or monomer) that interact with residue from another protein, ligand or monomer. The script below helps obtain a distance list:

proc contact_map {} {
    set seg1 [atomselect top "segname SG03 and name CA"]
    set seg2 [atomselect top "segname SG04 and name CA"]

    set file [open "vmd_contact_map.dat" w]

    set list1 [$seg1 get index]
    set list2 [$seg2 get index]

    foreach atom1 $list1 {
        foreach atom2 $list2 {
            set index1 [atomselect top "index $atom1"]
            set index2 [atomselect top "index $atom2"]
            set resid1 [[atomselect top "index $atom1"] get resid]
            set resid2 [[atomselect top "index $atom2"] get resid]
            set resnm1 [[atomselect top "index $atom1"] get resname]
            set resnm2 [[atomselect top "index $atom2"] get resname]
            puts $file "$resnm1 $resid1 $resnm2 $resid2 [veclength [vecsub [measure center $index1] [measure center $index2]]]"
            $index1 delete
            $index2 delete
        }
        puts $file " "   # I include this line to make it easier to make contour plots using gnuplot.
    }
    close $file
}

# Posted by Pavan K. Ghatty at 1:50 PM 2 comments:
# Labels: VMD
# Aligning hexameric proteins along an axis
# This tcl script aligns a hexamer such that its central axis is aligned along the y-axis.
# This script is also applicable to trimers, tetramers and other aggregates that have a well defined central axis.
proc some_rotation {} {
    set all [atomselect top protein]
    $all moveby [vecscale [measure center $all] -1]

    set res10 [atomselect top "resid 10"]
    set res40 [atomselect top "resid 40"]

    set cenres10 [measure center $res10]
    set cenres40 [measure center $res40]

    set vector [vecsub $cenres10 $cenres40]

    $all move [transvecinv $vector]
    $all move [transaxis z 90]

    foreach i {A B C D E F} {
        set chain [atomselect top "chain $i and protein and resid 4 to 105"]
        $chain writepdb chain$i.pdb
    }
}
proc show_fixed_points { {id 0} {diff 0} } {
    # colorize the SBD of Hsp70 in the tube,cpk, or (new)cartoon representations

    source ~/.pylib/vmd_tcl/colorize.tcl

    # fixed points
    # set lst_fixed {98 105 87000 88555}

    # fixed_beads 234
    set lst_fixed {245
        250
        254
        259
        322
        323
        326
        345
        346
        1111
        1116
        1120
        1125
        1188
        1189
        1192
        1211
        1212
        1977
        1982
        1986
        1991
        2054
        2055
        2058
        2077
        2078
        2843
        2848
        2852
        2857
        2920
        2921
        2924
        2943
        2944
        3709
        3714
        3718
        3723
        3786
        3787
        3790
        3809
        3810
        4575
        4580
        4584
        4589
        4652
        4653
        4656
        4675
        4676
        5441
        5446
        5450
        5455
        5518
        5519
        5522
        5541
        5542
        6307
        6312
        6316
        6321
        6384
        6385
        6388
        6407
        6408
        7173
        7178
        7182
        7187
        7250
        7251
        7254
        7273
        7274
        8039
        8044
        8048
        8053
        8116
        8117
        8120
        8139
        8140
        8905
        8910
        8914
        8919
        8982
        8983
        8986
        9005
        9006
        9771
        9776
        9780
        9785
        9848
        9849
        9852
        9871
        9872
        10637
        10642
        10646
        10651
        10714
        10715
        10718
        10737
        10738
        89734
        89812
        89813
        89816
        89857
        89860
        89861
        90039
        90043
        88868
        88946
        88947
        88950
        88991
        88994
        88995
        89173
        89177
        88002
        88080
        88081
        88084
        88125
        88128
        88129
        88307
        88311
        87136
        87214
        87215
        87218
        87259
        87262
        87263
        87441
        87445
        86270
        86348
        86349
        86352
        86393
        86396
        86397
        86575
        86579
        85404
        85482
        85483
        85486
        85527
        85530
        85531
        85709
        85713
        84538
        84616
        84617
        84620
        84661
        84664
        84665
        84843
        84847
        83672
        83750
        83751
        83754
        83795
        83798
        83799
        83977
        83981
        82806
        82884
        82885
        82888
        82929
        82932
        82933
        83111
        83115
        81940
        82018
        82019
        82022
        82063
        82066
        82067
        82245
        82249
        81074
        81152
        81153
        81156
        81197
        81200
        81201
        81379
        81383
        80208
        80286
        80287
        80290
        80331
        80334
        80335
        80513
        80517
        79342
        79420
        79421
        79424
        79465
        79468
        79469
        79647
        79651 }


    set len_fixed [llength $lst_fixed]

    for {set i 1} {$i <= $len_fixed} {incr i} {
        # information
        # puts "loop: $i"
        set index [expr $i - 1]
        set fixed_point [expr [lindex $lst_fixed $index 0] - $diff]
        # 0 1 (the zeroeth position)
        puts "index $index"
        puts "fixed point: $fixed_point"

        add_endpoint_by_index $id $fixed_point 1

        # type & color
        # mol selection all
        # mol material Opaque
        # mol modcolor $i $id ColorID [lindex $lst_colors $index]
        # mol modcolor $i $id ColorID 1
        # mol addrep $id
    }
    set rep_count [molinfo $id get numreps]
    puts "total reps: $rep_count"
}
# alpha 439, beta 427;
proc show_fixed_points_alpha { {id 0} {diff 0} } {
    # colorize the SBD of Hsp70 in the tube,cpk, or (new)cartoon representations

    source ~/.pylib/vmd_tcl/colorize.tcl

    # fixed points
    # set lst_fixed {98 105 87000 88555}

    # fixed_beads 234
    set lst_fixed {245
        250
        254
        259
        322
        323
        326
        345
        346
        1111
        1116
        1120
        1125
        1188
        1189
        1192
        1211
        1212
        1977
        1982
        1986
        1991
        2054
        2055
        2058
        2077
        2078
        2843
        2848
        2852
        2857
        2920
        2921
        2924
        2943
        2944
        3709
        3714
        3718
        3723
        3786
        3787
        3790
        3809
        3810
        4575
        4580
        4584
        4589
        4652
        4653
        4656
        4675
        4676
        5441
        5446
        5450
        5455
        5518
        5519
        5522
        5541
        5542
        6307
        6312
        6316
        6321
        6384
        6385
        6388
        6407
        6408
        7173
        7178
        7182
        7187
        7250
        7251
        7254
        7273
        7274
        8039
        8044
        8048
        8053
        8116
        8117
        8120
        8139
        8140
        8905
        8910
        8914
        8919
        8982
        8983
        8986
        9005
        9006
        9771
        9776
        9780
        9785
        9848
        9849
        9852
        9871
        9872
        10637
        10642
        10646
        10651
        10714
        10715
        10718
        10737
        10738
    }


    set len_fixed [llength $lst_fixed]

    for {set i 1} {$i <= $len_fixed} {incr i} {
        # information
        # puts "loop: $i"
        set index [expr $i - 1]
        set fixed_point [expr [lindex $lst_fixed $index 0] - $diff]
        # 0 1 (the zeroeth position)
        puts "index $index"
        puts "fixed point: $fixed_point"

        add_endpoint_by_index $id $fixed_point 1

        # type & color
        # mol selection all
        # mol material Opaque
        # mol modcolor $i $id ColorID [lindex $lst_colors $index]
        # mol modcolor $i $id ColorID 1
        # mol addrep $id
    }
    set rep_count [molinfo $id get numreps]
    puts "total reps: $rep_count"
}
