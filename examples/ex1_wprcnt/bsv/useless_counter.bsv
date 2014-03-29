
package useless_counter;

interface IO;
   (* always_ready *)
   method UInt#(5) out();
endinterface

(* synthesize *)
module mkCnt(IO);
   Reg#(UInt#(5)) x <- mkReg(0);
   
   rule up (x <= 30);
      x <= x + 1;
   endrule
   
   rule bounce (x > 30);
      x <= x - 1;
   endrule
   
   method UInt#(5) out();
      out = x;
   endmethod 
   
endmodule
endpackage
