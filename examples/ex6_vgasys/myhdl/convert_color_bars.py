
import os
import argparse

from myhdl import *
from vga_intf import *
from vga_color_bars import m_color_bars

def convert(args):
    dsys = System(frequency=50e6)
    vmem = VideoMemory()
    
    toVerilog(m_color_bars, dsys, vmem, 
              resolution=args.res, width=args.width)

    #toVHDL(m_color_bars, dsys, vmem, 
    #       resolution=args.res, width=args.width)

def get_cli_args():
    parser = argparse.ArgumentParser(description="Convert colobar generator")
    parser.add_argument('--resolution', default="640,480", type=str,
                        help="define the resolution, horizontal,veritical")
    parser.add_argument('--width', default=8, type=int,
                        help="define the pixel width in bits")

    args = parser.parse_args()

    res = args.resolution.replace(' ', '')
    args.res = tuple(map(int, res.split(',')))

    return args

if __name__ == '__main__':
    args = get_cli_args()
    convert(args)
            