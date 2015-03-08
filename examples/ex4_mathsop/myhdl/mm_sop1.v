// File: mm_sop1.v
// Generated by MyHDL 0.9dev
// Date: Sun Aug 31 23:38:08 2014


`timescale 1ns/10ps

module mm_sop1 (
    clock,
    reset,
    x,
    y
);


input clock;
input reset;
input signed [15:0] x;
output signed [15:0] y;
reg signed [15:0] y;


reg signed [15:0] xd [0:4-1];




always @(posedge clock, negedge reset) begin: MM_SOP1_RTL
    integer ii;
    integer sop;
    integer c;
    if (reset == 0) begin
        y <= 0;
        xd[0] <= 0;
        xd[1] <= 0;
        xd[2] <= 0;
        xd[3] <= 0;
    end
    else begin
        xd[0] <= x;
        for (ii=1; ii<4; ii=ii+1) begin
            xd[ii] <= xd[(ii - 1)];
        end
        sop = 0;
        for (ii=0; ii<4; ii=ii+1) begin
            case (ii)
                0: c = 64;
                1: c = 64;
                2: c = 64;
                default: c = 64;
            endcase
            sop = ($signed({1'b0, sop}) + (c * xd[ii]));
        end
        y <= $signed(sop >>> 8);
    end
end

endmodule
