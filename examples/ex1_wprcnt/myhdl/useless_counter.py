
from myhdl import *

def mm_cnt(clock, reset, out):
    @always_seq(clock.posedge, reset=reset)
    def rtl():
        if out <= 30:
            out.next = out + 1
        else:
            out.next = out - 1
    return rtl

clock = Signal(bool(0))
reset = ResetSignal(0, active=0, async=True)
out = Signal(intbv(0, min=0, max=32))
toVerilog(mm_cnt, clock, reset, out)