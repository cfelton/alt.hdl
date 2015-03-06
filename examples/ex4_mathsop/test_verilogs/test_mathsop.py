
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
import array

import numpy as np
from scipy import signal
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import mlab

from myhdl import *


def _prep_cosim(args, **sigs):
    """ prepare the cosimulation environment
    """
    # compile the verilog files with the verilog simulator
    files = ['../myhdl/mm_sop1.v',
             '../myhdl/mm_sop2.v',
             '../bsv/mkSOP1.v',
             '../bsv/mkSOP2.v',
             '../chisel/generated/mc_sop1.v',
             #'../chisel/generated/mc_sop2.v',
             './tb_mathsop.v',]

    print("compiling ...")
    cmd = "iverilog -o mathsop %s " % (" ".join(files))
    print("  *%s" %  (cmd))
    os.system(cmd)

    # get the handle to the
    print("cosimulation setup ...")
    cmd = "vvp -m ./myhdl.vpi mathsop"

    if not os.path.exists("vcd"):
        os.makedirs("vcd")

    return Cosimulation(cmd, **sigs)


def _create_chirp(args, imax=8):
    """generate a chirp signal, DUT input
    """
    tarray = np.arange(args.Nsamps/2)*(1./args.Fs)
    # chirp(tarray, time zero freq, time end freq, end freq)
    xin = signal.chirp(tarray, 2, tarray[-1], 230,
                       method=u'logarithmic') * .94

    # chirp down and up
    xin = np.concatenate(
        (xin, 
         np.array([-1*ss for ss in reversed(xin[:-1])]),
         -1*xin[:30],
        ))

    xin = map(int, [round(xx*imax) for xx in xin])
    return xin


def test_mathsop_verilogs(args):
    """the SOP (FIR filter) test stimulus
    """
    clock = Signal(bool(0))
    reset = ResetSignal(0, active=0, async=True)

    imin,imax = -2**15, 2**15
    x = Signal(intbv(0, min=imin, max=imax))
    (ym1,ym2,
     yb1,yb2,
     yc1,yc2,) = [Signal(intbv(0, min=imin, max=imax))
                  for _ in range(6)]

    tbdut = _prep_cosim(args, clock=clock, reset=reset,
                        x=x, ym1=ym1, ym2=ym2, 
                        yb1=yb1, yb2=yb2, yc1=yc1, yc2=yc2)

    # create the inputs and output containers
    xhrp = _create_chirp(args,  imax=imax)
    ym1v = array.array('h', [0 for _ in range(args.Nsamps)])
    ym2v = array.array('h', [0 for _ in range(args.Nsamps)])
    yb1v = array.array('h', [0 for _ in range(args.Nsamps)])
    yb2v = array.array('h', [0 for _ in range(args.Nsamps)])
    yc1v = array.array('h', [0 for _ in range(args.Nsamps)])
    yc2v = array.array('h', [0 for _ in range(args.Nsamps)])

    @always(delay(3))
    def tbclk():
        clock.next = not clock
    
    @instance
    def tbstim():
        reset.next = reset.active
        yield delay(33)
        reset.next = not reset.active
        yield clock.posedge
    
        yvals = []
        for ii,xx in enumerate(xhrp):
            if ii < 16:
                print("%08X: x %7d: mm1 %7d,  mm2 %7d,  mb %7d,  mc %7d" % \
                      (now(), x, ym1, ym2, yb1, yc1))

            # set the next input and save all current outputs
            if ii >= args.Nsamps:
                break
            x.next = xx
            ym1v[ii],ym2v[ii] = ym1,ym2
            yb1v[ii],yb2v[ii] = yb1,yb2
            yc1v[ii],yc2v[ii] = yc1,yc2

            yield clock.posedge                                   

        # simulation complete inform the simulator
        raise StopSimulation
        
    print("start (co)simulation ...")
    Simulation((tbdut, tbstim, tbclk,)).run()

    colors = matplotlib.rcParams['axes.color_cycle']
    fig,axl = plt.subplots(7, sharex=True, figsize=(12,7))
    labels = ('input', 'bsv', '*', 'chisel', '**', 'myhdl', '***', )
    xlen = len(xhrp)
    for ax,dd,cc,ll in zip(axl, 
                           (xhrp, 
                            yb1v, yb2v, 
                            yc1v, yc2v,
                            ym1v, ym2v,), 
                           colors[:7], labels):
        ax.plot(dd, color=cc, linewidth=2)
        ax.set_ylim(imin, imax)
        ax.set_xlim(-500, xlen+100)
        ax.text(-450, 0, ll, 
                color='#003366', fontsize=16, fontweight='bold')
        #ax.set_yticklabels([])        

    fig.subplots_adjust(hspace=0)
    for ax in axl:
        ax.set_yticks((imin/2,0,imax/2,))         
        ax.set_yticklabels(('-.5FS', '0', '.5FS',))

    # save the figure
    if not os.path.exists("plots"):
        os.makedirs("plots")

    for ext in ('png','pdf',):
        fig.savefig("plots/mathsop_time_response.%s"%(ext))
    raw_input("continue")


if __name__ == '__main__':
    args = Namespace(
        Nsamps=1024*4, # number of samples to test
        Fs=1e3,        # sample rate
        mmver=1,       # two MyHDL versions
        trace=True     # enable tracing
    )
    test_mathsop_verilogs(args)

