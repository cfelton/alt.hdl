#!/bin/sh
git clone https://github.com/jandecaluwe/myhdl
python myhdl/setup.py install
make -C myhdl/cosimulation/icarus
# copy the VPI to the test directory
cp myhdl/cosimulation/icarus/myhdl.vpi ../../examples/ex1_wprcnt/test_verilogs
cp myhdl/cosimulation/icarus/myhdl.vpi ../../examples/ex2_mathadds/test_verilogs
cp myhdl/cosimulation/icarus/myhdl.vpi ../../examples/ex3_zpexgcd/test_verilogs
cp myhdl/cosimulation/icarus/myhdl.vpi ../../examples/ex4_mathsop/test_verilogs
