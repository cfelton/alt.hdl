

from __future__ import division
from __future__ import print_function

import sys
import os
import argparse
from array import array
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
    """ compute the median of the list/array x
    This sort is the sort network used in the HDL 
    implementations
    """
    N = len(x)
    t = [0 for _ in range(N)]
    z = copy(x)

    for stage in range(N):
        k = 0 if (stage%2) else 1
        for ii in range(k, N-1, 2):
            t[ii] = min(z[ii], z[ii+1])
            t[ii+1] = max(z[ii], z[ii+1])
            z[ii] = t[ii];
            z[ii+1] = t[ii+1]

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

                    yield clock.posedge
            except Exception,err:
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

