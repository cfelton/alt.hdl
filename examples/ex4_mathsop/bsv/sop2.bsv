
package sop2;
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
module mkSOP2(IO);
   
   // Vectors to hold the delays and coefficients
   Vector#(`NTAPS, Int#(`SBITS)) h = replicate('h40);
   Vector#(`NTAPS, Reg#(Int#(`SBITS))) taps <- replicateM(mkReg(0));  
   Reg#(Int#(`SBITS)) y <- mkReg(0);
   
   rule rsop;      
          y <= fold (\+  , zipWith (\* , h, readVReg (taps))) ;
   endrule
      
   method Action write(Int#(`NBITS) x);
      taps[0] <= extend(x);
      for(int k=1; k<`NTAPS; k=k+1) begin
	 taps[k] <= taps[k-1];
      end
   endmethod 
   
   method Int#(`NBITS) read();
      read = truncate(y >> `NBITS/2);
   endmethod
   
endmodule

endpackage
