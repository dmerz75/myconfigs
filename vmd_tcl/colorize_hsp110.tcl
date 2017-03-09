# work in progress
proc colorize_test { rep {diff 0} {run_type gsop}} {
    # colorize the SBD of Hsp70 in the tube,cpk, or (new)cartoon representations
    # rep: tube cpk new (default)

    # residue segments
    # colors: alpha helices: 0,10-blue,cyan; important linkers: 1-red; minor linkers 13-pinklavendar; beta-sheet 3,17-orange,yellow;
    # alternatively replace 383 with 397
    # set lst_resids {{383 412} {413 419} {420 427} {428 434} {435 443} {444 450} {451 460} {461 470} {471 501} {502 508} {509 557} {558 579} {580 603}}

    # hsp110
    set lst_resids {{50 56} {60 62}}
    set lst_colors {0 10}

    # sbd
    # set lst_resids {{383 412} {413 419} {420 427} {428 434} {435 443} {444 450} {451 460} {461 470} {471 501} {502 508} {509 522} {523 556} {557 579} {580 595} {596 603}}
    # set lst_colors {18 13 17 13 12 13 12 13 3 1 0 10 0 10 0}


    colorize_with_list $rep $lst_resids $lst_colors $diff $run_type
}

# # nbd
# #                   IA     IB        IA        L         IIA       IIB       IIA
# set lst_resids {{1 39} {40 111} {112 170} {171 186} {187 228} {229 309} {310 383}}
# set lst_colors {7 10 7 1 3 11 3}
# colorize_with_list $rep $lst_resids $lst_colors $diff $run_type

# # sbd
# set lst_resids {{383 412} {413 419} {420 427} {428 434} {435 443} {444 450} {451 460} {461 470} {471 501} {502 508} {509 522} {523 556} {557 579} {580 595} {596 603}}
# set lst_colors {18 13 17 13 12 13 12 13 3 1 0 10 0 10 0}
# colorize_with_list $rep $lst_resids $lst_colors $diff $run_type



proc colorize_hsp70 { rep {diff 0} {run_type gsop}} {
    # colorize the SBD of Hsp70 in the tube,cpk, or (new)cartoon representations
    # rep: tube cpk new (default)

    # residue segments
    # colors: alpha helices: 0,10-blue,cyan; important linkers: 1-red; minor linkers 13-pinklavendar; beta-sheet 3,17-orange,yellow;
    # alternatively replace 383 with 397
    # set lst_resids {{383 412} {413 419} {420 427} {428 434} {435 443} {444 450} {451 460} {461 470} {471 501} {502 508} {509 557} {558 579} {580 603}}

    # hsp110
    # set lst_resids {{50 56} {60 62}}
    # set lst_colors {0 10}


    # hsp70
    # nbd
    #                   IA     IB        IA        L         IIA       IIB       IIA
    set lst_resids {{1 39} {40 111} {112 170} {171 186} {187 228} {229 309} {310 383} {384 412} {413 419} {420 427} {428 434} {435 443} {444 450} {451 460} {461 470} {471 501} {502 508} {509 522} {523 556} {557 579} {580 595} {596 603}}
    set lst_colors {7 10 7 1 3 11 3 18 13 17 13 12 13 12 13 3 1 0 10 0 10 0}
    colorize_with_list $rep $lst_resids $lst_colors $diff $run_type
}
