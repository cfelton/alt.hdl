
package sop2

import Chisel._

class mc_sop2(Nbits : Int) extends Module {
  val io = new Bundle {
    val x = SInt(INPUT, Nbits)
    val y = SInt(OUTPUT, Nbits)
  }
  
  // probably a better way to repeat in Scala??
  val h = Array(SInt(0x40, Nbits), 
		SInt(0x40, Nbits), 
		SInt(0x40, Nbits), 
		SInt(0x40, Nbits))

  def delays[T <: Data](x: T, n: Int): List[T] =
    if (n <= 1) List(x) else x :: delays(Reg(next = x), n-1)

  def sop[T <: Num](hs: Seq[T], x: T): T =
    (hs, delays(x, hs.length)).zipped.map(_ * _ ).reduce( _ + _ )

  io.y := sop(h, io.x)
}

object SOPMain {
  def main(args: Array[String]): Unit = {
    chiselMain( args, () =>
		Module( new mc_sop2(16) ))
  }
}




