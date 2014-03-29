
`timescale 1ns/10ps

module tb_median;

   reg clock, reset;
   reg [7:0] x;
   reg 	     dvi;
   
   wire [7:0] mbmed, mcmed, mmmed;   
   wire mbdvo, mcdvo, mmdvo;   
   wire finished;

   assign finished = mbdvo & mcdvo & mmdvo;

   initial begin
      $dumpfile("vcd/tb_median.vcd");
      $dumpvars(0, tb_median);
   end

   initial begin
      $from_myhdl(clock, reset, x, dvi);
      $to_myhdl(mbmed, mbdvo, mcmed, mcdvo, mmmed, mmdvo, finished);
   end

   /** the bsv verilog */
   mc_medtop dut_bsv(.clk(clock), //.reset(mc_reset),
			.x(x), .dvi(dvi), .med(mbmed), .dvo(mbdvo) );
   
   /** the chisel verilog */
   wire mc_reset = ~reset;
   mc_medtop dut_chisel(.clk(clock), //.reset(mc_reset),
			.x(x), .dvi(dvi), .med(mcmed), .dvo(mcdvo) );
   
   /** the myhdl verilog */
   mm_medtop dut_myhdl(.clock(clock), .reset(reset),
		       .x(x), .dvi(dvi), .med(mmmed), .dvo(mmdvo) );

endmodule
   

   
    
