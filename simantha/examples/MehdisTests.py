from simantha import Source, Machine, Buffer, Sink, System
# from simantha import utils

def main():
    source = Source()
    M1 = Machine(name='M1', cycle_time=2)
    B1 = Buffer(capacity=4)
    M2 = Machine(name='M2', cycle_time=1)
    B2 = Buffer(capacity=8)
    M3 = Machine(name='M3', cycle_time=1)
    B3 = Buffer(capacity=16)
    M4 = Machine(name='M4', cycle_time=1)
    sink = Sink()

    source.define_routing(downstream=[M1])
    M1.define_routing(upstream=[source], downstream=[B1])
    B1.define_routing(upstream=[M1], downstream=[M2])
    M2.define_routing(upstream=[B1],downstream=[B2])
    B2.define_routing(upstream=[M2], downstream=[M3])
    M3.define_routing(upstream=[B2],downstream=[B3])
    B3.define_routing(upstream=[M3], downstream=[M4])
    M4.define_routing(upstream=[B3],downstream=[sink])
    sink.define_routing(upstream=[M2])

    system = System(objects=[source, M1, B1, M2,
                             B2, M3, B3, M4, sink])

    system.simulate(simulation_time=500)
#   system.simulate(simulation_time=utils.WEEK)

if __name__ == '__main__':
    main()
    