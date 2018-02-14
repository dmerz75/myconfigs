# nbd description:
# IIA Orange!
#   189 - 228 3/4 beta sheet --> linker (187)
#   307 - 383 3 helices
#     1 helix: (pulled first) - 383 - 368
#     2 helix: (second) - 347 - 358
#     3 helix: (beta-sheet protected) - 312 - 328

# sbd description:
# when viewed with the alpha-helices on the right

# BETA: 397 to 507 - beta sheets
# 18   397 - 412 - [beta 1,2] beta_2_short (with turn)       ||
# 13   413 - 419 - linker beta_2_short-beta_4-1
# 17   420 - 427 - [beta 3] beta_4-1                         |
# 13   428 - 434 - linker from beta_4-1 into 2 long
# 12   435 - 443 - [beta 4]
# 13   444 - 450 - linker
# # #   435 - 460 - [beta 4,5] beta_2_long                   ||
# 12   451 - 460 - [beta 5]
# 13   461 - 470 - linker 2_long to 4-234
# 3    471 - 501 - [beta 6,7,8] beta_4-234                   |||

# Interdomain Linker
# 1   502 - 508

# ALPHA: 509 to 603 - 3 alpha helices
# previously
#   509 - 557 - long helix
#   558 - 579 - short / middle helix
#   580 - 594 - 603 - mid-length final helix with bend(594)
# currently
# 0    509 - 522 - A
# 10   523 - 556 - B
# 0    557 - 579 - C
# 10   580 - 595 - D
# 0    596 - 603 - E
#
# demarcations
# 15 (397)
# 79 / 461
# 109 / 491 beta strand prior to linker
# 128 (|A->) (510)
# 141 (|B->) (523)


# See colorize_sbd_newcartoon for more recent example.

proc colorize_sbd { {id 0} {rep Tube} } {
    # colorize the SBD of Hsp70 in the tube

    # residue segments
    # red: 1 29 30
    # green: 7 19 20
    # gray: 2
    # mauve/pink: 13

    # alternatively replace 383 with 397
    # set lst_colors {13          18        13        17        13        12       13         12        13     3(orange)    1         0        10         0         10        0}
    # set lst_colors {13          18        13        17        13        12       13         12        13     3(orange)    1         0        10         0         10        0}
    set lst_resids {{383 396} {397 412} {413 419} {420 427} {428 432} {433 443} {444 450} {451 460} \
                        {461 470} {471 479} {480 491} {492 500} {501 509} {510 522} {523 556} {557 579} {580 595} {596 603}}
    set lst_colors {    13        19        13        20        13        19        13        19    \
                            13       20        20        20         2         30       29         30        29        30}
    # set lst_colors {  13        18        13        17        13        12        13        12        13        3         1         0         10        0         10         0}
    set len_resids [llength $lst_resids]
    mol showrep $id 0 off

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
        set newrep1 [expr $molreps]
        set newrep2 [expr $molreps + 1]
        # puts "molreps: $molreps"


        # color, selection, material
        set color_num [lindex $lst_colors $index]
        # puts $color_num
        mol color ColorID $color_num
        mol selection resid $resid1 to $resid2
        mol material Opaque

        mol representation Tube 0.3 100.0
        mol modstyle $i $id Tube 0.3 100.0
        # mol addrep $id

        # Info) mol color ColorID 2
        # Info) mol representation Tube 0.500000 100.000000
        # Info) mol selection resid 491 to 500
        # Info) mol material Opaque
        # Info) mol addrep 1

        if { $color_num == 13 } {
            mol representation Tube 0.3 100.0
            mol modstyle $i $id Tube 0.3 100.0
            mol addrep $id
        } else {
            mol representation Tube 0.7 100.0
            mol modstyle $i $id Tube 0.7 100.0
            mol addrep $id
        }

        # if {$color_num == 13} {
        #     # mol representation $rep 4.7 0.5 10.0 8.0
        # }
        # if { $resid1 == 510} {
        #     mol representation Bead 1.2 12.0
        #     mol modstyle $newrep1 $id Beads 1.2 12.0
        #     mol addrep $id
        # }
        # if { $resid1 == 471} {
        #     mol representation Bead 1.2 12.0
        #     mol modstyle $newrep1 $id Beads 1.2 12.0
        #     mol addrep $id
        # }
        # if { $resid1 == 480} {
        #     mol representation Bead 1.2 12.0
        #     mol modstyle $newrep1 $id Beads 1.2 12.0
        #     mol addrep $id
        # }
        if { $resid1 == 492} {
            mol representation Beads 1.2 12.0
            mol modstyle $newrep1 $id Beads 1.2 12.0
            mol addrep $id
        }

        # specific beads:
        # if { $resid2 == 460} {
        #     mol selection resid $resid2
        #     mol representation Bead 2.0 12.0
        #     mol modstyle $newrep2 $id Beads 1.2 12.0
        #     mol addrep $id
        # }
        # if { $resid2 == 500} {
        #     mol selection resid $resid2
        #     mol representation Bead 2.0 12.0
        #     mol modstyle $newrep2 $id Beads 1.2 12.0
        #     mol addrep $id
        # }
        # if { $resid2 == 509} {
        #     mol selection resid $resid2
        #     mol representation Bead 2.0 12.0
        #     mol modstyle $newrep2 $id Beads 1.2 12.0
        #     mol addrep $id
        # }
        # if { $resid2 == 522} {
        #     mol selection resid $resid2
        #     mol representation Bead 2.0 12.0
        #     mol modstyle $newrep2 $id Beads 1.2 12.0
        #     mol addrep $id
        # }
    }

    # colorize_sbd_hsa $id
    # colorize_beaded_sbd $id # Big Beads!
};  #

proc colorize_sbd_newcartoon { {id 0} {rep NewCartoon} } {
    # colorize the SBD of Hsp70 in the tube

    # residue segments
    # red: 1 29 30
    # green: 7 19 20
    # gray: 2
    # mauve/pink: 13

    # alternatively replace 383 with 397
    # set lst_colors {13          18        13        17        13        12       13         12        13     3(orange)    1         0        10         0         10        0}
    # set lst_colors {13          18        13        17        13        12       13         12        13     3(orange)    1         0        10         0         10        0}
    set lst_resids {{383 396} {397 412} {413 419} {420 427} {428 432} {433 443} {444 450} {451 460} \
                        {461 470} {471 479} {480 491} {492 500} {501 509} {510 522} {523 556} {557 579} {580 595} {596 603}}
    set lst_colors {    13        19        13        20        13        19        13        19    \
                            13       20        20        20         2         30       29         30        29        30}
    # set lst_colors {  13        18        13        17        13        12        13        12        13        3         1         0         10        0         10         0}
    set len_resids [llength $lst_resids]
    mol showrep $id 0 off


    for {set i 1} {$i <= $len_resids} {incr i} {

        # information
        # puts "loop: $i"
        set index [expr $i - 1]
        set resid1 [expr [lindex $lst_resids $index 0]]
        set resid2 [expr [lindex $lst_resids $index 1]]
        # puts "indices $index $i"
        puts "resids: $resid1 $resid2"

        # molinfo
        set molreps [molinfo $id get numreps]
        set newrep1 [expr $molreps]
        set newrep2 [expr $molreps + 1]
        # puts "molreps: $molreps"
        # color, selection, material
        set color_num [lindex $lst_colors $index]
        # puts $color_num


        # base tube color.
        # if { $i == 1 } {
        mol color ColorID 13
        mol selection resid $resid1 to $resid2
        mol material Opaque
        mol representation $rep 0.28 100.0
        mol addrep $id
        # } else {
        # base tube color.
        mol color ColorID $color_num
        mol selection resid $resid1 to $resid2
        mol material Opaque
        # }

        if { $color_num == 13 } {
            mol representation Tube 0.3 100.0
            # mol modstyle $i $id Tube 0.3 100.0
            mol addrep $id
        } else {
            mol representation NewCartoon 0.35 10.0 4.1
            # mol modstyle $i $id $rep 0.7 100.0
            mol addrep $id
        }
    }

};  #


proc colorize_beaded_sbd { {id 0} } {

    set lst_resids { 460 491 500 509 522 }
    set lst_colors {  19 20   20  2   30 }


    # set newrep1 [expr $molreps]
    # mauve: 13, 5-tan, 2-gray, 3-orange, 11-purple, red-1

    set len_resids [llength $lst_resids]

    for {set i 1} {$i <= $len_resids} {incr i} {
        set my_numreps [molinfo $id get numreps]
        puts "the total reps are: $my_numreps"

        # information
        # puts "loop: $i"
        set index [expr $i - 1]
        set resid1 [lindex $lst_resids $index]
        # set resid2 [expr [lindex $lst_resids $index 1]]
        # puts "index: $index    i: $i"
        # puts "numbers $resid1 $resid2"

        set color_num [lindex $lst_colors $index]
        puts "color selected: $color_num"

        mol color ColorID $color_num
        # mol representation $rep 4.7 0.6 10.0 8.0
        mol representation Beads 2.0 12.0
        mol modstyle $my_numreps $id Beads 1.2 12.0
        mol selection resid $resid1
        mol material Opaque
        mol addrep $id
    }
}

proc colorize_sbd_hsa { {id 0} {rep CPK}} {
    # colorize the SBD of Hsp70 in the tube,cpk, or (new)cartoon representations

    # residue segments
    # set lst_resids {{397 427} {428 434} {435 460} {461 470} {471 490} {491 500} {501 509}}
    # set lst_colors {5 1 11 1 3 2 1}

    set lst_resids {{492 500} }
    set lst_colors {2}

    # mauve: 13, 5-tan, 2-gray, 3-orange, 11-purple, red-1

    set len_resids [llength $lst_resids]

    for {set i 1} {$i <= $len_resids} {incr i} {
        set my_numreps [molinfo $id get numreps]
        puts "the total reps are: $my_numreps"

        # information
        # puts "loop: $i"
        set index [expr $i - 1]
        set resid1 [expr [lindex $lst_resids $index 0]]
        set resid2 [expr [lindex $lst_resids $index 1]]
        puts "index: $index    i: $i"
        puts "numbers $resid1 $resid2"

        set color_num [lindex $lst_colors $index]
        puts "color selected: $color_num"

        mol color ColorID $color_num
        mol representation $rep 4.7 0.6 10.0 8.0
        mol selection resid $resid1 to $resid2
        mol material Opaque
        mol addrep $id
    }
}

proc colorize_peptide { {id 0} {rep Tube} } {
    # colorize the SBD of Hsp70 in the tube,cpk, or (new)cartoon representations

    # residue segments
    set lst_resids {{1 7}}
    set lst_colors {16}
    set len_resids [llength $lst_resids]

    for {set i 1} {$i <= $len_resids} {incr i} {
        set my_numreps [molinfo $id get numreps]
        puts "the total reps are: $my_numreps"

        # information
        # puts "loop: $i"
        set index [expr $i - 1]
        set resid1 [expr [lindex $lst_resids $index 0]]
        set resid2 [expr [lindex $lst_resids $index 1]]
        set color_num [lindex $lst_colors $index]

        puts "index: $index    i: $i"
        puts "numbers $resid1 $resid2"
        puts "color selected: $color_num"

        mol color ColorID $color_num
        mol representation $rep 1.0 100.0
        mol selection resid $resid1 to $resid2
        mol material Opaque
        mol addrep $id
    }
}

proc colorize_sbd_old_2 { {id 0} {rep Tube} } {
    # colorize the SBD of Hsp70 in the tube

    # residue segments
    # alternatively replace 383 with 397
    # set lst_resids {{383 412} {413 419} {420 427} {428 434} {435 443} {444 450} {451 460} {461 470} {471 501} {502 508} {509 557} {558 579} {580 603}}
    # set lst_resids {{383 396} {397 412} {413 419} {420 427} {428 432} {433 443} {444 450} {451 460} {461 470} {471 501} {502 508} {509 522} {523 556} {557 579} {580 595} {596 603}}
    set lst_resids {{383 396} {397 412} {413 419} {420 427} {428 432} {433 443} {444 450} {451 460} {461 470} {471 500} {501 509} {510 522} {523 556} {557 579} {580 595} {596 603}}
    # set lst_colors {13          18        13        17        13        12       13         12        13     3(orange)    1         0        10         0         10        0}
    set lst_colors {13 18 13 17 13 12 13 12 13 3 1 0 10 0 10 0}
    set len_resids [llength $lst_resids]


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

proc colorize_sbd_old_1 { {id 0} {rep Tube} {diff 0} {run_type gsop}} {
    # colorize the SBD of Hsp70 in the tube,cpk, or (new)cartoon representations
    # color Display Background white

    # puts "hello"
    # puts "the value of $diff"
    # return

    # residue segments
    # alternatively replace 383 with 397
    # set lst_resids {{383 412} {413 419} {420 427} {428 434} {435 443} {444 450} {451 460} {461 470} {471 501} {502 508} {509 557} {558 579} {580 603}}
    # set lst_resids {{383 396} {397 412} {413 419} {420 427} {428 432} {433 443} {444 450} {451 460} {461 470} {471 501} {502 508} {509 522} {523 556} {557 579} {580 595} {596 603}}
    set lst_resids {{383 396} {397 412} {413 419} {420 427} {428 432} {433 443} {444 450} {451 460} {461 470} {471 500} {501 509} {510 522} {523 556} {557 579} {580 595} {596 603}}
    set lst_colors {13 18 13 17 13 12 13 12 13 3 1 0 10 0 10 0}
    set len_resids [llength $lst_resids]


    for {set i 1} {$i <= $len_resids} {incr i} {

        # information
        # puts "loop: $i"
        set index [expr $i - 1]
        set resid1 [expr [lindex $lst_resids $index 0] - $diff]
        set resid2 [expr [lindex $lst_resids $index 1] - $diff]
        # puts "indices $index $i"
        # puts "numbers $resid1 $resid2"


        # type & color
        # set str_tube {mol modstyle $i 0 Tube 1.0 100.0}
        # set str_cpk {mol modstyle $i 0 CPK 3.000000 0.600000 10.00000 8.00000}
        # set str_new {mol modstyle $i 0 NewCartoon 0.28 26 4}

        set str_tube1 {mol modstyle $i $id Tube 0.9 100.0}
        set str_tube2 {mol modstyle $i $id Tube 0.5 100.0}
        set str_cpk {mol modstyle $i $id CPK 3.000000 0.600000 10.00000 8.00000}
        set str_new {mol modstyle $i $id NewCartoon 0.28 26 4}


        # #   397 - 412 - beta_2_short (with turn)          ||
        mol addrep $id
        mol selection all
        mol material Opaque
        mol modselect $i $id resid $resid1 to $resid2




        if {$run_type == "gsop"} {
            # puts "the value of run_type is $run_type, = gsop!"
            mol modselect $i $id resid $resid1 to $resid2
        } else {
            # puts "the value of run_type is $run_type, not gsop!"
            mol modselect $i $id protein and resid $resid1 to $resid2
        }


        mol modcolor $i $id ColorID [lindex $lst_colors $index]
        # # mol modstyle 1 0 CPK 3.000000 0.600000 10.00000 8.00000
        # # switch $rep tube {$str_tube} cpk {$str_cpk} new {$str_new} default {$str_tube}
        switch $rep tube {set sel $str_tube} cpk {set sel $str_cpk} new {set sel $str_new} default {set sel $str_tube}
        eval $sel

        mol color ColorID $color_num
        mol representation $rep 4.7 0.6 10.0 8.0
        mol selection resid $resid1 to $resid2
        mol material Opaque
        mol addrep $id

    }

    colorize_sbd_hsa $id
    # return

    # # working example!!
    # # #   397 - 412 - beta_2_short (with turn)          ||
    # mol addrep 0
    # mol selection all
    # mol material Opaque
    # mol modselect 1 0 protein and resid 397 to 412
    # mol modcolor 1 0 ColorID 0
    # # mol modstyle 1 0 CPK 3.000000 0.600000 10.00000 8.00000
    # # switch $rep tube {$str_tube} cpk {$str_cpk} new {$str_new} default {$str_tube}
    # switch $rep tube {set sel $str_tube} cpk {set sel $str_cpk} new {set sel $str_new} default {set sel $str_tube}
    # eval $sel
}

proc colorize_sbd_domains_CPK {} {
    color Display Background white

    #   397 - 412 - beta_2_short (with turn)          ||
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 1 0 protein and resid 397 to 412
    mol modcolor 1 0 ColorID 0
    mol modstyle 1 0 CPK 3.000000 0.600000 10.00000 8.00000

    #   413 - 419 - linker beta_2_short-beta_4-1
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 2 0 protein and resid 413 to 419
    mol modcolor 2 0 ColorID 1
    mol modstyle 2 0 CPK 3.000000 0.600000 10.00000 8.00000

    #   420 - 427 - beta_4-1                          |
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 3 0 protein and resid 420 to 427
    mol modcolor 3 0 ColorID 2
    mol modstyle 3 0 CPK 3.000000 0.600000 10.00000 8.00000

    #   428 - 434 - linker from beta_4-1 into 2 long
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 4 0 protein and resid 428 to 434
    mol modcolor 4 0 ColorID 3
    mol modstyle 4 0 CPK 3.000000 0.600000 10.00000 8.00000

    #   435 - 460 - beta_2_long                       ||
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 5 0 protein and resid 435 to 460
    mol modcolor 5 0 ColorID 4
    mol modstyle 5 0 CPK 3.000000 0.600000 10.00000 8.00000

    #   461 - 470 - linker 2_long to 4-234
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 6 0 protein and resid 461 to 470
    mol modcolor 6 0 ColorID 5
    mol modstyle 6 0 CPK 3.000000 0.600000 10.00000 8.00000

    #   471 - 501 - beta_4-234                        |||
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 7 0 protein and resid 471 to 501
    mol modcolor 7 0 ColorID 6
    mol modstyle 7 0 CPK 3.000000 0.600000 10.00000 8.00000

    # Interdomain Linker
    #   502 - 508
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 8 0 protein and resid 502 to 508
    mol modcolor 8 0 ColorID 7
    mol modstyle 8 0 CPK 3.000000 0.600000 10.00000 8.00000

    #   508 - 556 - long helix
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 9 0 protein and resid 509 to 557
    mol modcolor 9 0 ColorID 9
    mol modstyle 9 0 CPK 3.000000 0.600000 10.00000 8.00000

    #   558 - 579 - short / middle helix
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 10 0 protein and resid 558 to 579
    mol modcolor 10 0 ColorID 10
    mol modstyle 10 0 CPK 3.000000 0.600000 10.00000 8.00000

    #   580 - 594 - 603 - mid-length final helix with bend(594)
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 11 0 protein and resid 580 to 603
    mol modcolor 11 0 ColorID 11
    mol modstyle 11 0 CPK 3.000000 0.600000 10.00000 8.00000


    # #   397 - 412 - beta_2_short (with turn)          ||
    # #   413 - 419 - linker beta_2_short-beta_4-1
    # #   420 - 427 - beta_4-1                          |
    # #   428 - 434 - linker from beta_4-1 into 2 long
    # #   435 - 460 - beta_2_long                       ||
    # #   461 - 470 - linker 2_long to 4-234
    # #   471 - 501 - beta_4-234                        |||

    # # Interdomain Linker
    # #   502 - 508

    # # ALPHA: 509 to 603 - 3 alpha helices
    # #   508 - 556 - long helix
    # #   558 - 578 - short / middle helix
    # #   580 - 594 - 603 - mid-length final helix with bend(594)
    # mol addrep 0
    # mol selection all
    # mol material Opaque
    # mol modselect 1 0 resid 397 to 412
    # mol modcolor 1 0 ColorID 7
    # mol modstyle 1 0 CPK 3.000000 0.600000 10.00000 8.00000
}


proc colorize_tube { {id 0} resid1 resid2 {color 0} } {
    # colorize the SBD of Hsp70 in the tube

    # residue segments
    # red: 1 29 30
    # green: 7 19 20
    # gray: 2
    # mauve/pink: 13

    # molinfo
    # set molreps [molinfo $id get numreps]
    # set newrep1 [expr $molreps]

    set molreps [molinfo $id get numreps]
    set newrep [expr $molreps + 1]
    # puts "molreps: $molreps"
    # puts "residues: $resid1 $resid2"

    # mol color ColorID 20
    # mol representation Tube 0.600000 50.000000
    # mol selection resid 449 to 457
    # mol material Opaque
    # mol addrep 1

    # puts $color_num
    mol color ColorID $color
    mol representation Tube 0.6 50.0
    mol selection resid $resid1 to $resid2
    # mol modstyle $newrep $id Tube 0.6 100.0
    mol material Opaque
    mol addrep $id
};  #


proc colorize_hsp70_newcartoon { {id 0} } {

    colorize_nbd_domains_NewCartoon $id
    colorize_sbd_newcartoon $id
    colorize_tube $id 598 663 0
}

proc colorize_hsp70_tube { {id 0} } {

    # list of resids, colors
    set lst_nbd {}
    set lst_sbd {}
    set lst_nbdc {}
    set lst_sbdc {}

    # residues:
    set lst_nbd {
        {0 39} {112 170} {40 111} {187 228} \
            {310 385} {229 309} {170 186} \
        }
    set lst_beta {
        {382 391} {392 411} {412 415} \
            {416 424} {425 429} \
            {430 438} {439 448} \
            {449 457} {458 466} \
            {467 500} {501 505} }
    set lst_alpha {
        {506 518} {519 552} {553 575} {576 591} \
            {592 598} {599 663}
    }

    # colors:
    set lst_nbdc { 7 7 10 3 3 11 1}
    # set lst_betac { 13 20 13 19 13 \
    #                     20 13 20 13 \
    #                     19 2}
    set lst_betac { 13 19 13 20 13 \
                        19 13 19 13 \
                        20 2}
    set lst_alphac {30 29 30 29 30 0}

    # concat:residues
    set lst_sbd [concat $lst_beta $lst_alpha]
    set len_nbd [llength $lst_nbd]
    # concat:colors
    set lst_sbdc [concat $lst_betac $lst_alphac]
    set len_sbd [llength $lst_sbd]

    puts "NBD: $len_nbd   SBD: $len_sbd"

    # concat:total combination.
    set lst_resids [concat $lst_nbd $lst_sbd]
    set lst_colors [concat $lst_nbdc $lst_sbdc]

    set len_resids [llength $lst_resids]
    set len_colors [llength $lst_colors]

    puts "lengths: $len_resids $len_colors"
    # return

    if {$len_resids != $len_colors} {
        return
    }


    for {set i 1} {$i <= $len_resids} {incr i} {
        set index [expr $i - 1]
        set resid1 [expr [lindex $lst_resids $index 0]]
        set resid2 [expr [lindex $lst_resids $index 1]]
        set color_num [lindex $lst_colors $index]
        puts "colorize(i): index res1 res2 color): ($i)  $index  $resid1 $resid2  $color_num"
        colorize_tube $id $resid1 $resid2 $color_num
    }
}
