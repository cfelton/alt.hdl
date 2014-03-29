
`timescale 1ns/1ps
`default_nettype none

module tb_vgasys;

   // to the duts
   reg clock, reset;
   reg vselect;   
   // from the duts
   wire mm_hsync, mm_vsync;
   wire mm_pxlen, mm_active;
   wire [9:0] mm_red, mm_blue, mm_green;     
	
   initial begin
      $dumpfile("vcd/_tb_vgasys.vcd");
      $dumpvars(0, tb_vgasys);	
   end

   initial begin
      $from_myhdl(clock, reset, vselect);
      $to_myhdl
	(
	 mm_hsync, mm_vsync,
	 mm_red, mm_green, mm_blue,
	 mm_pxlen, mm_active
	 );      
   end

   mm_vgasys dut_myhdl
     (.clock(clock),
      .reset(reset),
      .vselect(vselect),
      .hsync(mm_hsync),
      .vsync(mm_vsync),
      .red(mm_red),
      .green(mm_green),
      .blue(mm_blue),
      .pxlen(mm_pxlen),
      .active(mm_active));
   		           

endmodule
