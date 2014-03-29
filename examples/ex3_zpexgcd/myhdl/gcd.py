from myhdl import *

def mm_gcd(clock, reset, a, b, c, 
           start, finished):
    # set the default to "finished"
    finished._val = True  
    x,y = [Signal(intbv(0)[len(a):]) 
           for _ in range(2)]

    @always_seq(clock.posedge, reset=reset)
    def rtl():
        if start:
            finished.next = False
            x.next = a
            y.next = b
        else:
            if y == 0:
                finished.next = True
                c.next = x
            elif x > y:
                x.next = x - y
            else:
                y.next = y - x
            
    return rtl

clock = Signal(bool(0))
reset = ResetSignal(0, active=0, async=False)
a,b,c = [Signal(intbv(0)[32:]) for _ in range(3)]
start,finished = (Signal(False),Signal(True),)
toVerilog(mm_gcd, clock, reset, 
          a, b, c, start, finished)