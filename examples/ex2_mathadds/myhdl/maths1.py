
import myhdl
from myhdl import Signal, intbv, always_comb


@myhdl.module
def mm_maths1(x, y, v, M=10):

    @always_comb
    def beh():
        v.next = (x + y) * M;

    return beh


# define the types and convert to Verilog
imin, imax = -2**15, 2**15
x = Signal(intbv(0, min=imin, max=imax))
y = Signal(intbv(0, min=imin, max=imax))
v = Signal(intbv(0, min=imin, max=imax))

myhdl.toVerilog.no_testbench = True
myhdl.toVerilog(mm_maths1(x, y, v, M=10))



    
