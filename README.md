
[![Build Status](https://travis-ci.org/cfelton/alt.hdl.svg)](https://travis-ci.org/cfelton/alt.hdl)

Alternative Hardware Description Languages
===========================================
This repository includes the examples used in the
[EELive 2014 Hardware Design and the Grunge Era](http://my.presentations.techweb.com/events/eelive/san-jose/2014/esc) 
presentation.  In each example directory is a directory for 
each alt.hdl: 
[bsv (bluespec)](http://www.bluespec.com/high-level-synthesis-tools.html), 
[chisel](https://chisel.eecs.berkeley.edu/), 
[myhdl](http://www.myhdl.org), 
and a *test_verilogs* directories.  The source for 
each language is in the respective directories.  The *test_verilogs* 
is a test environment to verify each of the generated Verilogs, 
this way each implementation can be verified via a single 
test environment.  

This repository contains two groups of examples: 
**complete** are the examples used in the presentation and are
fully finished and working examples.  The second set of 
examples are slightly larger examples not included
in the presentation and (as last writing) are **incomplete**
(since they were not used, less motivation to complete them :)

    Complete Examples (used in the presentation)
       ex1_wprcnt   : a silly counter
       ex2_mathadds : add and scale
       ex3_zpexgcd  : greatest common denominator
       ex4_mathsop  : sum-of-products (a.k.a FIR filter), non-optimized
       
    Incomplete Examples (not used in the presentation)
       ex5_medfilt : median filter, often used in image processing
       ex6_vgasys  : VGA driver
       ex7_mathsys : a more complicated math system
       ex8_uart    : UART bus driver

These examples are intended to be small digestible examples
that are used to introduce the different alt.hdls.  The 
examples are:

*  **Not** a tutorial.  These examples are not intended to 
   be a tutorial.  Each subsequent example might be slightly 
   more complex but not in the fashion that would make them
   useful for a tutorial.

*  **Not** a base for comparison.  Although some minor 
   comparisons were made in the presentation the goal of
   the presentation was simply to introduce the three 
   alt.hdls.  These examples are not exhaustive
   to be considered as a source for language comparison.  For 
   instance, the examples do not include a traditional 
   state-machine design.

Synthesis Results
------------------
Some of the examples provide synthesis results for each of 
alt.hdl examples.  No timing constaints were used - let the
tool determine *Fmax*.  Two FPGAs were targetted: Altera 
Cyclone II EP2C35 and a Xilinx Spartan6 XC6SLX25.  The 
results are not useful for comparing devices!  The results 
include resource utilization and maximum clock frequency.

  
Complete Examples 
===================
The following four are complete examples used in the 
presentation. 

A Useless Counter (ex1\_wprcnt)
-------------------------------
This example was mentioned briefly in the presentation.  It
is a counter that counts up to 31 and then toggles between
31 and 30.

Example source [bsv](https://github.com/cfelton/alt.hdl/blob/master/examples/ex1_wprcnt/bsv/useless_counter.bsv), 
[chisel](https://github.com/cfelton/alt.hdl/blob/master/examples/ex1_wprcnt/chisel/useless_counter.scala), 
and [myhdl](https://github.com/cfelton/alt.hdl/blob/master/examples/ex1_wprcnt/myhdl/useless_counter.py).


Add and Scale (ex2\_mathadds)
-----------------------------
This is a simple system that takes two inputs adds them
and then multiplies by a constant (constant is parameterizable).

    v[n] = (x[n] + y[n]) * M

This is a non-registered version.  A register version 
is used in the *ex7\_mathsys* example.  Also note, this example
does not handle overflow (the tests show the overflow).

Example source [bsv](https://github.com/cfelton/alt.hdl/blob/master/examples/ex2_mathadds/bsv/maths1.bsv), 
[chisel](https://github.com/cfelton/alt.hdl/blob/master/examples/ex2_mathadds/chisel/maths1.scala), 
and [myhdl](https://github.com/cfelton/alt.hdl/blob/master/examples/ex2_mathadds/myhdl/maths1.py).


Greatest Common Denominator (ex3\_zpexgcd)
------------------------------------------
Computes the greatest common denominator.  Two of the three
alt.hdls provided this as an example - I was compelled to 
include it in the presentation.

Example source [bsv](https://github.com/cfelton/alt.hdl/blob/master/examples/ex3_zpexgcd/bsv/gcd.bsv), 
[chisel](https://github.com/cfelton/alt.hdl/blob/master/examples/ex3_zpexgcd/chisel/gcd.scala), 
and [myhdl](https://github.com/cfelton/alt.hdl/blob/master/examples/ex3_zpexgcd/myhdl/gcd.py).

### Synthesis Results
![ZPEXGCD Synthesis]
(https://cloud.githubusercontent.com/assets/766391/4039716/c3261f72-2cd1-11e4-855f-fecb46870a88.png)

Comment on the synthesis results, the implementations are not identical, 
the myhdl version has an extra register stage on the ouptut, in such a 
small example this makes a difference.  The myhdl version can be modified
(e.g. remove the registered outputs) and the resource usage will be 
indetical for all three.


Math SOP (ex4\_mathsop)
-----------------------
This is a basic sum-of-products (SOP) example and is implemented as a 
*finite impulse response* (FIR) filter.  The operation is a simple SOP 
but when you combine the usage of the sliding window of the input signal 
with a set of coefficients it becomes a FIR filter.

This is an overused data-path example - why in the world did
I include it?  Couple reasons: it is useful to highlight
some of the language features and it is enjoyable to look at the
output waveforms (not the binary signals but the filtered
digital signals).

This example does not architecturally optimize the SOP for
a given design.  Example, often the clock rate is higher than
the sample rate and a single multiplier can be shared 
(time-multiplexed) in the SOP calculation.  The description
in this example would rarely (if ever) be used for an actual 
FIR filter in an FPGA or ASIC but is useful as as a starting 
point and digestable example.

Example source 
[bsv](https://github.com/cfelton/alt.hdl/blob/master/examples/ex4_mathsop/bsv/sop1.bsv), 
[chisel](https://github.com/cfelton/alt.hdl/blob/master/examples/ex4_mathsop/chisel/sop1.scala), 
and [myhdl](https://github.com/cfelton/alt.hdl/blob/master/examples/ex4_mathsop/myhdl/sop1.py).

### Synthesis Results
![MATHSOP Synthesis]
(https://cloud.githubusercontent.com/assets/766391/4039305/b3c8844c-2cc8-11e4-925f-ac6d2b667c9c.png)


Incomplete Examples
===================
The following are larger examples that I wanted to make 
available.  It shows features of the languages that are 
difficult to show with the small examples (but difficult
to present).  Since these examples were not targeted 
for the presentation they are a WIP, I am completing them
in my leisure (which means they will probably never be 
completed).  Feel free to create a pull-request with 
updated/completed versions.  


Median Filter (ex5\_medfilt)
----------------------------
Another filter example (give me a break) but this one is 
slightly different.  The median calculation involves a **sort**.
Given a list/array/vector of values sort and find the middle.
In image processing a median filter is often used to remove *noise*
from and image ([various examples via google](https://www.google.com/search?espv=210&es_sm=122&tbm=isch&q=image+processing+median+filter&oq=image+processing+median+filter&gs_l=img.3..0i24.6606.8763.0.8954.17.16.0.0.0.2.141.1083.12j4.16.0....0...1c.1.38.img..15.2.228.0fybRBHYu2k&bav=on.2,or.r_cp.r_qf.&bvm=bv.63808443,d.aWc,pv.xjs.s.en_US.9CjFb4DKbRI.O&biw=1217&bih=1434&dpr=1#pws=0&q=image+processing+median+filter&tbm=isch)).

*(following links not active - yet)*
Median example source [bsv](), [chisel](), and [myhdl]().
Median filter example source [bsv](), [chisel](), and [myhdl]().

[Here](http://www.fpgarelated.com/showarticle/578.php) is a 
write-up describing the median calculation implementation.

VGA system (ex6\_vgasys)
------------------------
This example is a straightforward VGA system, although VGA is
not as useful these days - it is readily available on many 
development boards and it is a self contained medium size 
example and explores some different aspects of a complex 
digital system.  The *vgasys* has two main components:

 1. video color bar generator
 2. video sync (drives the VGA signals with the 
    correct timing relationships)

Although this system only has the two components it is intended 
to support a generic video system ([outlined here]()) with video
memory and video generator as described in the 
[example description]().

*(following links not active - yet)*
Example source [bsv](), [chisel](), and [myhdl]().

Math System (ex7\_mathsys)
---------------------------
This system is some what nonsensical but it lets us build off
the previous and explore different aspects of the languages.  
The system will be defined as:

    z[n] = (v[n] * F{y[n] + x[n]}) + H{v[n]} + v[n-D]

where *H* is the *mathsop* (FIR filter) and *F* is
another system described in the [example description]().

*(following links not active - yet)*
Example source [bsv](), [chisel](), and [myhdl]().


Contributing
=============
It is difficult (impossible?) to be an expert in every language.
Majority of my past experience is with Verilog and VHDL but I have been
using MyHDL for a considerable amount of time and consequently use V\* 
less and less (I am reminded often how much VHDL I have forgotten, 
lack of use).  

If you have suggestions for improvements or version for the incomplete
code leave a comment or generate a pull-request.  If you provide an
example for one of the incomplete examples make sure the test completes
successfully.  To run the tests:

1.  Convert the example to Verilog
2.  Run the test\_verilogs test:

    >> python test\_<example>

Each completed example has a test and has verified the 
generated Verilog.  Each incomplete example has Verilog stubs and 
tests.  The incomplete examples tests can be run and indicate the
non-implemented tests fail.

Note, for the first four examples I probably will not make many
changes since these were the versions used in the presentation.
Also, because of different constraints I realize some language 
features were not used in the first four examples.

