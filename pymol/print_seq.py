import colorsys,sys
from pymol import cmd


def print_seq():
    print cmd.get_fastastr('all')


cmd.extend("print_seq",print_seq)
