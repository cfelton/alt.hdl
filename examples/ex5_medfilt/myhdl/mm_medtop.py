
from myhdl import *
from mm_median import mm_median

class System: pass

def mm_medtop(clock, reset, x, dvi, med, dvo, N=9):
    """ top-level for the median calculation
    """
    xcnt = Signal(intbv(1, min=0, max=N+1))
    win = [Signal(intbv(0)[8:]) for _ in range(N)]
    won = [Signal(intbv(0)[8:]) for _ in range(N)]
    okd = Signal(intbv(0)[N+1:])
    ok = Signal(bool(0))

    _med = Signal(med.val)
    
    sys = System()
    sys.clock = clock
    sys.reset = reset

    gmed = mm_median(sys, win, won, _med)

    @always_comb
    def rtl_ror():
        o = okd[0]
        for ii in range(1,N):
            o = okd[ii] or o
        ok.next = False if o else True

    @always_seq(clock.posedge, reset=reset)
    def rtl_in():
        okd.next = okd >> 1
        dvo.next = okd[0]
        med.next = _med

        if xcnt == N and dvi:
            win[xcnt-1].next = x
            okd.next[N] = True
            xcnt.next = 1

        elif ok and dvi:
            win[xcnt-1].next = x
            xcnt.next = xcnt + 1

    return gmed, rtl_ror, rtl_in

            
#-----------------------------------------------------
# create an instance and convert to Verilog
#-----------------------------------------------------
clock = Signal(bool(0))
reset = ResetSignal(0, active=1, async=False)
x = Signal(intbv(0)[8:])
dvi = Signal(bool(0))
med = Signal(intbv(0)[8:])
dvo = Signal(bool(0))

tbdut = mm_medtop(clock, reset, x, dvi, med, dvo)
def _test():
    @always(delay(5))
    def tbclk():
        clock.next = not clock
    
    @instance
    def tbstim():
        reset.next = reset.active
        yield delay(100)
        reset.next = not reset.active
        yield clock.posedge
                
        for ii in range(1000):
            x.next = ii%256
            dvi.next = True
            yield clock.posedge

        raise StopSimulation

    return tbdut, tbclk, tbstim

traceSignals.name = 'vcd/_test'
Simulation(traceSignals(_test)).run()        
toVerilog(mm_medtop, clock, reset, x, dvi, med, dvo)