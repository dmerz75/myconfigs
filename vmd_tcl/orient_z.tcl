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
