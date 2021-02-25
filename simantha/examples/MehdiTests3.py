
from simantha import Source, Machine, Buffer, Sink, System
# from simantha import utils

import matplotlib
import matplotlib.pyplot as plt
#import numpy as np
#import random

def plot_health(system):
    plt.figure(figsize=(8,5))
    
    for machine in system.machines:
        plt.step(
            machine.health_data['time'], 
            machine.health_data['health'], 
            lw=2, where='post', label=machine.name
        )
        
    plt.xlabel('time (minutes)')
    plt.ylabel('machine health')
    
    plt.legend()
    plt.show()

def plot_throughput(system, plot_rated_throughput=True):
    plt.figure(figsize=(8,5))

    bottleneck_cycle_time = 0
    for machine in system.machines:
        throughput = [
            production / t 
            for production, t in zip(
                machine.production_data['production'][1:], 
                machine.production_data['time'][1:]
            )
        ]
        plt.plot(machine.production_data['time'][1:], throughput, lw=2, label=machine.name)
        if machine.cycle_time.mean > bottleneck_cycle_time:
            bottleneck_cycle_time = machine.cycle_time.mean
        
    if plot_rated_throughput:
        plt.plot(
            [0, system.env.now], 
            [1/bottleneck_cycle_time]*2, ls='--', color='grey', label='Rated TH'
        )
    
    plt.xlabel('time (minutes)')
    plt.ylabel('throughput (units/minute)')

    plt.xlim([0, system.env.now])

    plt.legend()
    plt.show()
        
def main():
    source = Source()
    
    M1 = Machine(name='M1', cycle_time=1)
    #M99 = Machine(name='M99', cycle_time=1)
    stage1 = [M1]#, M99]
    B1 =Buffer(capacity=10)

    
    M2 = Machine(name='M2', cycle_time=1)
    M3 = Machine(name='M3', cycle_time=1)
    M4 = Machine(name='M4', cycle_time=1)
    M7 = Machine(name='M7', cycle_time=1)
    stage2 = [M2, M3, M4, M7]
    stage4 = [M2, M3, M4]
    B2 = Buffer(capacity=10)
    sink = Sink()


    M5 = Machine(name='M5', cycle_time=1)
    M6 = Machine(name='M6', cycle_time=1)
    stage3 = [M5, M6]
    B3 = Buffer(capacity=10)
    

    source.define_routing(downstream=stage1)
    for machine in stage1:
        machine.define_routing(upstream=[source], downstream=[B1])
    B1.define_routing(upstream=stage1, downstream=stage2)
    for machine in stage2:
        machine.define_routing(upstream=[B1], downstream=[B2])
    B2.define_routing(upstream=stage2, downstream=stage3)
    for machine in stage3:
        machine.define_routing(upstream=[B2], downstream=[B3])
    B3.define_routing(upstream=stage3, downstream=stage4)
    for machine in stage4:
        machine.define_routing(upstream=[B3], downstream=[sink])
    sink.define_routing(upstream=stage4)

    #objects = [source] + station1 + [B1] + station2 + [B2] + station3 + [B3]  + [sink]
    objects = [source, B1, B2, B3, sink] + stage1 + stage2 + stage3 + stage4 

    system = System(objects)

    system.simulate(simulation_time=10000)
#   system.simulate(simulation_time=utils.WEEK)
    print(f'\nM1 parts made: {M1.parts_made}')
    print(f'M2 parts made: {M2.parts_made}')
    print(f'M3 parts made: {M3.parts_made}')
    print(f'M4 parts made: {M4.parts_made}')
    print(f'M5 parts made: {M5.parts_made}')
    print(f'M6 parts made: {M6.parts_made}')
    print(f'M7 parts made: {M7.parts_made}')

    print(f'Stage 1 parts made: {M1.parts_made}\n')

    print(f'Stage 2 parts made: {M2.parts_made + M3.parts_made + M4.parts_made + M7.parts_made}\n')
    
    print(f'Stage 3 parts made: {M5.parts_made + M6.parts_made}\n')
    
    print(f'Stage 4 parts made: {M2.parts_made + M3.parts_made + M4.parts_made}\n')

    print(f'Total parts made: {sink.level}')
    
    plot_throughput(system, plot_rated_throughput=False)
    
    plot_health(system)
    
if __name__ == '__main__':
    main()
    