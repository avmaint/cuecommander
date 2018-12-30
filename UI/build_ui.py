"""TODO write comment
"""

__author__ = "Terry Doner"
__copyright__ = "Copyright 2018, Terry Doner"
__credits__ = ["Terry Doner"]
__license__ = "GPL 3"
__version__ = "0.1"

import sys
import time
from pathlib                import Path

from Config                 import config

from AudioRecording         import ar_actions
from ProjectorControl       import pc_actions
from MatrixControl          import mc_actions
from BmdControl             import bm_actions # BlackMagic ATEM Controls
#from OBSControl             import oc_actions # Open Broadcast Softwarefrom OBSControl             import oc_actions # Open Broadcast Software
from CSAVControl            import csav_actions

from tkinter import *
from tkinter import ttk


def ts():
    "Utility function to generate a timestamp"
    t = time.localtime(time.time())
    yyyy = str(t.tm_year)
    mm = str(t.tm_mon).zfill(2)
    dd = str(t.tm_mday).zfill(2)
    hh = str(t.tm_hour).zfill(2)
    mi = str(t.tm_min).zfill(2)
    se = str(t.tm_sec).zfill(2)
    stamp = yyyy + mm + dd + "_" + hh + mi + se
    return(stamp)


#setup Global UI
root = Tk()
root.title("CueCommander GUI")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

parent = root# ttk.Frame(root, padding="3 3 12 12")

n = ttk.Notebook(parent)
n.pack()

msgframe = ttk.Labelframe(n, padding="3 3 12 12", text="Messages:")
msgframe.pack()
n.add(msgframe, text="Messages")

tree = ttk.Treeview(msgframe, columns=('time', "level", "msg"))
# set the global

tree.column("time", width=150)
tree.heading("time", text="Time")
tree.column("level", width=50)
tree.heading("level", text="Level")
tree.column("msg", width=400)
tree.heading("msg", text="Message")

tree.pack()

def logmsg(level, message):
    t = ts()
    print(t, level, message  )
    tree.insert("", 0, values=(t, level, message))

mainframe = ttk.Frame(n, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
n.add(mainframe, text="Shortcuts")

ttk.Label(mainframe, text="Projectors").grid(column=1, row=1, sticky=W)
ttk.Button(mainframe, text="On",     command= lambda:pc_actions.projector_on(1,1) ).grid(column=2, row=1, sticky=W)
ttk.Button(mainframe, text="Off",    command= lambda:pc_actions.projector_off(1,1) ).grid(column=3, row=1, sticky=W)
ttk.Button(mainframe, text="Status", command= lambda:pc_actions.projector_status(1,1) ).grid(column=4, row=1, sticky=W)

ttk.Label(mainframe, text="Side (AC) Screen Source").grid(column=1, row=2, sticky=W)
ttk.Button(mainframe, text="CDWU-0009", command= lambda:mc_actions.kramer_AC_CDWU0009(1,1) ).grid(column=3, row=2, sticky=W)
ttk.Button(mainframe, text="CDMU-A001", command= lambda:mc_actions.kramer_AC_CDMUA001(1,1) ).grid(column=2, row=2, sticky=W)

ttk.Label(mainframe, text="Centre (B) Screen Source").grid(column=1, row=3, sticky=W)
ttk.Button(mainframe, text="CDWU-0009", command= lambda:mc_actions.kramer_centrems(1,1) ).grid(column=2, row=3, sticky=W)
ttk.Button(mainframe, text="Atem Prog", command= lambda:mc_actions.kramer_centrePrg(1,1) ).grid(column=3, row=3, sticky=W)
ttk.Button(mainframe, text="Atem Aux", command= lambda:mc_actions.kramer_centreAux(1,1) ).grid(column=4, row=3, sticky=W)
ttk.Button(mainframe, text="CDMU-A001", command= lambda:mc_actions.kramer_centreNorm(1,1) ).grid(column=5, row=3, sticky=W)

ttk.Label(mainframe, text="Lobby/Nursery Source").grid(column=1, row=6, sticky=W)
ttk.Button(mainframe, text="Atem Aux", command= lambda:mc_actions.kramer_LNvmAux(1,1) ).grid(column=3, row=6, sticky=W)
ttk.Button(mainframe, text="Atem Prog", command= lambda:mc_actions.kramer_LNvmPgm(1,1) ).grid(column=2, row=6, sticky=W)
ttk.Button(mainframe, text="CDWU-0009", command= lambda:mc_actions.kramer_LNms(1,1) ).grid(column=4, row=6, sticky=W)

ttk.Label(mainframe, text="Matrix Status").grid(column=1, row=11, sticky=W)
ttk.Button(mainframe, text="Query", command= lambda:mc_actions.kramer_status(1,1) ).grid(column=2, row=11, sticky=W)

ttk.Label(mainframe, text="Rear Source").grid(column=1, row=7, sticky=W)
ttk.Button(mainframe, text="CDWU-0009", command= lambda:mc_actions.kramer_rear_CDWU0009(1,1) ).grid(column=3, row=7, sticky=W)
ttk.Button(mainframe, text="CDMU-A001 SD", command= lambda:mc_actions.kramer_rear_CDMUA001(1,1) ).grid(column=2, row=7, sticky=W)

matrixframe = ttk.Labelframe(n, padding="3 3 12 12", text="Matrix:")
matrixframe.grid(column=1, row=12, sticky=(N,W,E,S))
n.add(matrixframe, text="Matrix")

ttk.Label(matrixframe, text="CDMU-A001\nA", wraplength=50).grid(column=3, row=0, sticky=(N) )
ttk.Label(matrixframe, text="CDMU-A001\nB", wraplength=50).grid(column=4, row=0, sticky=(N) )
ttk.Label(matrixframe, text="CDMU-A001\nC", wraplength=50).grid(column=5, row=0, sticky=(N) )
ttk.Label(matrixframe, text="CDMU-A001\nSD",wraplength=50).grid(column=6, row=0, sticky=(N) )
ttk.Label(matrixframe, text="CDWU-0009",   wraplength=50).grid(column=7, row=0, sticky=(N) )
ttk.Label(matrixframe, text="ATEM\nProg",   wraplength=50).grid(column=8, row=0, sticky=(N) )
ttk.Label(matrixframe, text="ATEM\nAux",    wraplength=50).grid(column=9, row=0, sticky=(N) )
ttk.Label(matrixframe, text="Color\nSource", wraplength=50).grid(column=10, row=0, sticky=(N) )

ttk.Label(matrixframe, text="1").grid(column=3, row=1 )
ttk.Label(matrixframe, text="2").grid(column=4, row=1 )
ttk.Label(matrixframe, text="3").grid(column=5, row=1 )
ttk.Label(matrixframe, text="4").grid(column=6, row=1 )
ttk.Label(matrixframe, text="5").grid(column=7, row=1 )
ttk.Label(matrixframe, text="6").grid(column=8, row=1 )
ttk.Label(matrixframe, text="7").grid(column=9, row=1 )
ttk.Label(matrixframe, text="8").grid(column=10, row=1 )

ttk.Label(matrixframe, text="Projector East").grid(column=1, row=2, sticky=(W, E))
ttk.Label(matrixframe, text="Projector Centre").grid(column=1, row=3, sticky=(W, E))
ttk.Label(matrixframe, text="Projector West").grid(column=1, row=4, sticky=(W, E))
ttk.Label(matrixframe, text="Projector Rear").grid(column=1, row=5, sticky=(W, E))
ttk.Label(matrixframe, text="ATEM IN1").grid(column=1, row=6, sticky=(W, E))
ttk.Label(matrixframe, text="ATEM IN3").grid(column=1, row=7, sticky=(W, E))
ttk.Label(matrixframe, text="Lobby").grid(column=1, row=8, sticky=(W, E))
ttk.Label(matrixframe, text="Nursery").grid(column=1, row=9, sticky=(W, E))

ttk.Label(matrixframe, text="1").grid(column=2, row=2, sticky=(W, E))
ttk.Label(matrixframe, text="2").grid(column=2, row=3, sticky=(W, E))
ttk.Label(matrixframe, text="3").grid(column=2, row=4, sticky=(W, E))
ttk.Label(matrixframe, text="4").grid(column=2, row=5, sticky=(W, E))
ttk.Label(matrixframe, text="5").grid(column=2, row=6, sticky=(W, E))
ttk.Label(matrixframe, text="6").grid(column=2, row=7, sticky=(W, E))
ttk.Label(matrixframe, text="7").grid(column=2, row=8, sticky=(W, E))
ttk.Label(matrixframe, text="8").grid(column=2, row=9, sticky=(W, E))

from functools import partial

def f(i, o):
    #mc_actions.kramer_in_out(i, o)
    print( "i=%d, o=%d" %(i,o))

out1 = StringVar()
outnum = 1
for innum in range(1, 9):

    b = ttk.Radiobutton(matrixframe,
                        text='%d %d'%(innum, outnum),
                        variable=out1,
                        value=str(innum),
                        #command=lambda:mc_actions.kramer_in_out(innum,outnum)
                        #command=lambda: f(innum,outnum)
                        command=partial(f, innum, outnum)
                        )
    b.grid(column=innum+2,row=outnum+1)

f(7,1)

# out1in2 = ttk.Radiobutton(matrixframe, text='', variable=out1, value='2').grid(column=4,row=2)
# out1in3 = ttk.Radiobutton(matrixframe, text='', variable=out1, value='3').grid(column=5,row=2)
# out1in4 = ttk.Radiobutton(matrixframe, text='', variable=out1, value='4').grid(column=6,row=2)
# out1in5 = ttk.Radiobutton(matrixframe, text='', variable=out1, value='5').grid(column=7,row=2)
# out1in6 = ttk.Radiobutton(matrixframe, text='', variable=out1, value='6').grid(column=8,row=2)
# out1in7 = ttk.Radiobutton(matrixframe, text='', variable=out1, value='7').grid(column=9,row=2)
# out1in8 = ttk.Radiobutton(matrixframe, text='', variable=out1, value='8').grid(column=10,row=2)


out2 = StringVar()
out2in1 = ttk.Radiobutton(matrixframe, text='', variable=out2, value='1', command=lambda:mc_actions.kramer_in_out(1,2)).grid(column=3,row=3)
out2in2 = ttk.Radiobutton(matrixframe, text='', variable=out2, value='2', command=lambda:mc_actions.kramer_in_out(2,2)).grid(column=4,row=3)
out2in3 = ttk.Radiobutton(matrixframe, text='', variable=out2, value='3', command=lambda:mc_actions.kramer_in_out(3,2)).grid(column=5,row=3)
out2in4 = ttk.Radiobutton(matrixframe, text='', variable=out2, value='4', command=lambda:mc_actions.kramer_in_out(4,2)).grid(column=6,row=3)
out2in5 = ttk.Radiobutton(matrixframe, text='', variable=out2, value='5', command=lambda:mc_actions.kramer_in_out(5,2)).grid(column=7,row=3)
out2in6 = ttk.Radiobutton(matrixframe, text='', variable=out2, value='6', command=lambda:mc_actions.kramer_in_out(6,2)).grid(column=8,row=3)
out2in7 = ttk.Radiobutton(matrixframe, text='', variable=out2, value='7', command=lambda:mc_actions.kramer_in_out(7,2)).grid(column=9,row=3)
out2in8 = ttk.Radiobutton(matrixframe, text='', variable=out2, value='8', command=lambda:mc_actions.kramer_in_out(8,2)).grid(column=10,row=3)

out3 = StringVar()
out3in1 = ttk.Radiobutton(matrixframe, text='', variable=out3, value='1').grid(column=3,row=4)
out3in2 = ttk.Radiobutton(matrixframe, text='', variable=out3, value='2').grid(column=4,row=4)
out3in3 = ttk.Radiobutton(matrixframe, text='', variable=out3, value='3').grid(column=5,row=4)
out3in4 = ttk.Radiobutton(matrixframe, text='', variable=out3, value='4').grid(column=6,row=4)
out3in5 = ttk.Radiobutton(matrixframe, text='', variable=out3, value='5').grid(column=7,row=4)
out3in6 = ttk.Radiobutton(matrixframe, text='', variable=out3, value='6').grid(column=8,row=4)
out3in7 = ttk.Radiobutton(matrixframe, text='', variable=out3, value='7').grid(column=9,row=4)
out3in8 = ttk.Radiobutton(matrixframe, text='', variable=out3, value='8').grid(column=10,row=4)

out4 = StringVar()
out4in1 = ttk.Radiobutton(matrixframe, text='', variable=out4, value='1').grid(column=3,row=5)
out4in2 = ttk.Radiobutton(matrixframe, text='', variable=out4, value='2').grid(column=4,row=5)
out4in3 = ttk.Radiobutton(matrixframe, text='', variable=out4, value='3').grid(column=5,row=5)
out4in4 = ttk.Radiobutton(matrixframe, text='', variable=out4, value='4').grid(column=6,row=5)
out4in5 = ttk.Radiobutton(matrixframe, text='', variable=out4, value='5').grid(column=7,row=5)
out4in6 = ttk.Radiobutton(matrixframe, text='', variable=out4, value='6').grid(column=8,row=5)
out4in7 = ttk.Radiobutton(matrixframe, text='', variable=out4, value='7').grid(column=9,row=5)
out4in8 = ttk.Radiobutton(matrixframe, text='', variable=out4, value='8').grid(column=10,row=5)

out5 = StringVar()
out5in1 = ttk.Radiobutton(matrixframe, text='', variable=out5, value='1', command=lambda:mc_actions.kramer_in_out(1,5)).grid(column=3,row=6)
out5in2 = ttk.Radiobutton(matrixframe, text='', variable=out5, value='2', command=lambda:mc_actions.kramer_in_out(2,5)).grid(column=4,row=6)
out5in3 = ttk.Radiobutton(matrixframe, text='', variable=out5, value='3', command=lambda:mc_actions.kramer_in_out(3,5)).grid(column=5,row=6)
out5in4 = ttk.Radiobutton(matrixframe, text='', variable=out5, value='4', command=lambda:mc_actions.kramer_in_out(4,5)).grid(column=6,row=6)
out5in5 = ttk.Radiobutton(matrixframe, text='', variable=out5, value='5', command=lambda:mc_actions.kramer_in_out(5,5)).grid(column=7,row=6)
out5in6 = ttk.Radiobutton(matrixframe, text='', variable=out5, value='6', command=lambda:mc_actions.kramer_in_out(6,5)).grid(column=8,row=6)
out5in7 = ttk.Radiobutton(matrixframe, text='', variable=out5, value='7', command=lambda:mc_actions.kramer_in_out(7,5)).grid(column=9,row=6)
out5in8 = ttk.Radiobutton(matrixframe, text='', variable=out5, value='8', command=lambda:mc_actions.kramer_in_out(8,5)).grid(column=10,row=6)

out6 = StringVar()
out6in1 = ttk.Radiobutton(matrixframe, text='', variable=out6, value='out6in1').grid(column=3,row=7)
out6in2 = ttk.Radiobutton(matrixframe, text='', variable=out6, value='out6in2').grid(column=4,row=7)
out6in3 = ttk.Radiobutton(matrixframe, text='', variable=out6, value='out6in3').grid(column=5,row=7)
out6in4 = ttk.Radiobutton(matrixframe, text='', variable=out6, value='out6in4').grid(column=6,row=7)
out6in5 = ttk.Radiobutton(matrixframe, text='', variable=out6, value='out6in5').grid(column=7,row=7)
out6in6 = ttk.Radiobutton(matrixframe, text='', variable=out6, value='out6in6').grid(column=8,row=7)
out6in7 = ttk.Radiobutton(matrixframe, text='', variable=out6, value='out6in7').grid(column=9,row=7)
out6in8 = ttk.Radiobutton(matrixframe, text='', variable=out6, value='out6in8').grid(column=10,row=7)

out7 = StringVar()
out7in1 = ttk.Radiobutton(matrixframe, text='', variable=out7, value='out7in1').grid(column=3,row=8)
out7in2 = ttk.Radiobutton(matrixframe, text='', variable=out7, value='out7in2').grid(column=4,row=8)
out7in3 = ttk.Radiobutton(matrixframe, text='', variable=out7, value='out7in3').grid(column=5,row=8)
out7in4 = ttk.Radiobutton(matrixframe, text='', variable=out7, value='out7in4').grid(column=6,row=8)
out7in5 = ttk.Radiobutton(matrixframe, text='', variable=out7, value='out7in5').grid(column=7,row=8)
out7in6 = ttk.Radiobutton(matrixframe, text='', variable=out7, value='out7in6').grid(column=8,row=8)
out7in7 = ttk.Radiobutton(matrixframe, text='', variable=out7, value='out7in7').grid(column=9,row=8)
out7in8 = ttk.Radiobutton(matrixframe, text='', variable=out7, value='out7in8').grid(column=10,row=8)

out8 = StringVar()
out8in1 = ttk.Radiobutton(matrixframe, text='', variable=out8, value='out8in1').grid(column=3,row=9)
out8in2 = ttk.Radiobutton(matrixframe, text='', variable=out8, value='out8in2').grid(column=4,row=9)
out8in3 = ttk.Radiobutton(matrixframe, text='', variable=out8, value='out8in3').grid(column=5,row=9)
out8in4 = ttk.Radiobutton(matrixframe, text='', variable=out8, value='out8in4').grid(column=6,row=9)
out8in5 = ttk.Radiobutton(matrixframe, text='', variable=out8, value='out8in5').grid(column=7,row=9)
out8in6 = ttk.Radiobutton(matrixframe, text='', variable=out8, value='out8in6').grid(column=8,row=9)
out8in7 = ttk.Radiobutton(matrixframe, text='', variable=out8, value='out8in7').grid(column=9,row=9)
out8in8 = ttk.Radiobutton(matrixframe, text='', variable=out8, value='out8in8').grid(column=10,row=9)


proj_status = StringVar()

def p_on():
    #pc_actions.projector_on(1, 1)
    proj_status.set('On')
    logmsg("I", "Projectors turned on.")

def p_off():
    proj_status.set('Off')
    logmsg("I", "Projectors turned off.")

am0800frame = ttk.Frame(n, padding="3 3 12 12" )
am0800frame.pack()
n.add(am0800frame, text="08:00 AM")
ttk.Button(am0800frame, text="Projectors On",     command=lambda:p_on()).grid(column=2, row=1, sticky=W)

proj_status = StringVar()
ttk.Label(am0800frame, textvariable=proj_status).grid(column=3, row=1, sticky=(W, E))
proj_status.set('Off')


am1130frame = ttk.Frame(n, padding="3 3 12 12" )
am1130frame.pack()
n.add(am1130frame, text="11:30 AM")
ttk.Button(am1130frame, text="Projectors Off",     command= lambda:p_off() ).grid(column=2, row=1, sticky=W)
ttk.Label(am1130frame, textvariable=proj_status).grid(column=3, row=1, sticky=(W, E))



