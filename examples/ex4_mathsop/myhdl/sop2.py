
from copy import copy
from myhdl import *

import construct
from construct import Reg

def mm_sop2(clock, reset, x, y, hs):

    # use the "construction" to build the SOP
    construct.init(clock, reset)
    def taps(x, N):
        return [x] if N <= 1 else [x] + taps(Reg(x), N-1)
    w = sum([x*h for x,h in zip(taps(Reg(x), len(hs)), hs)])        
    cgens = construct.end()

    # the resulting Wire will have grown in bit size, we 
    # need to reduce the bits down
    wwire = w()
    print("wwire is %s %s" % (type(wwire), wwire))
    @always_seq(clock.posedge, reset=reset)
    def rtl_scale():
        y.next = wwire >> 8

    return cgens, rtl_scale

#-----------------------------------------------------
# create an instance and convert to Verilog
#-----------------------------------------------------
clock = Signal(bool(0))
reset = ResetSignal(0, active=0, async=True)
x = Signal(intbv(0, min=-2**15, max=2**15))
y = Signal(intbv(0, min=-2**15, max=2**15))
h = [0x40 for _ in range(4)]

tbdut = mm_sop2( clock, reset, x, y, h)
@always(delay(3))
def tbclk():
    clock.next = not clock

@instance
def tbstim():
    reset.next = reset.active
    yield delay(10)
    reset.next = not reset.active
    x.next = 1
    for _ in range(10):
        print(y)
        yield clock.posedge
    raise StopSimulation

print("*** SIMULATION ***")
Simulation((tbdut, tbclk, tbstim,)).run()
print("*** VERILOG ***")
toVerilog(mm_sop2, clock, reset, x, y, h)
