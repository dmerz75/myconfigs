from molecule import *
from AtomSel import AtomSel

load('psf','../nolh495917.psf','dcd','nolh495917.dcd')

resid_1 = AtomSel('resid 1 to 383', frame=50)
resid_1.frame()
