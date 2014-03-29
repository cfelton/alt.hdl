
package gcd

import Chisel._

class mc_gcd extends Module {
  val io = new Bundle {
    val a  = UInt(INPUT,  32)
    val b  = UInt(INPUT,  32)
    val start  = Bool(INPUT)
    val c  = UInt(OUTPUT, 32)
    val finished  = Bool(OUTPUT)
  }
  val x  = Reg(UInt())
  val y  = Reg(UInt())
  when   (x > y) { x := x - y }
  unless (x > y) { y := y - x }
  when (io.start) { x := io.a; y := io.b }
  io.c := x
  io.finished := y === UInt(0)
}

object GCDMain {
  def main(args: Array[String]): Unit = {
    chiselMain(args, () => Module(new mc_gcd()))
  }
}
