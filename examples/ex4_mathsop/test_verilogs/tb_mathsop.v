

`timescale 1ns/10ps

module tb_mathsop;

   reg clock, reset;
   reg [15:0] x;
   wire [15:0] ym1, ym2, yb1, yb2, yc1, yc2;
   
   initial begin
      $dumpfile("vcd/mathsop.vcd");
      $dumpvars(0, tb_mathsop);
   end
   
   initial begin
      $from_myhdl(clock, reset, x);
      $to_myhdl(ym1, ym2, yb1, yb2, yc1, yc2);
   end
   
   /** the myhdl verilog */   
   mm_sop1 dut_myhdl1(.clock(clock), .reset(reset),
		      .x(x), .y(ym1));
   mm_sop2 dut_myhdl2(.clock(clock), .reset(reset),
		      .x(x), .y(ym2));
   
   /** the bluespec verilog (wrapper) */
   mkSOP1 dut_bsv1(.CLK(clock), .RST_N(reset), 
                   .write_x(x), .read(yb1));
   
   mkSOP2 dut_bsv2(.CLK(clock), .RST_N(reset), 
                   .write_x(x), .read(yb2));

   /** the chisel verilog */
   // chisel use active high reset
   wire mc_reset = ~reset;   
   mc_sop1 dut_chisel1(.clk(clock), .reset(mc_reset),
                       .io_x(x), .io_y(yc1));

   //mc_sop2 dut_chisel2(.clk(clock), .reset(mc_reset),
   //                    .io_x(x), .io_y(yc1));
   
endmodule
