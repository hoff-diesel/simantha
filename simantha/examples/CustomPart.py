import random

from simantha import Part, Source, Machine, Buffer, Sink, System, utils

class QualityPart(Part):
    def initialize(self):
        self.quality = 1.0
        
class QualityMachine(Machine):
    def __init__(self, quality_distribution, **kwargs):
        # Quality distribution should return a value on [0, 1]
        self.quality_distribution = quality_distribution
        
        super().__init__(**kwargs)
    
    def output_addon_process(self, part):
        part.quality *= self.quality_distribution()

def main():
    source = Source(part_type=QualityPart)
    M1 = QualityMachine(
        name='M1',
        quality_distribution=lambda: 1-0.1*random.random(), # [0.9, 1.0]
        cycle_time=1
    )
    B1 = Buffer('B1', capacity=10)
    M2 = QualityMachine(
        name='M2',
        quality_distribution=lambda: 0.8-0.2*random.random(), # [0.6, 0.8]
        cycle_time=2
    )
    M3 = QualityMachine(
        name='M3',
        quality_distribution=lambda: 0.6-0.3*random.random(), # [0.3, 0.6]
        cycle_time=2
    )
    sink = Sink()

    source.define_routing(downstream=[M1])
    M1.define_routing(upstream=[source], downstream=[B1])
    B1.define_routing(upstream=[M1], downstream=[M2, M3])
    M2.define_routing(upstream=[B1], downstream=[sink])
    M3.define_routing(upstream=[B1], downstream=[sink])
    sink.define_routing(upstream=[M2, M3])

    system = System([source, M1, B1, M2, M3, sink])

    random.seed(1)
    system.simulate(simulation_time=utils.DAY)

    print()
    for machine in system.machines:
        machine_parts = [
            part for part in sink.contents if machine.name in part.routing_history
        ]
        average_quality = (
            sum([part.quality for part in machine_parts]) / machine.parts_made
        )
        print(f'{machine.name} average part quality: {average_quality:.2%}')

if __name__ == '__main__':
    main()
    