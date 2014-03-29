
from math import log, ceil
from myhdl import *

def mm_sop1(clock, reset, x, y, h):

    xd = [Signal(intbv(0, min=x.min, max=x.max))
          for _ in range(len(h))]

    # need to scale the outputs, the multiply will
    # create a number twice as big
    scale = int(len(x)/2)

    @always_seq(clock.posedge, reset=reset)
    def rtl():
        xd[0].next = x
        for ii in range(1,len(h)):
            xd[ii].next = xd[ii-1]
            
        sop = 0
        for ii in range(len(h)):
            c = h[ii]
            sop = sop + (c * xd[ii])

        y.next = sop >> scale

    return rtl

#-----------------------------------------------------
# create an instance and convert to Verilog
#-----------------------------------------------------
M = 4   # order of this simple filter
mv = 0x100 >> int(ceil(log(M,2)))
h = tuple([mv for _ in range(4)])
clock = Signal(bool(0))
reset = ResetSignal(0, active=0, async=True)
x = Signal(intbv(0, min=-2**15, max=2**15))
y = Signal(intbv(0, min=-2**15, max=2**15))
toVerilog(mm_sop1, clock, reset, x, y, h)
