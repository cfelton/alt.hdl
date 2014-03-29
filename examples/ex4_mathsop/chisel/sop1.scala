
package sop1

import Chisel._

class mc_sop1(Nbits : Int, Ntaps : Int, 
	      h : Array[SInt]) extends Module {
  val io = new Bundle {
    val x = SInt(INPUT, Nbits)
    val y = SInt(OUTPUT, Nbits)
  }
  val yy = Reg(init=SInt(0, Nbits))
  val delays = Vec.fill(Ntaps){ Reg(init=SInt(0, Nbits)) }
  val mults = Vec.fill(Ntaps){ Reg(init=SInt(0, 2*Nbits)) }

  delays(0) := io.x
  for(ii <- 1 until Ntaps) {
    delays(ii) := delays(ii-1)
  }

  for(ii <- 0 until Ntaps) {
    mults(ii) := delays(ii) * h(ii)
  }
  
  val scale = UInt(Nbits/2)
  val sop = mults.reduce(_ + _)
  yy := sop >> scale
  io.y := yy 
  
}

object SOP1Main {
  def main(args: Array[String]): Unit = {
    val Nbits = 16
    val Ntaps = 4
    // @todo: calculate val mv = 0x100 >> int(log(Ntaps,2))
    val h = Array.fill(Ntaps){ SInt(0x40, Nbits) }
    chiselMain( args, () =>
		Module( new mc_sop1(Nbits, Ntaps, h)))
  }
}
