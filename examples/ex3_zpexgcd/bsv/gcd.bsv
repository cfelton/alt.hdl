
package gcd;

interface IO;
   method Action start(UInt#(32) a, UInt#(32) b);
   method UInt#(32) result();
endinterface


(* synthesize *)
module mkGCD (IO);
   Reg#(UInt#(32)) x <- mkReg(0);
   Reg#(UInt#(32)) y <- mkReg(0);
   
   rule r1 ((x > y) && (y != 0));
      x <= x - y;
   endrule
   
   rule r2 ((x <= y) && (y != 0));
      y <= y - x;
   endrule
   
   method Action start(
      UInt#(32) a, 
      UInt#(32) b) if (y == 0);
      x <= a; y <= b;
   endmethod
   
   method UInt#(32) result() if (y==0);
      return x;
   endmethod
   
endmodule

endpackage
