
`timescale 1ns/10ps

module tb_maths1;

reg  [15:0] x;
reg  [15:0] y;
wire [15:0] vm, vb, vc;

initial begin
    $dumpfile("vcd/maths1.vcd");
    $dumpvars(0, tb_maths1);
end

initial begin
    $from_myhdl(
        x,
        y
    );
    $to_myhdl(
        vm,
        vb,
        vc
    );
end

/** the myhdl verilog */   
mm_maths1 dut_myhdl(x, y, vm);

/** the bluespec verilog */
wire clock, reset;
mb_maths1 dut_bsv(clock, reset, x, y, vb);
	  
/** the chisel verilog */  
mc_maths1 dut_chisel(x, y, vc);
   
endmodule
