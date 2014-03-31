package maths1;
   
interface IO;
   (* always_ready *)
   method ActionValue #(Int#(16)) update(
      Int#(16) x, Int#(16) y );
endinterface

(* synthesize *)
module mkMaths1 #(parameter Int#(16) m_val) (IO);
   
   method ActionValue #(Int#(16)) update (
      Int#(16) x, Int#(16) y );
       return (x + y) * m_val;
   endmethod
   
endmodule 
   
endpackage 


  
  
