module mc_maths1(
    input [15:0] io_x,
    input [15:0] io_y,
    output[15:0] io_v
);

  wire[15:0] T0;
  wire[31:0] T1;
  wire[15:0] T2;


  assign io_v = T0;
  assign T0 = T1[4'hf:1'h0];
  assign T1 = $signed(T2) * $signed(16'ha);
  assign T2 = io_x + io_y;
endmodule

