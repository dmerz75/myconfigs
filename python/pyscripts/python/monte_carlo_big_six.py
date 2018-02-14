#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
print (sys.version)
import time
import numpy as np
from pylib.BigSix import BigSix

my_dir = os.path.abspath(os.path.dirname(__file__))


def place_your_bets():
    W = BigSix()
    # print(W.wheel.keys())
    # print(len(W.wheel.keys()))
    W.cash = 50.0
    W.set_wager(1,1.)
    W.set_wager(3,2.)
    W.show_wager()

    W.spin(58625)


    W.print_results()


place_your_bets()
