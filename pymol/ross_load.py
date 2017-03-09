import colorsys,sys
import os

from pymol import cmd

# mylib/faf
# my_library = os.path.expanduser('~/.pylib')
# sys.path.append(my_library)
# from mylib.run_command import run_command
# from pymol.color_by_restype import color_by_restype
# print 'exit'
# sys.exit()


def ross_load(molecule):
    '''
    for Jennifer Ross.
    '''
    # if pic == 0:
    cmd.reinitialize()
    # cmd.depth_cue(1) # fails
    # cmd.set_depth_cue("off") # fails
    cmd.set("depth_cue","off")
    cmd.bg_color('white')


    fasta = molecule + '.fasta'
    pdb = molecule + '.pdb'

    print molecule
    print fasta
    print pdb

    cmd.load(fasta)

    if not os.path.exists(pdb):
        cmd.save(pdb)


    # cmd.show( string representation="", string selection="" )
    cmd.show('spheres','all')
    # cmd.ray(5600) # works



    # cmd.set_view(string-or-sequence view)
    # cmd.set_view(1.0 1.0 1.0 0.0 0.0)
                  # 0.999876618,   -0.000452542,   -0.015699286,\
                  # 0.000446742,    0.999999821,   -0.000372844,\
                  # 0.015699454,    0.000365782,    0.999876678,\
                  # 0.000000000,    0.000000000, -150.258514404,\
                  # 11.842411041,   20.648729324,    8.775371552,\
                  # 118.464958191,  182.052062988,    0.000000000 )


    # cmd.ray_trace_mode(0)
    # cmd.zoom('all')
    # cmd.color_by_restype
    # cmd.png(molecule)

    # # end of ross_load
    # if pic != 0:
    #     cmd.png(molecule,
    #             width=4800,
    #             height=3600,
    #             dpi=1200, # currently creates 1.2 Mb.
    #             ray=0, # shadowing if 1,2
    #             quiet=0)
    # pic = 0

def ross_pic(molecule):
    '''
    for Jennifer Ross picture.
    '''
    # if pic != 0:
    cmd.png(molecule,
            width=4800,
            height=3600,
            dpi=1200, # currently creates 1.2 Mb.
            ray=0, # shadowing if 1,2
            quiet=0)
    # pic = 0





cmd.extend("ross_load",ross_load)
cmd.extend("ross_pic",ross_pic)
# run ~/.pylib/pymol/color_by_restype.py
