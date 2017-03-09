
# 1
# mol new {/home/dale/sop_dev/tension/evaluate/example1/Struct_data/ADP4B9Q.structure_10000001} type {pdb} first 0 last -1 step 1 waitfor 1
# animate style Loop
# mol addfile {/home/dale/sop_dev/tension/evaluate/example1/Coord/ADP4B9Q.dcd} type {dcd} first 0 last -1 step 1 waitfor -1 0
# animate style Loop
# mol selection all
# mol representation CPK 1.300000 0.600000 10 8
# mol color Name
# mol addrep 0
# mol delrep 0 0
# mol addfile {/home/dale/sop_dev/tension/evaluate/example1/Coord/ADP4B9Q.dcd} type {dcd} first 0 last -1 step 1 waitfor 1 0
# end 1


proc example_rename { {molid 0} {args "name0" } } {
    # set name [lsearch $args 0]
    # mol rename $molid $name

    puts "set name [lsearch args 0]"
    puts "mol rename <molid> <name>"
}

proc example1 { } {

    set num1 [molinfo num]
    puts "molecules loaded: $num1"

    set mollist [molinfo list]

    puts "molecules:"
    for {set i 0} {$i < $num1} { incr i} {
        set x [lsearch [molinfo list] $i]
        puts -nonewline $i
        puts " $x"
    }
    # molinfo list
    # molinfo top

    puts "molinfo <molid>0 get numatoms"
    # puts "<molid> get {}"
    # puts "<molid> set {}"
    puts "molinfo 0 get numatoms"
}

example1
example_rename
