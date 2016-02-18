
# Need to verify each design is correct, it is easiest 
# to verify each of the converted files (Verilog).  By
# verifying the final result, the design, functionality,
# methodology, etc are all verified.
# 
# Using Python testbenches because Python is a very flexible
# easy language (author knows well).  No need for complicated
# compile (builds) etc.

from __future__ import print_function, division

import os
import argparse
from argparse import Namespace
import math

from myhdl import *


def _prep_cosim(args, **sigs):
    """ prepare the cosimulation environment
    """
    # compile the verilog files with the verilog simulator,
    # file paths relative to the ex2_mathadds
    files = ['myhdl/mm_maths1.v',
             'bsv/mb_maths1.v',
             'bsv/mkMaths1.v',
             'chisel/generated/mc_maths1.v',
             'test_verilogs/tb_mathadds.v',]

    for ii, ff in enumerate(files):
        files[ii] = os.path.join(args.expath, 'ex2_mathadds', ff)
        
    print("compiling ...")
    cmd = "iverilog -o mathadds %s " % (" ".join(files))
    print("  *%s" %  (cmd))
    os.system(cmd)

    # get the handle to the
    print("cosimulation setup ...")
    cmd = "vvp -m ./myhdl.vpi mathadds"

    if not os.path.exists("vcd"):
        os.makedirs("vcd")

    return Cosimulation(cmd, **sigs)


def test_mathadds(expath, args=None):
    """
    The maths1 was a simple two input (x,y) and a single
    output (v).  The verilog modules should look something
    like
        module m_maths1(input x, input y, output v)

    The type/size of the inputs and outputs was defined at
    the conversion, 16 bit inputs and 
    """
    if args is None:
        args = Namespace()
    args.expath = expath
    
    clock = Signal(bool(0))
    reset = ResetSignal(0, active=0, async=True)
    imin,imax = -2**15, 2**15
    x = Signal(intbv(0, min=imin, max=imax))
    y = Signal(intbv(0, min=imin, max=imax))
    vm,vb,vc = [Signal(intbv(0, min=imin, max=imax))
                for _ in range(3)]

    tbdut =  _prep_cosim(args, x=x, y=y,
                         vm=vm, vb=vb, vc=vc)

    @always(delay(3))
    def tbclk():
        clock.next = not clock
    
    @instance
    def tbstim():
        reset.next = reset.active
        yield delay(33)
        reset.next = not reset.active
        yield clock.posedge

        for valpairs in zip((1,543,-7,31000),(1,-13,2,32001)):
            x.next, y.next = valpairs
            er = sum(valpairs)*10
            for ii in range(4):                
                print("%8d:  [%8d, %8d] mb %5d,  mc %5d,  mm %5d [%d]" % \
                      (now(), x, y, vb, vc, vm, er))
                yield delay(1) 

        raise StopSimulation

    print("start (co)simulation ...")
    Simulation((tbdut, tbstim, tbclk,)).run()


if __name__ == '__main__':
    test_mathadds(expath='../..')
