

`timescale 1ns/10ps

module tb_gcd;

   reg clock, reset;
   reg [31:0] a,b;
   wire [31:0] cb, cc, cm;
   reg 	       start;
   wire        finished;
   wire        fb, fc, fm;

   assign finished = fb & fc & fm;   
   
   initial begin
      $dumpfile("vcd/gcd.vcd");
      $dumpvars(0, tb_gcd);
   end
   
   initial begin
      $from_myhdl(clock, reset, a, b, start);
      $to_myhdl(cb, cc, cm, finished);
   end
   
   /** the myhdl verilog */   
   mm_gcd dut_myhdl(.clock(clock), .reset(reset),
		    .a(a), .b(b), .c(cm),
		    .start(start), .finished(fm));
   
   /** the bsv verilog (wrapper) */
   mb_gcd dut_bsv(.clock(clock), .reset(reset), 
                  .a(a), .b(b), .c(cb),
		  .start(start), .finished(fb));
   
   /** the chisel verilog */
   // chisel use active high reset
   wire mc_reset = ~reset;   
   mc_gcd dut_chisel(.clk(clock), //.reset(mc_reset),
                     .io_a(a), .io_b(b), .io_c(cc),
		     .io_start(start), .io_finished(fc));
   
endmodule
