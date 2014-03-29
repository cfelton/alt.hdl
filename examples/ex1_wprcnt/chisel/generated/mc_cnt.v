module mc_cnt(input clk, input reset,
    output[4:0] io_out
);

  reg[4:0] x;
  wire T0;
  wire T1;
  wire T2;
  wire T3;
  wire[4:0] T4;
  wire[4:0] T5;
  wire[4:0] T6;

`ifndef SYNTHESIS
  integer initvar;
  initial begin
    #0.001;
`ifdef RANDOM_SEED
    initvar = $random(`RANDOM_SEED);
`endif
    #0.001;
    x = {1{$random}};
  end
`endif

  assign io_out = x;
  assign T0 = T3 || T1;
  assign T1 = ! T2;
  assign T2 = x <= 5'h1e;
  assign T3 = x <= 5'h1e;
  assign T4 = T1 ? T6 : T5;
  assign T5 = x + 5'h1;
  assign T6 = x - 5'h1;

  always @(posedge clk) begin
    if(reset) begin
      x <= 5'h0;
    end else if(T0) begin
      x <= T4;
    end
  end
endmodule

