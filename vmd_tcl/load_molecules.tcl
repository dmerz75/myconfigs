# file: load_molecule.tcl
# \n works!

proc load_psf_dcd { {psf_file "1.psf" } {dcd_file "pull.dcd" } } {
    mol new $psf_file type psf first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
    mol addfile $dcd_file type dcd first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
    puts file dirname $dcd_file
}
proc find_by_ext { {basedir .} { by_type "dcd" } } {

    puts "arg1: basedir (cwd) by_type ('dcd')"
    set oldwd [pwd]
    cd $basedir
    set cwd [pwd]
    set filenames [glob -nocomplain *.$by_type]
    set files {}
    foreach filename $filenames {
        lappend files [file join $cwd $filename]
    }
    cd $oldwd
    return $files
}
# -------------------------------------
# ......^ works;      ......v  testing.
# -------------------------------------

proc load_dcdfiles_by_regex_numeral { { basedir . } { pos -1 } } {
    puts "arg: basedir . pos -1"
    puts "basedir:" $basedir "pos:" $pos
    set cwd [pwd]
    puts $cwd

    set dcd_files [find_by_ext $basedir dcd]
    puts $dcd_files

    set psf_file [find_by_ext $basedir psf]
    puts $psf_file

    foreach filename $dcd_files {
        puts $pos
        # set file2 [lindex [file split [file rootname $filename]] end-1]
        set file2 [lindex [file split [file rootname $filename]] $pos]
        puts $file2
        # puts file nativename $filename -fails
        # load_psf_dcd $psf_file $filename
    }
    # find_by_ext $cwd "dcd"
    # puts $file_list
}



proc get_numeral_from_filename { { file_list "" } { pos -1 } } {
    puts "arg1: pos -1"
    set cwd [pwd]
    puts $cwd

    set dcd_files [find_by_ext $cwd dcd]
    puts $dcd_files

    set psf_file [find_by_ext $cwd psf]
    puts $psf_file


    foreach filename $dcd_files {
        set file1 [file rootname $filename]
        puts $file1
        # puts file rootname $filename
        # lrange [file split [file dirname $name]] 1 end
        # set file2 [lrange [file split [file rootname $filename]] 1 end]
        # set file2 [file split [file rootname $filename]]
        set file2 [lindex [file split [file rootname $filename]] end-1]
        puts $file2
        # puts file nativename $filename -fails
        # load_psf_dcd $psf_file $filename
    }
    # find_by_ext $cwd "dcd"
    # puts $file_list
}

proc testing { {dcd_file "pull.dcd" } } {
    # puts file dirname $dcd_file
    set curdir [pwd]
}

proc find_files_and_dirs { {basedir .} { by_type "dcd" } } {
    set oldwd [pwd]
    cd $basedir
    set cwd [pwd]
    set filenames [glob -nocomplain * .*]
    # set filenames [glob -nocomplain *.$by_type]
    set files {}
    # set filt [string length $filterScript]
    foreach filename $filenames {
        lappend files [file join $cwd $filename]
        # if {!$filt || [eval $filterScript [list $filename]]} {
        #     lappend files [file join $cwd $filename]
        # }
        if {[file isdirectory $filename]} {
            set files [concat $files $filename]
        }
    }
    cd $oldwd
    return $files
}



# proc find {{basedir .} {filterScript {}}} {
#     set oldwd [pwd]
#     cd $basedir
#     set cwd [pwd]
#     set filenames [glob -nocomplain * .*]
#     set files {}
#     set filt [string length $filterScript]
#     foreach filename $filenames {
#         if {!$filt || [eval $filterScript [list $filename]]} {
#             lappend files [file join $cwd $filename]
#         }
#         if {[file isdirectory $filename]} {
#             set files [concat $files [find $filename $filterScript]]
#         }
#     }
#     cd $oldwd
#     return $files
# }


# proc example {first {second ""} args} {
#     if {$second eq ""} {
#         puts "There is only one argument and it is: $first"
#         return 1
#     } else {
#         if {$args eq ""} {
#             puts "There are two arguments - $first and $second"
#             return 2
#         } else {
#             puts "There are many arguments - $first and $second and $args"
#             return "many"
#         }
#     }
# }
# set count1 [example ONE]
# set count2 [example ONE TWO]
# set count3 [example ONE TWO THREE ]
# set count4 [example ONE TWO THREE FOUR]
# puts "The example was called with $count1, $count2, $count3, and $count4 Arguments"
