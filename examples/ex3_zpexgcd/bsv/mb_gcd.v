

module mb_gcd
(
    input  wire clock,
    input  wire reset,
    input  wire [31:0] a,
    input  wire [31:0] b,
    output wire [ 31:0] c,
    input  wire start,
    output wire finished    
 );
   
  mkGCD M1(
	   .CLK(clock),
	   .RST_N(reset),
	   .start_a(a),
	   .start_b(b),
	   .EN_start(start),
	   .RDY_start(),
	   .result(c),
	   .RDY_result(finished));   
endmodule  
