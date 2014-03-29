

module mb_medtop 
(
    input  wire       clock,
    input  wire       reset,
    input  wire [7:0] x,
    input  wire       dvi,
    output wire [7:0] med,
    output wire       dvo
);

   assign dvo = 1'b0;
   
endmodule
