from simantha import Source, Machine, Buffer, Sink, System
# from simantha import utils

#import numpy as np
#import random

def main():
    source = Source()
    
    M1 = Machine(name='M1', cycle_time=1)
    #M99 = Machine(name='M99', cycle_time=1)
    station1 = [M1]#, M99]
    B1 =Buffer(capacity=10)

    
    M2 = Machine(name='M2', cycle_time=1)
    M3 = Machine(name='M3', cycle_time=1)
    M4 = Machine(name='M4', cycle_time=1)
    station2 = [M2, M3, M4]
    B2 = Buffer(capacity=10)
    sink = Sink()


    M5 = Machine(name='M5', cycle_time=1)
    M6 = Machine(name='M6', cycle_time=1)
    station3 = [M5, M6]
    B3 = Buffer(capacity=10)
    

    source.define_routing(downstream=station1)
    for machine in station1:
        machine.define_routing(upstream=[source], downstream=[B1])
    B1.define_routing(upstream=station1, downstream=station2)
    for machine in station2:
        #machine.define_routing(upstream=[B1,B3],downstream=[B2,sink])
       
        #possible for station2 to get a part upstream from B1, then 
        #send that to sink -> this needs rules
        #define upstream first, then do if-statement for downstream?
        machine.define_routing(upstream=[B1,B3])
        if machine.upstream == [B1]: #part came from B1, then:
           machine.define_routing(downstream=[B2])
        if machine.upstream == [B3]: #part came from B3, then:
            machine.define_routing(downstream=[sink])


        #if machine.upstream == [B1]: #part came from B1, then:
        #    machine.define_routing(upstream=[B1], downstream=[B2])
        #if machine.upstream == [B3]: #part came from B3, then:
        #    machine.define_routing(upstream=[B3], downstream=[sink])
    B2.define_routing(upstream=station2, downstream=station3)
    for machine in station3:
        machine.define_routing(upstream=[B2], downstream=[B3])
    sink.define_routing(upstream=station2)

    #objects = [source] + station1 + [B1] + station2 + [B2] + station3 + [B3]  + [sink]
    objects = [source, B1, B2, B3, sink] + station1 + station2 + station3

    system = System(objects)

    system.simulate(simulation_time=10000)
#   system.simulate(simulation_time=utils.WEEK)

    

if __name__ == '__main__':
    main()
    