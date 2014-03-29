This repository includes the examples used in the
[EELive 2014 Hardware Design and the Grunge Era](http://www.eeliveshow.com/sanjose/schedule-builder/session-id/827205) 
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
fully finished and working examples.  The second, set of 
examples are slightly larger examples but were not included
in the presentation and (as last writing) are **incomplete**
(since they were not used, less motivation to complete them :)

    Complete Examples (used in the presentation)
       ex1_wprcnt
       ex2_mathadds
       ex3_zpexgcd
       ex4_mathsop
       
    Incomplete Examples (not used in the presentation)
       ex5_medfilt
       ex6_vgasys	    
       ex7_mathsys

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

  
Complete Examples 
===================
The following four are complete examples used in the 
presentation. 

A Useless Counter (ex1\_wprcnt)
-------------------------------
This example was mentioned briefly in the presentation.  It
is a counter that counts up to 31 and then toggles between
31 and 30.

Example source [bsv](), [chisel](), and [myhdl]().


Add and Scale (ex2\_mathadds)
-----------------------------
This is a simple system that takes two inputs adds them
and then multiplies by a constant (constant is parameterizable).

    v[n] = (x[n] + y[n]) * M

This is a non-registered version.  A register version 
is used in the *ex7\_mathsys* example.

Example source [bsv](), [chisel](), and [myhdl]().


Greatest Common Denominator (ex3\_zpexgcd)
------------------------------------------
Computes the greatest common denominator.  Two of the three
alt.hdls provided this as an example - I was compelled to 
include it in the presentation.

Example source [bsv](), [chisel](), and [myhdl]().


Math SOP (ex4\_mathsop)
-----------------------
This is a basic sum-of-products (SOP) also known as a *finite impulse
response* (FIR) filter.  The operation is a simple SOP but when you
combine the usage of the sliding window of the input signal with
a set of coefficients it becomes a FIR filter.

This is an overused data-path example - why in the world did
I include it?  Couple reasons: it is useful to highlight
some of the language features and it is enjoyable to look at the
output waveforms (not the binary signals but the filtered
digital signals).

This example does not architecturally optimize the SOP for
a given design.  Example, often the clock rate is higher than
the sample rate and a single multiplier can be shared 
(time-multiplexed) in the SOP calculation.

Example source [bsv](), [chisel](), and [myhdl]().


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
Another filter example - give me a break.  Well this one is 
slightly different.  The median calculation involves a **sort**!.
Given a list/array/vector of values sort and find the middle.
In image processing a median filter is often used to remove *noise*
from and image ([millions of examples via google](https://www.google.com/search?espv=210&es_sm=122&tbm=isch&q=image+processing+median+filter&oq=image+processing+median+filter&gs_l=img.3..0i24.6606.8763.0.8954.17.16.0.0.0.2.141.1083.12j4.16.0....0...1c.1.38.img..15.2.228.0fybRBHYu2k&bav=on.2,or.r_cp.r_qf.&bvm=bv.63808443,d.aWc,pv.xjs.s.en_US.9CjFb4DKbRI.O&biw=1217&bih=1434&dpr=1#pws=0&q=image+processing+median+filter&tbm=isch)).

Median example source [bsv](), [chisel](), and [myhdl]().

Median filter example source [bsv](), [chisel](), and [myhdl]().


VGA system (ex6\_vgasys)
------------------------
This example is a straightforward VGA system, although VGA is
not as useful - it is readily available on many development 
boards and it is a self contained medium size example and explores
some different aspects of a system.  The *vgasys* has two 
main components:

 1. video color bar generator
 2. video sync (drives the VGA signals with the 
    correct timing relationships)

Although this system only has the two components it is intended 
to support a generic video system ([outlined here]()) with video
memory and video generator as described in the 
[example description]().

Example source [bsv](), [chisel](), and [myhdl]().

Math System (ex7\_mathsys)
---------------------------
This system is some what nonsensical but it lets us build off
the previous and explore different aspects.  The system will be
defined as:

    z[n] = w[n] + v[n-D] + H1{v[n]} + F{x[n] + y[n]} * H2{v[n]}

where *H1* and *H2* are the *mathsop* (FIR filters) and *F* is
another system described in the [example description]().

Example source [bsv](), [chisel](), and [myhdl]().


Contributing
=============
It is difficult (impossible?) to be an expert in every language.
My goal is not to be a language expert but to successfully use the
tools to build my designs.
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

Each completed example has a test and each example has verified the 
generated Verilog.  Each incomplete example has Verilog stubs and 
tests.  The incomplete examples tests can be run and indicate the
non-implemented tests fail.

Note, for the first four examples I probably will not make many
changes since these were the versions used in the presentation.
Because of different constraints I realize some language features
were not used in the first four examples.

