# vmd Struct_data/molecule.000001 -dispdev text -e force_frames_load.tcl

# VMD for LINUXAMD64, version 1.9.1 (February 1, 2012)
# Log file '/home/dale/completed/sopnucleo/adp-half_ehi_eli/adp-half-ehi-eli_runsopnuc__03-25-2014_1829__72_8439684/force_frames_load.vmd', created by user dale
menu files off
menu files on
mol addfile {/home/dale/completed/sopnucleo/adp-half_ehi_eli/adp-half-ehi-eli_runsopnuc__03-25-2014_1829__72_8439684/Coord/interims/1800.pdb} type {pdb} first 0 last -1 step 1 waitfor 1 0
animate style Loop
mol addfile {/home/dale/completed/sopnucleo/adp-half_ehi_eli/adp-half-ehi-eli_runsopnuc__03-25-2014_1829__72_8439684/Coord/interims/4100.pdb} type {pdb} first 0 last -1 step 1 waitfor 1 0
animate style Loop
mol addfile {/home/dale/completed/sopnucleo/adp-half_ehi_eli/adp-half-ehi-eli_runsopnuc__03-25-2014_1829__72_8439684/Coord/interims/11000.pdb} type {pdb} first 0 last -1 step 1 waitfor 1 0
animate style Loop
mol addfile {/home/dale/completed/sopnucleo/adp-half_ehi_eli/adp-half-ehi-eli_runsopnuc__03-25-2014_1829__72_8439684/Coord/interims/13800.pdb} type {pdb} first 0 last -1 step 1 waitfor 1 0
animate style Loop
mol addfile {/home/dale/completed/sopnucleo/adp-half_ehi_eli/adp-half-ehi-eli_runsopnuc__03-25-2014_1829__72_8439684/Coord/interims/15900.pdb} type {pdb} first 0 last -1 step 1 waitfor 1 0
animate style Loop
menu files off


# source from TKCON
proc orient_protein_on_z { molec start end } {
    # protein
    set all [atomselect $molec all]

    set resid_CA_begin_coord [atomselect $molec "resid $start and name CA"]
    set resid_CA_end_coord [atomselect $molec "resid $end and name CA"]


    set pos_begin [measure center $resid_CA_begin_coord]
    # set inv_pos_begin [vecinvert [measure center $resid_CA_begin_coord]]
    set pos_end   [measure center $resid_CA_end_coord]

    # get the protein vector; $end - $begin for vecsub
    set protein_vector [vecsub $pos_end $pos_begin]
    set prot_on_x [transvecinv $protein_vector]

    # translate from x0,y0,z0 to {0.1 -0.5 0.08}
    # set inv_protein_vector [vecinvert [vecsub $pos_end $pos_begin]]
    # set inv_protein_vector [vecadd $inv_protein_vector {0.1 -0.05 0.08}]

    # translate: (1) near origin (2) to x axis
    # (1)
    # $all moveby $inv_pos_begin
    # (2)
    $all move $prot_on_x
    $all move [trans y -90]
    set pos_begin [vecinvert [measure center $resid_CA_begin_coord]]
    $all moveby $pos_begin
    $all moveby {0.01 -0.05 0.08}


    # $all writepsf 00_start.psf
    # $all writepdb 00_start.pdb
    # set ptn_ca [atomselect $molec "segname PTN and name CA"]
    # $ptn_ca set beta 1
    # $all writepdb hold_ca.ref
    # # $ptn_ca writepdb hold_ca.ref
    # set ptn [atomselect $molec "segname PTN"]
    # $ptn set beta 1
    # $all writepdb hold.ref
    # # $ptn writepdb hold.ref

}

proc set_to_cpk {} {
    mol selection all
    mol representation CPK 1.300000 0.600000 10 8
    # mol color Name
    # mol addrep 0
    # mol delrep 0 0
}
proc colorize_domains {} {
    # mol delrep 2 0
    # mol showrep 0 0 0    

    mol addrep 0
    mol color ColorID 0
    mol representation CPK 1.300000 0.600000 10.000000 8.000000
    mol selection all
    mol material Opaque
    # domain
    mol modselect 1 0 resid 1 to 39 116 to 188
    mol modcolor 1 0 ColorID 7 
    # IA Green 7

    mol addrep 0
    mol color ColorID 0
    mol representation CPK 1.300000 0.600000 10.000000 8.000000
    mol selection all
    mol material Opaque
    # domain
    mol modselect 2 0 resid 40 to 115
    mol modcolor 2 0 ColorID 10
    # IB Cyan-10

    mol addrep 0
    mol color ColorID 0
    mol representation CPK 1.300000 0.600000 10.000000 8.000000
    mol selection all
    mol material Opaque
    # domain
    mol modselect 3 0 resid 189 to 228 307 to 383
    mol modcolor 3 0 ColorID 3
    # IIA Orange-3

    mol addrep 0
    mol color ColorID 0
    mol representation CPK 1.300000 0.600000 10.000000 8.000000
    mol selection all
    mol material Opaque
    # domain
    mol modselect 4 0 resid 229 to 306
    mol modcolor 4 0 ColorID 11
    # IIB Magenta-11(purple)
}

# START
set idn 0
# mol selection all
# mol representation CPK 1.300000 0.600000 10 8
# orient_protein_on_z $idn 4 385


# translate by 2.5 0.00 0.00
# scale by 6.8
# colorize_domains

# for {set i 0} {$i<6} {incr i} {
#     animate goto $i
#     orient_protein_on_z $idn 2 383
#     display reset_view
#     rotate y by 90
#     set_to_cpk
# }

animate goto 0
orient_protein_on_z $idn 2 383
display resetview
rotate y by 90
set_to_cpk

animate goto 1
orient_protein_on_z $idn 2 383
display resetview
rotate y by 90
set_to_cpk

animate goto 2
orient_protein_on_z $idn 2 383
display resetview
rotate y by 90
set_to_cpk

animate goto 3
orient_protein_on_z $idn 2 383
display resetview
rotate y by 90
set_to_cpk

animate goto 4
orient_protein_on_z $idn 2 383
display resetview
rotate y by 90
set_to_cpk

animate goto 5
orient_protein_on_z $idn 2 383
display resetview
rotate y by 90
set_to_cpk

translate by 2.5 0.00 0.00
scale by 6.8

# pictures
colorize_domains

# animate goto 0
# render snapshot scene0.tga display %s
# animate goto 1
# render snapshot scene1.tga display %s
# animate goto 2
# render snapshot scene2.tga display %s
# animate goto 3
# render snapshot scene3.tga display %s
# animate goto 4
# render snapshot scene4.tga display %s
# animate goto 5
# render snapshot scene5.tga display %s

# animate goto 0
# animate forward
# animate pause
# animate next

# rotate x by -0.133333
# rotate y by 0.333333
# translate by -0.020000 -0.000000 0.000000
# translate by -0.030000 -0.000000 0.000000

# animate next
# scale by 1.040000

# translate by 0.010000 -0.000000 0.000000
# translate by 0.000000 -0.010000 0.000000
# animate next

# mol selection all
# mol representation CPK 1.300000 0.600000 10 8
# mol color Name
# mol addrep 0
# mol delrep 0 0
