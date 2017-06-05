# /home/dale/Dropbox/completed/biocat_completed/sop_sop_dev__01-15-2014_1410t__run_j15lee1_l1h1__91
# vmd pdb2mol.ent -dispdev text -e animatepsf.tcl
# animate write psf Coord/2mol.psf

proc make_psf_dir { } {
    if {[file isdirectory psf]} {
        # the directory 'movies' exists
        puts "directory exists .."
    } else {
        # create the directory
        file mkdir psf
    }
}

proc write_my_psf { {id 0} } {

    make_psf_dir

    set name [molinfo $id get name]
    puts "writing $name.psf"
    animate write psf psf/$name.psf
    # writepsf psf/$name.psf
    # animate write psf Coord/2mol.psf


}
# write_my_psf 0

# for sopnucleo - use Struct_data
#   sop-nucleo-hsp70_sop-nucleo__02-15-2014_1342t__runsopnuc__32/Struct_data/ATP4B9Q.structure_101
# for gsop - Use structures
#   loaded trajectory
# exit

proc write_partial_dcd { {filename "one.dcd"} {sel "all"} {start 0} {stop 100} {step 10} } {
    #
    animate write dcd $filename sel $sel beg $start end $stop skip $step
}


proc renumber_residue_1chain { sel name } {

    $sel set resid [$sel get residue]
    $sel writepdb $name.pdb
}
