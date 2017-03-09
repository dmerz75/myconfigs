# from vmd:

proc sbdload { molname } {

    mol new
    mol addfile $molname/vac.psf
    mol addfile $molname/combined.dcd waitfor all

    # Get last loaded molecule.
    set molnum [lindex [molinfo list] end]

    mol rename $molnum $molname
    colorize_sbd_newcartoon $molnum

    puts "loading complete for $molnum $molname"
}

sbdload sbdlid1
sbdload sbdlid2
