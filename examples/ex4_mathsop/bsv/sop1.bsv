
package sop1;
import Vector::*;

// the two main parameters for this module
`define NTAPS 4
`define NBITS 16
`define SBITS 32

interface IO;
   (* always_ready, always_enabled *)
   method Action write(Int#(`NBITS) x);
   (* always_ready, always_enabled *)
   method Int#(`NBITS) read();
endinterface

(* synthesize *)
module mkSOP1(IO);
   
   // Vectors to hold the delays and coefficients
   Vector#(`NTAPS, Int#(`NBITS)) h = replicate('h40);
   Vector#(`NTAPS, Reg#(Int#(`NBITS))) taps <- replicateM(mkReg(0));  
   Reg#(Int#(`SBITS)) y <- mkReg(0);
   
   rule rsop;      
      Int#(`SBITS) sop = 0;
      for(int k=0; k<`NTAPS; k=k+1) begin
	 sop = sop + (extend(h[k]) * extend(taps[k]));
      end
      y <= sop;
   endrule
   
   method Action write(Int#(`NBITS) x);
      taps[0] <= x;
      for(int k=1; k<`NTAPS; k=k+1) begin
	 taps[k] <= taps[k-1];
      end
   endmethod 
   
   method Int#(`NBITS) read();
      read = truncate(y >> `NBITS/2);
   endmethod
   
endmodule

endpackage
