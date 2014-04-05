
from myhdl import *        
                  
def mm_median(sys, wi, wo, med):
    """ hardware version of the median: sort-network
    """
    N,st = len(wi), wi[0]

    # create the logical signal banks (list of signals)
    z = [wi,] + [[Signal(st.val) for _ in range(N)]
                      for stage in range(N-1)] + [wo,]

    # create (instantiated) the compare stages
    gcmp = [m_cmp(sys, z[ii], z[ii+1], ii) 
            for ii in range(N)]
    
    # grab the median (middle) from the output of the 
    # last stage
    MN = N//2
    @always_comb 
    def rtlmed():
        med.next = wo[MN]

    return gcmp, rtlmed


def m_cmp(sys, x, z, stage=0):
    """ compare stage
    """
    N = len(z)
    K = 0 if stage%2 else 1
    B = 0 if K == 1 else N-1
    @always_seq(sys.clock.posedge, reset=sys.reset)
    def rtl():
        z[B].next = x[B]
        for ii in range(K, N-1, 2):
            z[ii].next   = x[ii] if x[ii] < x[ii+1] else x[ii+1] 
            z[ii+1].next = x[ii] if x[ii] > x[ii+1] else x[ii+1] 

    return rtl