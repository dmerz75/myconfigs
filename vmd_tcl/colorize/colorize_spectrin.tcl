proc colorize_Spectrin {} {
    color Display Background white

    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 1 0 resid 1 to 27
    mol modcolor 1 0 ColorID 1
    mol modstyle 1 0 Tube 1.0 10.0
    # N-term RED A (Paci_Karplus)

    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 2 0 resid 33 to 68
    mol modcolor 2 0 ColorID 0
    mol modstyle 2 0 Tube 1.0 10.0
    # Mid-term BLUE B

    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 3 0 resid 73 to 98
    mol modcolor 3 0 ColorID 7
    mol modstyle 3 0 Tube 1.0 10.0
    # C-term GREEN C

    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 4 0 resid 28 to 32 69 to 72
    mol modcolor 4 0 ColorID 2
    mol modstyle 4 0 Tube 1.0 10.0
    # C-term GREEN C
}

# proc add_endpoint { residue_num ball_color } {
#     # add VDW balls of color gray:first and blue:last
#     # mol delete all - deletes everything

#     # mol addrep 0
#     mol selection resid $residue_num and name CA
#     mol representation VDW 2.000 14.000
#     mol color ColorID $ball_color
#     # Gray
#     mol material Opaque
#     mol addrep 0
# }

# proc add_endpoints { first last } {
#     # add VDW balls of color gray:first and blue:last
#     # mol delete all - deletes everything

#     # mol addrep 0
#     mol selection resid $first and name CA
#     mol representation VDW 2.000 14.0000
#     mol color ColorID 2
#     # Gray
#     mol material Opaque
#     mol addrep 0

#     # mol addrep 0
#     mol selection resid $last and name CA
#     mol representation VDW 2.0000 14.0000
#     mol color ColorID 0
#     # Blue
#     mol material Opaque
#     mol addrep 0
# }
# proc draw_bond { first last } {
#     # provide resid

#     # get CA
#     set ca1 [atomselect top "resid $first and name CA"]
#     set ca2 [atomselect top "resid $last and name CA"]

#     # get atom index of CA
#     set atom1 [$ca1 get index]
#     set atom2 [$ca2 get index]

#     # draw bond line
#     # 0/1 0/3217
#     # label add Atoms 0/$first
#     # label add Atoms 0/$last
#     # label add Bonds 0/$first 0/$last
#     label add Atoms 0/$atom1
#     label add Atoms 0/$atom2
#     label add Bonds 0/$atom1 0/$atom2

#     # add label
#     label textsize 1.50
#     label textthickness 1.50
#     # label color black
#     # color Labels Bonds black
# }
# proc draw_dashed_line { resfirst reslast sel_color } {
#     # draw a black dashed line
#     # get CA
#     set ca1 [atomselect top "resid $resfirst and name CA"]
#     set ca2 [atomselect top "resid $reslast and name CA"]

#     # get atom index of CA
#     # set atom1 [$ca1 get index]
#     # set atom2 [$ca2 get index]

#     # get {x y z}
#     set coords1 [$ca1 get {x y z}]
#     set coords2 [$ca2 get {x y z}]

#     # get vectors
#     set pos_begin [measure center $ca1]
#     set pos_end   [measure center $ca2]

#     # subtract vectors; $end - $begin for vecsub
#     set vector12 [vecsub $pos_end $pos_begin]
#     set distance12 [veclength $vector12]

#     puts $vector12
#     puts $distance12

#     graphics 0 color $sel_color
#     # graphics 0 line $pos_begin $vector12 width 8 style dashed
#     graphics 0 line $pos_begin $pos_end width 8 style dashed
# }

# proc calc_distance { first last } {
#     # provide resid (CA will be selected)

#     # get CA
#     set ca1 [atomselect top "resid $first and name CA"]
#     set ca2 [atomselect top "resid $last and name CA"]

#     # get {x y z}
#     set coords1 [$ca1 get {x y z}]
#     set coords2 [$ca2 get {x y z}]

#     set pos_begin [measure center $ca1]
#     set pos_end   [measure center $ca2]

#     # get the protein vector; $end - $begin for vecsub
#     set vector12 [vecsub $pos_end $pos_begin]
#     set distance12 [veclength $vector12]

#     puts $vector12
#     puts $distance12
# }
