
import myhdl
from myhdl import Signal, ResetSignal, intbv, always_seq, always_comb


@myhdl.block
def mm_cnt(clock, reset, out):
    counter = Signal(out.val)
    
    @always_seq(clock.posedge, reset=reset)
    def beh():
        if counter <= 30:
            counter.next = counter + 1
        else:
            counter.next = counter - 1
            
    @always_comb
    def beh_assign():
        out.next = counter 
        
    return beh, beh_assign


clock = Signal(bool(0))
reset = ResetSignal(0, active=0, async=True)
out = Signal(intbv(0, min=0, max=32))

# the latest myhdl 1.0 is moving to the "block" decorator,
# the simulation and conversion methods are available from
# the `BlockInstance`
# myhdl.toVerilog.no_testbench = True
# myhdl.toVerilog(mm_cnt(clock, reset, out))

inst = mm_cnt(clock, reset, out)
# this is wrong, should keep the same names
inst.convert(tb=False)

