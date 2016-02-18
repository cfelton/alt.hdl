#!/bin/sh
git clone -b mep-114 https://github.com/jandecaluwe/myhdl
cd myhdl
python setup.py install
make -C cosimulation/icarus
# copy the VPI to the test directory
cp cosimulation/icarus/myhdl.vpi ../examples/
cp cosimulation/icarus/myhdl.vpi ../examples/ex1_wprcnt/test_verilogs/
cp cosimulation/icarus/myhdl.vpi ../examples/ex2_mathadds/test_verilogs/
cp cosimulation/icarus/myhdl.vpi ../examples/ex3_zpexgcd/test_verilogs/
cp cosimulation/icarus/myhdl.vpi ../examples/ex4_mathsop/test_verilogs/
cp cosimulation/icarus/myhdl.vpi ../examples/ex5_medfilt/test_verilogs/
cp cosimulation/icarus/myhdl.vpi ../examples/ex6_vgasys/test_verilogs/
