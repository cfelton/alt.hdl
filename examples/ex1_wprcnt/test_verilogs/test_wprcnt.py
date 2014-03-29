
# Need to verify each design is correct, it is easiest 
# to verify each of the converted files (Verilog).  By
# verifying the final result, the design, functionality,
# methodology, etc are all verified.
# 
# Using Python testbenches because Python is a very flexible
# easy language (author knows well).  No need for complicated
# compile (builds) etc.

from __future__ import division
from __future__ import print_function

import os
import argparse
from argparse import Namespace
import math

from myhdl import *

def _prep_cosim(args, **sigs):
    """ prepare the cosimulation environment
    """
    # compile the verilog files with the verilog simulator
    files = ['../myhdl/mm_cnt.v',
             '../bsv/mkCnt.v',
             '../chisel/generated/mc_cnt.v',
             './tb_wprcnt.v',]

    print("compiling ...")
    cmd = "iverilog -o wprcnt %s " % (" ".join(files))
    print("  *%s" %  (cmd))
    os.system(cmd)

    # get the handle to the
    print("cosimulation setup ...")
    cmd = "vvp -m ./myhdl.vpi wprcnt"
    return Cosimulation(cmd, **sigs)


def test_wprcnt(args):
    """
    """
    clock = Signal(bool(0))
    reset = ResetSignal(0, active=0, async=True)
    outb,outc,outm = [Signal(intbv(0, min=0, max=32))
                      for _ in range(3)]

    tbdut =  _prep_cosim(args, clock=clock, reset=reset,
                         outb=outb, outc=outc, outm=outm)

    @always(delay(3))
    def tbclk():
        clock.next = not clock
    
    @instance
    def tbstim():
        reset.next = reset.active
        yield delay(33)
        yield clock.negedge
        reset.next = not reset.active
        yield clock.posedge

        for ii in range(128):
            print("%8d:  mb %2d,  mc %2d,  mm %2d" % \
                  (now(), outb, outc, outm))
            yield clock.posedge

        raise StopSimulation

    print("start (co)simulation ...")
    Simulation((tbdut, tbstim, tbclk,)).run()


if __name__ == '__main__':
    test_wprcnt(Namespace())
