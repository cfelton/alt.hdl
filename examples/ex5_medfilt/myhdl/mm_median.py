
from myhdl import *

def mm_medtop(clock, reset, x, dvi, med, dvo, N=9):
    """
    """
    xcnt = Signal(intbv(1, min=0, max=N+1))
    win = [Signal(intbv(0)[8:]) for _ in range(N)]
    won = [Signal(intbv(0)[8:]) for _ in range(N)]
    okd = Signal(intbv(0)[N+1:])
    ok = Signal(bool(0))

    _med = Signal(med.val)

    gmed = mm_median(clock, reset, win, won, _med)

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
            
        
                  
def mm_median(clock, reset, wi, wo, med):
    """ hardware version of the median
    """
    assert isinstance(wi, list)
    assert isinstance(wo, list)
    N,st = len(wi), wi[0]
    z = [wi,] + [[Signal(st.val) for _ in range(N)]
                       for stage in range(N)]
    
    # create the compare stages
    g = [m_cmp(clock, reset, z[ii], z[ii+1], ii) for ii in range(N)]
    
    last_stage = z[N]
    MN = N//2
    @always_comb #(clock.posedge)
    def rtl():
        for ii in range(N):
            wo[ii].next = last_stage[ii]
        med.next = last_stage[MN]

    return g, rtl


def m_cmp(clock, reset, x, z, stage=0):
    """ compare stage
    """
    assert isinstance(x, list)
    assert isinstance(z, list)
    N = len(z)

    def _min(a, b): return a if a < b else b
    def _max(a, b): return a if a > b else b

    K = 0 if stage%2 else 1
    @always_seq(clock.posedge, reset=reset)
    def rtl():
        for ii in range(N):
            z[ii].next = x[ii]
        for ii in range(K, N-1, 2):
            z[ii].next   = x[ii] if x[ii] < x[ii+1] else x[ii+1] #_min(x[ii], x[ii+1])
            z[ii+1].next = x[ii] if x[ii] > x[ii+1] else x[ii+1] #_max(x[ii], x[ii+1])

    return rtl


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