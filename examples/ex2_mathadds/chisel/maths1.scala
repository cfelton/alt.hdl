
package maths1

import Chisel._

class mc_maths1(M : SInt, Nbits : Int) extends Module {
    val io = new Bundle {
	val x = SInt(INPUT, Nbits)
	val y = SInt(INPUT, Nbits)    
        val v = SInt(OUTPUT, Nbits)
    }

    io.v := (io.x + io.y) * M
}


object MathsMain {
  def main(args: Array[String]): Unit = { 
    chiselMain( args, () => 
	        Module( new mc_maths1(SInt(10, 16), 16) ))
  }
}

