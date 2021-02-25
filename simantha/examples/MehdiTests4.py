
from simantha import Source, Machine, Buffer, Sink, System
# from simantha import utils

#import numpy as np
#import random

def main():
    source = Source()
    
    M1 = Machine(name='M1', cycle_time=1)
    M99 = Machine(name='M99', cycle_time=1)
    stage1 = [M1,M99]
    B1 =Buffer(capacity=10)

    
    M2 = Machine(name='M2', cycle_time=1)
    stage2 = [M2]
    B2 = Buffer(capacity=10)
    
    M3 = Machine(name='M3', cycle_time=1)
    stage3 = [M99, M3]
    
    sink = Sink()
    

    source.define_routing(downstream=stage1)
    for machine in stage1:
        machine.define_routing(upstream=[source], downstream=[B1])
    B1.define_routing(upstream=stage1, downstream=stage2)
    for machine in stage2:
        machine.define_routing(upstream=[B1], downstream=[B2])
    B2.define_routing(upstream=stage2, downstream=stage3)
    for machine in stage3:
        machine.define_routing(upstream=[B2], downstream=[sink])
    sink.define_routing(upstream=stage3)

    #objects = [source] + station1 + [B1] + station2 + [B2] + station3 + [B3]  + [sink]
    objects = [source, B1, B2, sink] + stage1 + stage2 + stage3  

    system = System(objects)

    system.simulate(simulation_time=500)
#   system.simulate(simulation_time=utils.WEEK)

    

if __name__ == '__main__':
    main()
    