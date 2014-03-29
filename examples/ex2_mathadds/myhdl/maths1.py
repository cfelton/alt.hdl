
from myhdl import *

def mm_maths1(x, y, v, M=10):

    @always_comb
    def rtl():
        v.next = (x + y) * M;

    return rtl

# define the types and convert to Verilog
imin,imax = -2**15, 2**15
x = Signal(intbv(0, min=imin, max=imax))
y = Signal(intbv(0, min=imin, max=imax))
v = Signal(intbv(0, min=imin, max=imax))
toVerilog(mm_maths1, x, y, v, M=10)



    
