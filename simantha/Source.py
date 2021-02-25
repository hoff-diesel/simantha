import random

from .Part import Part

class Source:
    def __init__(
        self,
        name='Source',
        interarrival_time=None,
        part_type=Part
    ):
        self.name = name
        self.interarrival_time = interarrival_time
        self.last_arrival = 0

        self.part_type = part_type
        
        if self.interarrival_time is None:
            self.level = float('inf')
        else:
            self.level = 0

        self.define_routing()

        self.env = None

    def initialize(self):
        # schedule inital get events for each downstream machine
        # currently it's assumed that no machine pulling from a source is starved
        self.reserved_content = 0

        self.part_id = 1

        for receiver in self.downstream:
            if receiver.can_receive():
                receiver.starved = False
                self.env.schedule_event(
                    self.env.now, 
                    receiver, 
                    receiver.request_part,
                    f'{self.name}.arrival at {self.env.now}'
                )
        
    def generate_arrival(self):
        if self.interarrival_time is None:
            return
            
        self.last_arrival += 1
        if (self.last_arrival >= self.interarrival_time) and self.is_empty():
            self.level += 1
            self.last_arrival = 0
            
    def get(self, quantity=1):
        self.reserved_content -= quantity
        #if self.interarrival_time is None:
        #    return
        
        if not self.is_empty():
            self.level -= quantity
            new_part = self.part_type(id_=self.part_id)
            new_part.initialize()
            self.part_id += 1
            
            return new_part
        else:
            raise RuntimeError('Attempting to take part from source before arrival.')
    
    def reserve_content(self, quantity=1):
        self.reserved_content += quantity

    def is_empty(self):
        return self.level == 0
    
    def define_routing(self, upstream=[], downstream=[]):
        self.upstream = upstream
        self.downstream = downstream

    def can_give(self):
        # TODO: this assumes receivers are never starved
        return True

    def get_candidate_givers(self, only_free=False, blocked=False):
        return self.upstream

    def get_candidate_receivers(self, only_free=False, starved=False):
        if only_free:
            # get only candidate receivers that can accept a part
            return [obj for obj in self.get_candidate_receivers() if obj.can_receive()]
        else:
            return [obj for obj in self.downstream if obj.can_receive()]