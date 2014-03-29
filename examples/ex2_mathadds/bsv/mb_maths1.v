
/**
 * BSV has some powerful interface techniques
 * but reducing it to an actual (HW) set of signals
 * is not straightfoward (don't know how).  Here we
 * need to create a wrapper to match the hardware 
 * requirement to the BSV generated modules.
 */
module mb_maths1
(
  input  wire clock,
  input  wire reset,
  input  wire signed [15:0] x,
  input  wire signed [15:0] y,
  output wire signed [15:0] v
);

   wire eni;  // enable inputs
   wire dvi;  // inputs valid   
   wire dvo;  // left hanging
   
   assign eni = 1'b1;
   assign dvi = 1'b1;

   // instantiate the module created with BSV
   mkMaths1 
     #(.m_val(10)) 
   M1(
      .CLK(clock),  
      .RST_N(reset),    // wrong reset structure for FPGA!
      .update_x(x),
      .update_y(y),
      .EN_update(eni),
      //.RDY_update(dvi),
      .update(v),         // "v" output
      .RDY_update(dvo)
      );
   

endmodule  
