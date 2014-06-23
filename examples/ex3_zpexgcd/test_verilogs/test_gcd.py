
from __future__ import division
from __future__ import print_function

import os
import argparse
from argparse import Namespace
from random import randint
import fractions

from myhdl import *

def _prep_cosim(args, **sigs):
    # compile the verilog files with the verilog simulator
    files = ['../myhdl/mm_gcd.v',
             '../bsv/mb_gcd.v',
             '../bsv/mkGCD.v',
             '../chisel/generated/mc_gcd.v',
             './tb_gcd.v',]

    print("compiling ...")
    cmd = "iverilog -o gcd %s " % (" ".join(files))
    print("  *%s" %  (cmd))
    os.system(cmd)

    # get the handle to the
    print("cosimulation setup ...")
    cmd = "vvp -m ./myhdl.vpi gcd"

    if not os.path.exists("vcd"):
        os.makedirs("vcd")

    return Cosimulation(cmd, **sigs)

def test_gcd(args=None):
    clock = Signal(bool(0))
    reset = ResetSignal(0, active=0, async=True)
    a,b = [Signal(intbv(0)[32:]) for _ in range(2)]
    start = Signal(False)
    finished = Signal(True)
    cb,cc,cm = [Signal(intbv(0)[32:])
                for _ in range(3)]

    tbdut =  _prep_cosim(args, 
                         clock=clock,
                         reset=reset,
                         a=a, b=b,
                         cb=cb, cc=cc, cm=cm,
                         start=start, finished=finished)

    @always(delay(3))
    def tbclk():
        clock.next = not clock
    
    @instance
    def tbstim():
        reset.next = reset.active
        yield delay(33)
        reset.next = not reset.active
        yield clock.posedge

        for ii in range(args.N):
            a.next = randint(0, 2**26-1) # 2**32-1
            b.next = randint(0, 2**26-1) # 2**32-1
            start.next = True
            yield clock.posedge
            start.next = False
            yield clock.posedge
            waitcnt = 0
            #print(a,b)
            while not finished:                
                er = fractions.gcd(a,b)
                yield clock.posedge            
                waitcnt += 1
                if waitcnt > 100000:
                    raise StandardError, "Timeout something happened"
            print("%8d:  [%8d, %8d], mb %5d,  mc %5d,  mm %5d [%d]" % \
                  (now(), a, b, cb, cc, cm, er))
            assert cm == er
            assert cb == er
            assert cc == er
            yield delay(100)
            yield clock.posedge                

        raise StopSimulation

    print("start (co)simulation ...")
    Simulation((tbdut, tbstim, tbclk,)).run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', type=int, default=100,
                        help="number of loops to test")
    args = parser.parse_args()
    test_gcd(args)
