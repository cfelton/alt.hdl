
import myhdl
from myhdl import Signal, ResetSignal, intbv, always_seq


@myhdl.module
def mm_cnt(clock, reset, out):
    @always_seq(clock.posedge, reset=reset)
    def beh():
        if out <= 30:
            out.next = out + 1
        else:
            out.next = out - 1
    return beh


clock = Signal(bool(0))
reset = ResetSignal(0, active=0, async=True)
out = Signal(intbv(0, min=0, max=32))

myhdl.toVerilog.no_testbench = True
myhdl.toVerilog(mm_cnt(clock, reset, out))
