
import math

from myhdl import *
# @todo: move clock and reset wrappers here
from mysigs import Clock, Reset

class System:
    def __init__(self, clock=None, reset=None, frequency=1):
        self.clock = Clock(0, frequency=frequency) if clock is None else clock
        self.reset = Reset(0, active=1, async=False) if reset is None else reset
        
class VGA:
    def __init__(
        self, 
        hsync=None, vsync=None,
        red=None, green=None, blue=None,
        pxlen=None, active=None,
        color_depth=(10,10,10,)
    ):
        """
        color_depth the number of bits per RGB
        """
        self.N = color_depth

        # the sync signals
        self.hsync = Signal(bool(1)) if hsync is None else hsync
        self.vsync = Signal(bool(1)) if vsync is None else vsync
        # the RGB signals to the video
        cd = color_depth
        self.red = Signal(intbv(0)[cd[0]:]) if red is None else red
        self.green = Signal(intbv(0)[cd[1]:]) if green is None else green
        self.blue = Signal(intbv(0)[cd[2]:]) if blue is None else blue

        # logic VGA timing signals, used internally only
        self.pxlen  = Signal(bool(0)) if pxlen is None else pxlen
        self.active = Signal(bool(0)) if active is None else active

        # these are used for verification.
        self.States = enum('NONE', 'ACTIVE',
                          'HOR_FRONT_PORCH', 'HSYNC', 'HOR_BACK_PORCH',
                          'VER_FRONT_PORCH', 'VSYNC', 'VER_BACK_PORCH')
        self.state = Signal(self.States.ACTIVE)  


class VideoMemory:
    def __init__(self, size=128, res=(640,480,), width=10):
        aw = math.ceil(math.log(size,2))
        width = width * 3
        # write port
        #self.wr = Signal(bool(0))
        #self.wdat = Signal(intbv(0)[width:])
        #self.wadr = Signal(intbv(0)[aw:])
        
        self.wr = Signal(bool(0))
        self.hpxl = Signal(intbv(0, min=0, max=res[0])) # column
        self.vpxl = Signal(intbv(0, min=0, max=res[1])) # row
        self.red = Signal(intbv(0)[width:])
        self.green = Signal(intbv(0)[width:])
        self.blue = Signal(intbv(0)[width:])

        # the memory, if large, eternal required
        # @todo: check the size, if larger than??
        #self.mem = [Signal(intbv(0)[width:]) for _ in range(size)]
        
