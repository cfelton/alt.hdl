
`timescale 1ns/10ps

module tb_wprcnt;

   reg  clock;
   reg 	reset;
   wire [4:0] outb, outc, outm;
   
   initial begin
      $dumpfile("vcd/wprcnt.vcd");
      $dumpvars(0, tb_wprcnt);
   end
   
   initial begin
      $from_myhdl(
		  clock,
		  reset
		  );
      $to_myhdl(
		outb,
		outc,
		outm
		);
   end
   
   /** the bluespec verilog */
   mkCnt dut_bsv(.CLK(clock), .RST_N(reset), .out(outb));
   
   /** the chisel verilog */
   wire mc_reset = ~reset;   
   mc_cnt dut_chisel(.clk(clock), .reset(mc_reset), .io_out(outc));
   
   /** the myhdl verilog */   
   mm_cnt dut_myhdl(.clock(clock), .reset(reset), .out(outm));

   
endmodule
