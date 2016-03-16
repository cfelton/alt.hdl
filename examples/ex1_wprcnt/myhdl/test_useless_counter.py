
import os
import myhdl
from myhdl import (Signal, ResetSignal, intbv, instance,
                   always, delay, StopSimulation)

from useless_counter import mm_cnt


def test_useless_counter():
    clock = Signal(bool(0))
    reset = ResetSignal(0, active=0, async=True)
    out = Signal(intbv(0, min=0, max=32))

    @myhdl.block
    def bench():
        tbdut = mm_cnt(clock, reset, out)
        
        @always(delay(4))
        def tbclk():
            clock.next = not clock
            
        @instance 
        def tbstim():
            reset.next = reset.active
            yield delay(100)
            reset.next = not reset.active
            yield clock.posedge
            
            for ii in range(35):
                if out == 31:
                    break
                yield clock.posedge
                
            assert out == 31
            yield clock.posedge
            assert out == 30
            yield clock.posedge
            assert out == 31
            
            raise StopSimulation

        return tbdut, tbclk, tbstim

    # myhdl.Simulation(bench()).run()
    tbinst = bench()
    tbinst.conf_sim(trace=True)
    tbinst.run()
    
    # myhdl.toVerilog.no_testbench = True
    # myhdl.toVerilog(mm_cnt(clock, reset, out))
    inst = mm_cnt(clock, reset, out)
    inst.convert(tb=False)


if __name__ == '__main__':
    test_useless_counter()


            