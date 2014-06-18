

from __future__ import division
from __future__ import print_function

import sys
import os
import argparse
from copy import copy
from random import randint

from myhdl import *


def _prep_cosim(args, **sigs):
    """
    """

    files = ['../bsv/mb_medtop.v',
             '../chisel/generated/mc_medtop.v',
             '../myhdl/mm_medtop.v',
             'tb_median.v']

    print("compiling ...")
    cmd = "iverilog -o medtop %s " % (" ".join(files))
    os.system(cmd)

    print("cosimulation setup ...")
    cmd = "vvp -m ./myhdl.vpi medtop"
    gcosim = Cosimulation(cmd, **sigs)

    return gcosim


def median(x):
    """ compute the meidan of the list/array x
    This sort is the sort network used in the HDL
    """
    N = len(x)
    def compare_stage(z, stage, N):
        t,k = copy(z), 0 if (stage%2) else 1        
        for ii,zd in range(k ,N-1, 2):
            t[ii] = min(zd, z[ii+1])
            t[ii+1] = max(zd, z[ii+1])
        return t

    z = x
    for stage in range(N):
        z = compare_stage(z, stage, N)

    return z[N//2], z
            

def test_median(args):
    N = args.N

    clock = Signal(bool(0))
    reset = ResetSignal(0, active=1, async=False)
    win = [Signal(intbv(0)[8:]) for _ in range(N)]
    x = Signal(intbv(0)[8:])
    dvi = Signal(bool(0))
    mbmed = Signal(intbv(0)[8:])  # median from bsv
    mbdvo = Signal(bool(0))
    mcmed = Signal(intbv(0)[8:])  # median from chisel
    mcdvo = Signal(bool(0))
    mmmed = Signal(intbv(0)[8:])  # median from myhdl
    mmdvo = Signal(bool(0))

    finished = Signal(bool(0))

    tbdut = _prep_cosim(args, 
                        clock=clock, reset=reset,
                        x=x, dvi=dvi, 
                        mbmed=mbmed, mbdvo=mbdvo, 
                        mcmed=mcmed, mcdvo=mcdvo, 
                        mmmed=mmmed, mmdvo=mmdvo,
                        finished=finished)
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

            try:
                for ii in range(args.Nloops):
                    twin = [randint(0, 255) for _ in range(N)]
                    
                    for xx in twin:
                        x.next = xx
                        dvi.next = True
                        yield clock.posedge
                    dvi.next = False
                    
                    while not (mbdvo or mcdvo or mmdvo):
                        yield clock.posedge

                    # valid ouptut
                    fmed,w = median(twin)
                    emed = sorted(twin)[N//2]
                    print("%8d: [%5d, %5d] mb %5d,  mc %5d,  mm %5d" % \
                          (now(), emed, fmed, mbmed, mcmed, mmmed))
                    assert emed == fmed, "reference function failed"
                    assert emed == mmmed, "myhdl invalid median"
                    yield clock.posedge
            except Exception,err:
                print("** simulation ERROR **")
                yield delay(100)
                print(err)
                raise err

            raise StopSimulation

        return tbdut, tbclk, tbstim

    traceSignals.name = 'vcd/_test'
    if os.path.isfile(traceSignals.name+'.vcd'):
        os.remove(traceSignals.name+'.vcd')
    Simulation(traceSignals(_test)).run()


if __name__ == '__main__':
    args = argparse.Namespace(N=9, Nloops=27)
    test_median(args)

