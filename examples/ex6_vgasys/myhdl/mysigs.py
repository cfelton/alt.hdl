
from math import floor
import myhdl
from myhdl import instance, delay

class Clock(myhdl.SignalType):
    
    def __init__(self, val, frequency=1.):        
        self.frequency = frequency
        self.period = 1./frequency
        myhdl.SignalType.__init__(self, bool(val))
        
    def gen(self):
        """ generate a clock """
        @instance
        def gclock():
            self.next = False
            while True:
                yield delay(10)               
                self.next = not self.val
                
        return gclock
                                
    def timescale(self):
        """ get the timescale given the clock freq
        six simulation steps is equal to one clock cycle, each
        simulation step is clock_period/6.
        """
        tstep = int(round(((self.period)/6.) * 1e12))
        ts = "%d ps"%(tstep)
        print(ts)
        return ts

class Reset(myhdl.ResetSignal):
    def __init__(self, val, active, async):
        myhdl.ResetSignal.__init__(self,val,active,async)

    def pulse(self, delays=10):
        if isinstance(delays,(int,long)):
            self.next = self.active
            yield delay(delays)
            self.next = not self.active
        elif isinstance(delays,tuple):
            assert len(delays) in (1,2,3), "Incorrect number of delays"
            self.next = not self.active if len(delays)==3 else self.active
            for dd in delays:
                yield delay(dd)
                self.next = not self.val
            self.next = not self.active
        else:
            raise ValueError("%s type not supported"%(type(d)))
