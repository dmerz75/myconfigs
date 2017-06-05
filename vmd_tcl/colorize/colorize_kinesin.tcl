# kinesin:

# proc colorize_kinesin { {id 0} {set selection [atomselect $id "all"]} }
proc colorize_3j8y { {id 0} {selection "all"} } {
    puts "for 3j8y"
    puts "proc <molid> <selection>"
    puts "selection: $selection"

    # step 2. Get the number of chains.
    set sel [atomselect $id $selection]
    set chains [lsort -ascii -unique [$sel get chain]]
    set num_chains [llength $chains]
    puts "the number of chains is: $num_chains"
    # $sel delete


    for {set ch 0} {$ch < $num_chains} {incr ch} {

        set chain_name [lindex $chains $ch]
        set chain_sel [atomselect $id "chain $chain_name"]
        set chain_num [$chain_sel num]

        # puts $chain_sel
        puts "chain $ch $chain_name number of atoms: $chain_num"
    }
}

proc colorize_kinesin_and_finger { {id 0} {selection "all"}} {
    puts "colorize_kinesin"

    # get resid:  5 - 502 _ 3j8y
    # get resid: 42 - 634 _ MCAK 1v8j
    # by merely my self-inspection, I find the finger to be:
    # resid 102 - 125

    # set num_reps [make_current_reps_invisible $id]
    # puts "number of invisible representations: $num_reps"
    set molreps [molinfo $id get numreps]


    mol material Opaque
    mol color ColorID 14
    mol representation NewCartoon 0.30 10.00 4.10 0
    mol selection "$selection"
    # mol modstyle $molreps $id NewCartoon 0.30 10.00 4.10 0
    mol addrep $id



    mol material Opaque
    mol color ColorID 13
    mol representation NewCartoon 0.33 10.00 4.10 0
    mol selection resid 102 to 125
    mol addrep $id

}
