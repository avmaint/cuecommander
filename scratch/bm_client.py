#from osc4py3.as_eventloop import *

#x = osc_startup()

from BmdControl             import bm_actions # BlackMagic ATEM Controls

bm_actions.aux_source_prog(True, 1.0)
#bm_actions.aux_source_vmac(True, 1.0)

#y = osc_process()

#z = osc_terminate()

print("done")