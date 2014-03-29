
from myhdl import *

from vga_intf import Clock
from vga_intf import Reset
from vga_intf import System
from vga_intf import VGA
from vga_intf import VideoMemory

from vga_sync import m_vga_sync
from vga_color_bars import m_color_bars

def mm_vgasys(

    # ~~~[PORTS]~~~
    clock,  reset, vselect,
    hsync, vsync, 
    red, green, blue,
    pxlen, active,

    # ~~~~[PARAMETERS]~~~~
    resolution=(640,480,),
    color_depth=(10,10,10,),
    refresh_rate=60,
    line_rate=31250
    ):
    
    # create the system-level signals, overwrite clock, reset
    dsys = System(clock=clock, reset=reset)
    # VGA inteface
    vga = VGA(hsync=hsync, vsync=vsync, 
              red=red, green=green, blue=blue,
              pxlen=pxlen, active=active)
    # video memory interface
    vmem = VideoMemory()
        
    # instances of modules
    gbar = m_color_bars(dsys, vmem, 
                        resolution=resolution)

    gvga = m_vga_sync(dsys, vga, vmem,
                      resolution=resolution)


    return gvga, gbar


def convert(color_depth=(10,10,10,)):
    """ convert the vgasys to verilog
    """
    clock = Clock(0, frequency=50e6)
    reset = Reset(0, active=0, async=False)
    vselect = Signal(bool(0))

    hsync = Signal(bool(0))
    vsync = Signal(bool(0))
    cd = color_depth
    red = Signal(intbv(0)[cd[0]:])
    green = Signal(intbv(0)[cd[1]:])
    blue = Signal(intbv(0)[cd[2]:])
    pxlen = Signal(bool(0))
    active = Signal(bool(0))

    toVerilog.timescale = '1ns/1ns'
    toVerilog(mm_vgasys, clock, reset, vselect,
              hsync, vsync, red, green, blue,
              pxlen, active)


if __name__ == '__main__':
    # @todo: add command line arguments for the different 
    #        settings, resolution, width, etc.
    convert()
    