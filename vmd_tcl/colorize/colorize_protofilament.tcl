# colorize protofilament:



proc call_colorize_indices { {id 0} {index1 0} {index2 1} {colorid 16} } {
    # call colorize_indices 0 300

    set rep_count [molinfo $id get numreps]
    puts "current reps: $rep_count"
    set rep_count [expr [molinfo $id get numreps] + 1]
    puts "soon to be: $rep_count"

    mol selection "index $index1 to $index2"

    mol material Opaque
    mol representation CPK {3.500000 2.500000 9 8}
    # mol representation Lines 3.0
    mol color ColorID $colorid
    # puts $str_lin2
    # eval $str_lin2
    # mol modcolor $new2 $id ColorID 0
    mol addrep $id
}

# proc colorize_index_protofilament { {id 0} } {
proc colorize_protofilament { {id 0} } {
    # description: <chain number> <index> <final index>
    # 0     0   426
    # 1   427   845

    # colorize_indices 0 0 426 0
    # colorize_indices 0 427 845 1

    # index file
    set infile [glob indices_*.dat]
    # puts $infile

    #  Slurp up the data file
    set fp [open $infile r]
    set file_data [read $fp]
    close $fp

    #  Process data file
    set data [split $file_data "\n"]

    # loop
    set line_count 0
    foreach line $data {
        # do some line processing here
        incr line_count

        # remove whitespace
        regsub -all -- {[[:space:]]+} $line " " line

        set line_items [split $line]
        # {} 14 5641 5940 ... note the leading space

        # set variables
        set chain [lindex $line_items 1]
        set index [lindex $line_items 2]
        set final_index [lindex $line_items 3]
        # puts "$chain $index $final_index"


        # if < 4, skip ..
        set len_line [llength $line_items]
        if { $len_line==4 } {

            set diff [expr $final_index - $index]
            puts $diff

            if { $diff==426 || $diff==419 } {
                # orange 3
                call_colorize_indices $id $index $final_index 3
            }
            if { $diff==418} {
                # cyan 10
                call_colorize_indices $id $index $final_index 10
                # call_colorize_indices $id $index $final_index 1
            }
            if { $diff<300} {
                # purple 11
                # call_colorize_indices $id $index $final_index 11
                call_colorize_indices $id $index $final_index 1
            }
        }
    }
    # end foreach
}

proc colorize_index_file { {id 0} {filename "foreach" }} {
    # description: <chain number> <index> <final index>
    # 0     0   426
    # 1   427   845

    # colorize_indices 0 0 426 0
    # colorize_indices 0 427 845 1

    # index file
    puts $filename
    set infile [glob indices_*$filename*.dat]
    puts $infile
    # return


    #  Slurp up the data file
    set fp [open $infile r]
    set file_data [read $fp]
    close $fp

    #  Process data file
    set data [split $file_data "\n"]


    # color list
    set colorlist { 16 7 1 14 0 }

    # loop
    set line_count 0
    set line_count_used 0
    foreach line $data {
        # do some line processing here
        incr line_count

        # remove whitespace
        regsub -all -- {[[:space:]]+} $line " " line

        set line_items [split $line]
        # {} 14 5641 5940 ... note the leading space

        # set variables
        set chain [lindex $line_items 1]
        set index [lindex $line_items 2]
        set final_index [lindex $line_items 3]
        # puts "$chain $index $final_index"




        # if < 4, skip ..
        set len_line [llength $line_items]
        if { $len_line==4 } {

            puts "line_count_used $line_count_used"
            if { $line_count_used <= 5 } {
                incr line_count_used 5
                set colorindex [expr $line_count_used % 5]
                incr line_count_used -5
            } else {
                set colorindex [expr $line_count_used % 5]
            }
            incr line_count_used
            puts "ColorIndex: $colorindex"
            # return

            set diff [expr $final_index - $index]
            puts $diff

            set sel_color [lindex $colorlist $colorindex]
            puts $sel_color

            call_colorize_indices $id $index $final_index $sel_color
        }
    }
    # end foreach
}

proc colorize_pfball { {id 0} } {
    # Colorize the protofilament as large sphere/chain.


    # step 1. Make current representations invisible.
    set num_reps [make_current_reps_invisible $id]
    puts "number of invisible representations: $num_reps"


    # step 2. Get the number of chains.
    set sel [atomselect top all]
    set chains [lsort -ascii -unique [$sel get chain]]
    set num_chains [llength $chains]
    puts "the number of chains is: $num_chains"
    $sel delete


    # step 3. Get chains with certain number of atoms.
    # step 4. Get the center of mass of each chain.
    # step 5. Get the atom closest to the center of mass.
    for {set ch 0} {$ch < $num_chains} {incr ch} {
        set chain_name [lindex $chains $ch]
        set curchain [atomselect $id "chain $chain_name"]
        set num_atoms_chain [$curchain num]
        puts "chain: ($ch) $chain_name $num_atoms_chain"

        # step 4. COM
        set COM [center_of_mass $curchain]
        # puts $COM;


        # Loop through Atoms, find the one closest to the COM.
        set min_dist 1000.0
        set min_index -1
        foreach coord [$curchain get {x y z}] ind [$curchain get index] {
            # puts "the index-coord: $ind $coord"
            # puts $COM
            # puts $coord
            set dist [veclength [vecsub $COM $coord]]

            if {$dist < $min_dist} {
                set min_dist [expr $dist]
                set min_index $ind
                if {$min_dist < 4.0} {
                    break
                }
            }
        }
        puts "the closest atom:   $min_index   is at distance:  $min_dist"

        # Selection & Material
        mol material Opaque
        mol selection index $min_index

        # 3: orange (alpha)
        # 10: cyan (beta)
        # NOTE: elseif must be on the same line as brackets
        if {$num_atoms_chain == 420 || $num_atoms_chain == 427} {
            # puts "alpha-tubulin"
            mol color ColorID 3
            mol representation Beads 28.0 12.0
            mol addrep $id
        } elseif {$num_atoms_chain == 419} {
            # puts "beta-tubulin"
            mol color ColorID 10
            mol representation Beads 28.0 12.0
            mol addrep $id
        } elseif {$num_atoms_chain == 300} {
            # puts "kinesin"
            mol color ColorID 1
            mol representation Beads 26.0 12.0
            mol addrep $id
        }
    }
}
