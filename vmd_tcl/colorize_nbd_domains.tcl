# nbd description:
# IIA Orange!
#   189 - 228 3/4 beta sheet --> linker (187)
#   307 - 383 3 helices
#     1 helix: (pulled first) - 383 - 368
#     2 helix: (second) - 347 - 358
#     3 helix: (beta-sheet protected) - 312 - 328

# % VMD - introspective___________________!
# N-Term overall:
# N-Term IA desc: B3-(B-A-B-A-B)
# N-Term - IA - 1
# 1 - 39: (4) beta
# flaherty: 1-39

# N-Term IB desc: B2-A-B-A2-B2
# N-Term - IB - 1
# 40 - 50: (2) beta
# 51 - 60: helix
# 61 - 66: beta
# 67 - 87: (2) helix
# 88 - 111: beta sheet 2-pleat
# flaherty: 40 - 115

# N-Term - IA - 2
# 112 - 131: helix
# 132 - 145: beta sheet 1-pleat
# 146 - 160: helix
# 161 - 169: beta sheet 1-pleat
# flaherty: 116-188

# Linker overall: 170 - 186

# C-Term overall:
# C-Term IIA desc: B3-A-B-A(2,3)
# C-Term - IIA - 1
# 187 - 228: (3/4) beta sheet 3-pleats
# flaherty: 189-228

# C-Term IIB desc: A2-B-A
# C-Term - IIB - 1
# 229 - 250: (1/3) helix
# 256 - 275: (2/3) helix
# 276 - 301: beta 2-pleats
# 302 - 309: (3/3) helix small
# flaherty: 229-306

# C-Term - IIA - 2
# 310 - 331: (1/3) helix (310,328)
# 332 - 346: (4/4) beta sheet
# 347 - 358: helix (15?)
# 359 - 367: ---
# 368 - 385: last helix (16)
# --368 - 383
# flaherty: 307-end
# ________________________________________!


proc colorize_nbd_binding { {id 0} } {

    mol color ColorID 13
    mol representation CPK 5.200000 0.600000 10.000000 8.000000
    mol selection resid 186 to 195
    mol material Opaque
    mol addrep $id

    mol color ColorID 15
    mol representation CPK 5.200000 0.600000 10.000000 8.000000
    mol selection resid 196 to 207
    mol material Opaque
    mol addrep $id

    mol color ColorID 12
    mol representation CPK 5.200000 0.600000 10.000000 8.000000
    mol selection resid 330 to 345
    mol material Opaque
    mol addrep $id
}


proc colorize_nbd_domains_CPK {} {
    color Display Background white

    # IA Green 7
    mol addrep 0
    mol selection all
    mol material Opaque
    # original
    # mol modselect 1 0 resid 1 to 39 116 to 188
    mol modselect 1 0 resid 1 to 39 116 to 170
    mol modcolor 1 0 ColorID 7
    mol modstyle 1 0 CPK 3.000000 0.600000 10.00000 8.00000


    # IB Cyan-10
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 2 0 resid 40 to 115
    mol modcolor 2 0 ColorID 10
    mol modstyle 2 0 CPK 3.000000 0.600000 10.00000 8.00000


    # IIA Orange-3
    mol addrep 0
    mol selection all
    mol material Opaque
    # original
    # mol modselect 3 0 resid 189 to 228 307 to 383
    mol modselect 3 0 resid 187 to 228 307 to 382
    mol modcolor 3 0 ColorID 3
    mol modstyle 3 0 CPK 3.000000 0.600000 10.00000 8.00000


    # IIB Magenta-11(purple)
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 4 0 resid 229 to 306
    mol modcolor 4 0 ColorID 11
    mol modstyle 4 0 CPK 3.300000 0.600000 10.00000 8.00000


    # Red Linker
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 5 0 resid 171 to 186
    mol modcolor 5 0 ColorID 1
    mol modstyle 5 0 CPK 3.000000 0.600000 10.00000 8.00000


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
proc colorize_nbd_domains_tube {} {
    color Display Background white

    # IA Green 7
    mol addrep 0
    mol selection all
    mol material Opaque
    # original
    # mol modselect 1 0 resid 1 to 39 116 to 188
    mol modselect 1 0 resid 1 to 39 116 to 170
    mol modcolor 1 0 ColorID 7
    mol modstyle 1 0 Tube 1.0 100.0


    # IB Cyan-10
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 2 0 resid 40 to 115
    mol modcolor 2 0 ColorID 10
    mol modstyle 2 0 Tube 1.0 100.0


    # IIA Orange-3
    mol addrep 0
    mol selection all
    mol material Opaque
    # original
    # mol modselect 3 0 resid 189 to 228 307 to 383
    mol modselect 3 0 resid 187 to 228 307 to 382
    mol modcolor 3 0 ColorID 3
    mol modstyle 3 0 Tube 1.0 100.0


    # IIB Magenta-11(purple)
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 4 0 resid 229 to 306
    mol modcolor 4 0 ColorID 11
    mol modstyle 4 0 Tube 1.0 100.0


    # Red Linker
    mol addrep 0
    mol selection all
    mol material Opaque
    mol modselect 5 0 resid 171 to 186
    mol modcolor 5 0 ColorID 1
    mol modstyle 5 0 Tube 1.0 100.0

}
proc colorize_nbd_domains_NewCartoon { {id 0 } } {
    color Display Background white

    mol addrep $id

    mol selection all
    mol material Opaque
    # original
    # mol modselect 1 $id resid 1 to 39 116 to 188
    mol modselect 1 $id resid 1 to 39 112 to 170
    mol modcolor 1 $id ColorID 7
    mol modstyle 1 $id NewCartoon 0.28 26 4
    # IA Green 7
    mol addrep $id

    mol selection all
    mol material Opaque
    # original
    # mol modselect 2 $id resid 40 to 115
    mol modselect 2 $id resid 40 to 111
    mol modcolor 2 $id ColorID 10
    mol modstyle 2 $id NewCartoon 0.28 26 4
    # IB Cyan-10
    mol addrep $id

    mol selection all
    mol material Opaque
    # original
    # mol modselect 3 $id resid 189 to 228 307 to 383
    mol modselect 3 $id resid 187 to 228 310 to 383
    mol modcolor 3 $id ColorID 3
    mol modstyle 3 $id NewCartoon 0.28 26 4
    # IIA Orange-3
    mol addrep $id

    mol selection all
    mol material Opaque
    mol modselect 4 $id resid 229 to 309
    mol modcolor 4 $id ColorID 11
    mol modstyle 4 $id NewCartoon 0.28 26 4
    # IIB Magenta-11(purple)
    mol addrep $id

    mol selection all
    mol material Opaque
    mol modselect 5 $id "protein and resid 170 to 186"
    mol modcolor 5 $id ColorID 1
    mol modstyle 5 $id Cartoon 2.000000 26.0000 5.0000
    # Red Linker
    mol addrep $id
}
proc add_endpoint { residue_num ball_color } {
    # add VDW balls of color gray:first and blue:last
    # mol delete all - deletes everything

    # mol addrep 0
    mol selection resid $residue_num and name CA
    mol representation VDW 2.000 14.000
    mol color ColorID $ball_color
    # Gray
    mol material Opaque
    mol addrep 0

    # # mol addrep 0
    # mol selection resid $last and name CA
    # mol representation VDW 1.3000 12.0000
    # mol color ColorID 0
    # # Blue
    # mol material Opaque
    # mol addrep 0
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

#     # puts $coords1
#     # puts $coords2

#     # set coordinates1 [lindex $coords1]
#     # set coordinates2 [lindex $coords2]

#     # set vec [vecsub $coords1 $coords2]
#     # compute connection vector, length
#     # else: use lindex (since coords are a list), # foreach

#     # puts $coordinates1
#     # puts $coordinates2

#     #-----------
#     # set xyz {}
#     # foreach i $coords2 j $coords1 {
#     #     set xdist [vecsub $i $j]
#     #     lappend xyz $xdist
#     # }
#     # set distance12 [veclength [lindex $xyz]]
#     # puts $xyz
#     #-----------

#     # set vector12 [vecsub [lindex $coordinates2] [lindex $coordinates1]]

#     set pos_begin [measure center $ca1]
#     set pos_end   [measure center $ca2]

#     # get the protein vector; $end - $begin for vecsub
#     set vector12 [vecsub $pos_end $pos_begin]
#     set distance12 [veclength $vector12]

#     puts $vector12
#     puts $distance12
# }
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

# colorize_nbd_domains_CPK
# colorize_nbd_domains_NewCartoon
