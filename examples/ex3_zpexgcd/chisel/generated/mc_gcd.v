module mc_gcd(input clk,
    input [31:0] io_a,
    input [31:0] io_b,
    input  io_start,
    output[31:0] io_c,
    output io_finished
);

  wire T0;
  reg[31:0] y;
  wire T1;
  wire T2;
  wire T3;
  reg[31:0] x;
  wire T4;
  wire T5;
  wire[31:0] T6;
  wire[31:0] T7;
  wire[31:0] T8;
  wire[31:0] T9;

`ifndef SYNTHESIS
  integer initvar;
  initial begin
    #0.001;
`ifdef RANDOM_SEED
    initvar = $random(`RANDOM_SEED);
`endif
    #0.001;
    y = {1{$random}};
    x = {1{$random}};
  end
`endif

  assign io_finished = T0;
  assign T0 = y == 32'h0;
  assign T1 = T2 || io_start;
  assign T2 = ! T3;
  assign T3 = y < x;
  assign T4 = T5 || io_start;
  assign T5 = y < x;
  assign T6 = io_start ? io_a : T7;
  assign T7 = x - y;
  assign T8 = io_start ? io_b : T9;
  assign T9 = y - x;
  assign io_c = x;

  always @(posedge clk) begin
    if(T1) begin
      y <= T8;
    end
    if(T4) begin
      x <= T6;
    end
  end
endmodule

