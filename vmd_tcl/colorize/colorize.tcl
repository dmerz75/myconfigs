# colorize

proc get_molinfo {} {

    for {set i 0} {$i < [molinfo top get numreps]} {incr i} {
        lassign [molinfo top get "{rep $i} {selection $i} {color $i}"] a b c
        puts "view $i:"
        puts " representation: $a"
        puts " selection: $b"
        puts " coloring method: $c"
    };                          #
};                              #



proc colorize_with_list { rep lst_resids lst_colors {diff 0} {run_type gsop}} {
    # des.

    set len_resids [llength $lst_resids]

    for {set i 1} {$i <= $len_resids} {incr i} {

        # information
        # puts "loop: $i"
        set index [expr $i - 1]
        set resid1 [expr [lindex $lst_resids $index 0] - $diff]
        set resid2 [expr [lindex $lst_resids $index 1] - $diff]

        # type & color
        set str_tube {mol modstyle $i 0 Tube 1.0 100.0}
        set str_cpk {mol modstyle $i 0 CPK 3.000000 0.600000 10.00000 8.00000}
        set str_new {mol modstyle $i 0 NewCartoon 0.28 26 4}

        # #   397 - 412 - beta_2_short (with turn)          ||
        mol addrep 0
        mol selection all
        mol material Opaque

        # Standard simple if with else clause
        if {$run_type == "gsop"} {
            # puts "the value of run_type is $run_type, = gsop!"
            mol modselect $i 0 resid $resid1 to $resid2
        } else {
            # puts "the value of run_type is $run_type, not gsop!"
            mol modselect $i 0 protein and resid $resid1 to $resid2
        }

        mol modcolor $i 0 ColorID [lindex $lst_colors $index]
        # # mol modstyle 1 0 CPK 3.000000 0.600000 10.00000 8.00000
        # # switch $rep tube {$str_tube} cpk {$str_cpk} new {$str_new} default {$str_tube}
        switch $rep tube {set sel $str_tube} cpk {set sel $str_cpk} new {set sel $str_new} default {set sel $str_tube}
        eval $sel
    }
}

proc colorize_nucleotide {} {
    mol addrep 0
    mol selection all
    mol material Opaque
    # original
    # mol modselect 1 0 resid 1 to 39 116 to 188
    mol modselect 6 0 "resid > 384"
    mol modcolor 6 0 ColorID 16
    mol modstyle 6 0 CPK 4.000000 0.600000 10.00000 8.00000

    # mol addrep 0
    # IA Green 7
}
proc add_endpoint { {id 0} {residue_num 0} {ball_color 1} } {
    # add VDW balls of color gray:first and blue:last
    # mol delete all - deletes everything

    # mol addrep 0
    mol selection resid $residue_num and name CA
    mol representation VDW 2.000 14.000
    mol color ColorID $ball_color
    # Gray
    mol material Opaque
    mol addrep $id

    # # mol addrep 0
    # mol selection resid $last and name CA
    # mol representation VDW 1.3000 12.0000
    # mol color ColorID 0
    # # Blue
    # mol material Opaque
    # mol addrep 0
}
proc add_endpoint_by_index { {id 0} {index 0} {ball_color 1} } {
    # id index color(numeral)
    mol selection index $index
    mol representation VDW 4.000 10.000
    mol color ColorID $ball_color
    mol material Opaque
    mol addrep $id
}
proc delete_reps { {id 0} {start 1} {stop 1} } {
    set rep_count [molinfo $id get numreps]
    puts "total reps: $rep_count"

    for {set i $start} {$i < $stop} {incr i} {
        # information
        puts "loop: $i"
        mol delrep $i $id
    }

    set rep_count [molinfo $id get numreps]
    puts "total reps: $rep_count"

}
proc add_endpoints { first last } {
    # add VDW balls of color gray:first and blue:last
    # mol delete all - deletes everything

    # mol addrep 0
    mol selection resid $first and name CA
    mol representation VDW 2.000 26.0000
    mol color ColorID 2
    # Gray
    mol material Opaque
    mol addrep 0

    # mol addrep 0
    mol selection resid $last and name CA
    mol representation VDW 2.0000 26.0000
    mol color ColorID 0
    # Blue
    mol material Opaque
    mol addrep 0
}
proc colorize_sopnucleonbd {} {
    # mol delete all
    for {set i 0} {$i<7} {incr i} {
        mol delrep $i 0
    }
    colorize_nbd_domains_tube
    colorize_nucleotide
    add_endpoints 1 383
    calc_distance 1 383
}


proc make_current_reps_invisible { {id 0} } {
    # Get the # of current representations.
    # Make them invisible. (deactivate)
    set molreps [molinfo $id get numreps]

    for {set i 0} {$i < $molreps} {incr i} {
        mol showrep $id $i off
    }

    return $molreps
}
