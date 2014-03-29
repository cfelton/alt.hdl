
package wprcnt

import Chisel._

class mc_cnt() extends Module {
  val io = new Bundle {
    val out = UInt(OUTPUT, 5)
  }

  val x = Reg(init=UInt(0, 5))
  when(x <= UInt(30)){
    x := x + UInt(1)
  }
  unless(x <= UInt(30)){
    x := x - UInt(1)
  }

  io.out := x
}

object CountMain {
  def main(args: Array[String]): Unit = {
    chiselMain(args, () =>
	       Module(new mc_cnt()))
  }
}
