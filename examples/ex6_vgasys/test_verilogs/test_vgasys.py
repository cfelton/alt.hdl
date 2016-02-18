
from __future__ import division
from __future__ import print_function

# @todo: need a better way to do this
import sys
sys.path.append('../myhdl')

import os
import argparse
from argparse import Namespace
from array import array

import myhdl
from myhdl import *

# resuse some of the interfaces
from vga_intf import Clock
from vga_intf import Reset
from vga_intf import System
from vga_intf import VGA
from vga_sync import m_vga_sync

# a video display model to check the timings
from model_video_display import VideoDisplay

def _prep_cosim(
    args, 
    clock=None, reset=None, vselect=None,
    bvga=None, cvga=None, mvga=None
    ):
    """
    """
    # compile the verilog files with the verilog simulator
    files = ['myhdl/mm_vgasys.v',
             'test_verilogs/tb_vgasys.v']

    for ii, ff in enumerate(files):
        files[ii] = os.path.join(args.expath, 'ex6_vgasys', ff)
        assert os.path.isfile(files[ii]), "missing file {}".format(files[ii])
        
    print("compiling ...")
    cmd = "iverilog -o vgasys %s " % (" ".join(files))
    os.system(cmd)

    if not os.path.exists("vcd"):
        os.makedirs("vcd")

    print("cosimulation setup ...")
    cmd = "vvp -m ./myhdl.vpi vgasys"
    gcosim = Cosimulation(cmd,
        clock=clock, reset=reset, vselect=vselect,
        # bsv dut signals
        # chisel dut signals
        # myhdl dut signals
        mm_hsync=mvga.hsync, mm_vsync=mvga.vsync,
        mm_red=mvga.red, mm_green=mvga.green, mm_blue=mvga.blue,
        mm_pxlen=mvga.pxlen, mm_active=mvga.active
    )

    return gcosim
    

def test_vgasys(expath, args=None):
    if args is None:
        args = Namespace(trace=False)
    args.expath = expath
    
    # @note: these have to stay fixed, the alt.hdl are converted
    #        to verilog in a separate step.  Each conversion 
    #        would need to be udpated to match the following.
    res = (640, 480,)  
    line_rate = int(31250)

    clock = Clock(0, frequency=50e6)
    reset = Reset(0, active=0, async=False)
    vselect = Signal(bool(0))

    bvga = VGA(color_depth=(10,10,10), )
    cvga = VGA(color_depth=(10,10,10), )
    mvga = VGA(color_depth=(10,10,10), )
    
    # prepare and start the cosimulation with the Verilogs
    tbdut = _prep_cosim(args, 
                        clock, reset, vselect,
                        bvga, cvga, mvga)

    @myhdl.module
    def bench():

        # group global signals
        dsys = System(clock=clock, reset=reset)
        # a display for each dut
        bvd = VideoDisplay(frequency=clock.frequency,
                           resolution=res,
                           line_rate=line_rate)
        
        cvd = VideoDisplay(frequency=clock.frequency,
                           resolution=res,
                           line_rate=line_rate)
        
        mvd = VideoDisplay(frequency=clock.frequency,
                           resolution=res,
                           line_rate=line_rate)

        # 
        tbclk = clock.gen()

        # video display model connected to the VGA signals
        # of each language design.
        tbvd = []
        for vd, vga in zip((bvd, cvd, mvd,),
                           (bvga, cvga, mvga,)):
            tbvd.append(vd.process(dsys, vga))

        @instance
        def tbstim():
            reset.next = reset.active
            yield delay(18)
            reset.next = not reset.active

            # Wait till a full screen has been updated
            while mvd.update_cnt < 1:
                 yield delay(10000)

            raise StopSimulation

        return tbclk, tbvd, tbstim


    if os.path.isfile('vcd/_test.vcd'):
        os.remove('vcd/_test.vcd')

    g = bench()
    if args.trace:
        traceSignals.timescale = '1ns'
        traceSignals.name = 'vcd/test_vgasys'
        g = traceSignals(g)
        
    Simulation((g, tbdut,)).run()


if __name__ == '__main__':
    test_vgasys(expath='../..')
