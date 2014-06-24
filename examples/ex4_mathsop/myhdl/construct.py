
from myhdl import *

ggens = []

gclock = None #Signal(bool(0))
greset = None #ResetSignal(0, active=0, async=True)

def init(clock=None, reset=None):
    global ggens,gclock,greset
    gclock,greset = clock,reset
    ggens = []
    return ggens

def end(g=None, dump=False):
    global ggens

    if dump:
        for gg in ggens:
            print("  %s -> %s : %s" % (gg.func.func_code.co_name,
                                       gg.func.func_code.co_varnames,
                                       gg.objlist))
    g = ggens
    # @todo: need global gens stack
    ggens = None
    # @todo: ???? do some checking ????
    return g

#=========================================#
def _m_mul(x, y, z):
    @always_comb
    def rtl_mul():
        z.next = x * y
    return rtl_mul


def _m_add(x, y, z):
    @always_comb
    def rtl_add():
        z.next = x + y
    return rtl_add


def _m_dff(x, y, load=None, clock=None, reset=None):
    # @todo: if we really want this to be "construction"
    #        this should use low-level primitives, the
    #        behavioral description can be used for simulation
    #        but otherwise dff should be used?
    global glock, greset
    clock = gclock if clock is None else clock
    reset = greset if reset is None else reset

    @always_seq(clock.posedge, reset=reset)
    def rtl_dff_load():
        if load: y.next = x

    @always_seq(clock.posedge, reset=reset)
    def rtl_dff():
        y.next = x

    g = rtl_dff if load is None else rtl_dff_load
    return g

#=========================================#
class Wire(object):
    def __init__(self, val):
        assert isinstance(val, (SignalType, Reg, Wire))
        _val = val if isinstance(val, SignalType) else val.d
        self.d = Signal(_val.val)

    def __add__(self, other):
        assert isinstance(other, (Reg, Wire, int))
        _max = max(abs(self.d.min), self.d.max)
        _max = 2*_max
        z = Wire(Signal(intbv(0, min=-_max, max=_max)))
        od = other if isinstance(other, int) else other.d
        g = _m_add(self.d, od, z.d)
        ggens.append(g)
        return z

    def __call__(self):
        return self.d
    
    def __radd__(self, other):
        assert isinstance(other, (Reg, Wire, int))
        _max = max(abs(self.d.min), self.d.max)
        _max = 2*_max
        z = Wire(Signal(intbv(0, min=-_max, max=_max)))
        od = other if isinstance(other, int) else other.d
        g = _m_add(self.d, od, z.d)
        ggens.append(g)
        return z


    def __mul__(self, other):
        assert isinstance(other, (Reg, Wire, int))
        _max = max(abs(self.d.min), self.d.max)
        _max = _max**2
        z = Wire(Signal(intbv(0, min=-_max, max=_max)))
        od = other if isinstance(other, int) else other.d
        g = _m_mul(self.d, od, z.d)
        ggens.append(g)
        return z


#=========================================#
#=========================================#
class Reg(object):
    # @todo: init=None, next=None
    def __init__(self, next=None):
        # @todo: if it is None it will need to be assigned
        #        later with @when decorator construct.when
        #        if it is None no generator created
        if next is None:
            self._load = Signal(bool(1))
        else:
            assert isinstance(next, (SignalType, Reg, Wire))
            _next = next if isinstance(next, SignalType) else next.d
            self.d = Signal(_next.val)
            # @todo _when signal
            g = _m_dff(_next, self.d)
            ggens.append(g)

    def __call__(self):
        return self.d
    
    def __add__(self, other):
        assert isinstance(other, (Reg, Wire, int))
        _max = max(abs(self.d.min), self.d.max)
        _max = 2*_max
        z = Wire(Signal(intbv(0, min=-_max, max=_max)))
        od = other if isinstance(other, int) else other.d
        g = _m_add(self.d, od, z.d)
        ggens.append(g)
        return z

    def __mul__(self, other):
        assert isinstance(other, (Reg, Wire, int))
        _max = max(abs(self.d.min), self.d.max)
        _max = _max**2
        z = Wire(Signal(intbv(0, min=-_max, max=_max)))
        od = other if isinstance(other, int) else other.d
        g = _m_mul(self.d, od, z.d)
        ggens.append(g)
        return z

    # @todo when decarator
    # y = Reg(x)
    # @y.when
    # def action():
    #    if x > 0:
    #        y.update()

