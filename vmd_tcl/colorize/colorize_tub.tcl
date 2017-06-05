# colorize_tub.tcl

proc colorize_monomer { {id 0} { chain_sel "A"} } {
    # BETA monomer.
    set lst_resids {{1 215} {216 384} {385 441}}
    # set lst_colors {10 7 0}
    # 1 red   (west)
    # 7 green (east)
    # 0 blue  (outer/North)
    set lst_colors {1 7 0}

    set len_resids [llength $lst_resids]


    for {set i 1} {$i <= $len_resids} {incr i} {
        # information
        # puts "loop: $i"
        set index [expr $i - 1]
        set resid1 [expr [lindex $lst_resids $index 0]]
        set resid2 [expr [lindex $lst_resids $index 1]]
        # puts "indices $index $i"
        # puts "numbers $resid1 $resid2"

        # molinfo
        set molreps [molinfo $id get numreps]
        # puts "molreps: $molreps"
        set newrep1 [expr $molreps]
        set newrep2 [expr $molreps + 1]

        # color, selection, material
        set color_num [lindex $lst_colors $index]
        # puts $color_num

        # mol representation Tube 0.3 100.0
        # mol modstyle $i $id Tube 0.3 100.0

        mol color ColorID $color_num
        # mol selection chain [lindex $chains 1] and resid $resid1 to $resid2
        mol selection "chain $chain_sel and resid $resid1 to $resid2"
        mol material Opaque
        mol representation NewCartoon 0.32 10.0 4.1 0.0
        mol modstyle $i $id NewCartoon 0.32 10.0 4.1 0.0
        mol addrep $id
    }
};

# proc colorize_monomer_cg { {id 0} {x 1} } {
proc colorize_tubulin_NMC { {id 0} {x 1} } {

    # BETA monomer.
    set lst_resid_a {{0 214} {215 380} {381 438}}
    set lst_resid_b {{439 650} {651 819} {820 866}}

    set xl [expr $x - 1]
    set last_index [lindex $lst_resid_b end 1]
    set last_index [expr $x * $last_index]
    set new_index1 [expr $last_index]
    # set new_index2 [expr $last_index + 1]
    puts "last_index: $last_index"
    # return


    # set lst_colors {10 7 0}
    # 0 blue
    # 1 red
    # 7 green
    set lst_colors {1 7 0}

    set len_resids [llength $lst_resid_a]

    for {set i 1} {$i <= $len_resids} {incr i} {
        # information
        # puts "loop: $i"
        set index [expr $i - 1]
        set resid1 [expr [lindex $lst_resid_a $index 0] + $new_index1]
        set resid2 [expr [lindex $lst_resid_a $index 1] + $new_index1]

        set resid11 [expr [lindex $lst_resid_b $index 0] + $new_index1]
        set resid22 [expr [lindex $lst_resid_b $index 1] + $new_index1 - 1]

        # puts "indices $index $i"
        # puts "numbers $resid1 $resid2"

        # molinfo
        set molreps [molinfo $id get numreps]
        # puts "molreps: $molreps"
        set newrep1 [expr $molreps]
        set newrep2 [expr $molreps + 1]

        # color, selection, material
        set color_num [lindex $lst_colors $index]
        # puts $color_num

        # mol representation Tube 0.3 100.0
        # mol modstyle $i $id Tube 0.3 100.0

        mol color ColorID $color_num
        # mol selection chain [lindex $chains 1] and resid $resid1 to $resid2
        # mol selection "chain $chain_sel and index $resid1 to $resid2"
        mol selection "index $resid1 to $resid2"
        mol material Opaque
        # mol representation NewCartoon 0.32 10.0 4.1 0.0
        # mol modstyle $i $id NewCartoon 0.32 10.0 4.1 0.0
        # mol representation CPK 3.000000 0.600000 10.00000 8.00000
        mol representation CPK 10.000000 3.00000 12.00000 10.00000
        # mol modstyle $i $id CPK 3.000000 0.600000 10.00000 8.00000
        mol addrep $id


        mol color ColorID $color_num
        # mol selection chain [lindex $chains 1] and resid $resid1 to $resid2
        mol selection "index $resid11 to $resid22"
        mol material Opaque
        # mol representation NewCartoon 0.32 10.0 4.1 0.0
        # mol modstyle $i $id NewCartoon 0.32 10.0 4.1 0.0
        # mol representation CPK 3.000000 0.600000 10.00000 8.00000
        mol representation CPK 10.000000 3.00000 12.00000 10.00000
        # mol modstyle $i $id CPK 3.000000 0.600000 10.00000 8.00000
        mol addrep $id
    }
};


proc colorize_tub { {id 0} } {

    puts "usage: colorize_tub <id>"
    # colorize 1tub.
    # red: 1 29 30
    # green: 7 19 20
    # gray: 2
    # mauve/pink: 13

    # set lst_resids {{383 396} {397 412} {413 419} {420 427} {428 432} {433 443} {444 450} {451 460} \
    #                     {461 470} {471 479} {480 491} {492 500} {501 509} {510 522} {523 556} {557 579} {580 595} {596 603}}
    # set lst_colors {    13        19        13        20        13        19        13        19    \
    #                         13       20        20        20         2         30       29         30        29        30}

    mol showrep $id 0 off
    # mol showrep $id 0 on

    set sel [atomselect top all]
    set chains [lsort -ascii -unique [$sel get chain]]
    puts "the current file contains [llength $chains] chain(s)"
    if { [llength $chains] > 1} {
        puts "they are $chains..  the first couple: [lindex $chains 0]   the second: [lindex $chains 1]"
    }
    $sel delete

    # return

    set molreps [molinfo $id get numreps]
    set newrep1 [expr $molreps]
    set newrep2 [expr $molreps + 1]

    # ALPHA-ORANGE
    mol color ColorID 3
    mol selection chain [lindex $chains 0]

    mol material Opaque
    mol representation NewCartoon 0.28 10.0 4.1 0.0
    mol modstyle $newrep1 $id NewCartoon 0.28 10.0 4.1 0.0
    mol addrep $id


    # # BETA-BLUE (CYAN)
    mol color ColorID 10
    mol selection chain [lindex $chains 1]

    mol material Opaque
    mol representation NewCartoon 0.28 10.0 4.1 0.0
    mol modstyle $newrep2 $id NewCartoon 0.28 10.0 4.1 0.0
    mol addrep $id


    # return
    for {set i 0} {$i < [llength $chains]} {incr i} {
        puts $i
        puts [lindex $chains $i]
        colorize_monomer $id [lindex $chains $i]
    }
};
