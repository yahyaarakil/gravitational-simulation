PHYSICS_TICK_SIZE = 0.01

class World:
    def __init__(self):
        self.entities = []
        self.physics_tick = 0
        self.physics_suspended = False
        
    def place_entity(self, entity):
        self.entities.append(entity)

    def simulate_physics(self, delta_time):
        if self.physics_suspended:
            return
        self.physics_tick += delta_time
        if self.physics_tick > PHYSICS_TICK_SIZE:
            self.physics_tick = 0
            # for entity in self.entities:
            #     if "Physics" in entity.comps:
            #         entity.comps["Physics"].reset()
            for entity in self.entities:
                if "Physics" in entity.comps:
                    entity.comps["Physics"].recalc()
        for entity in self.entities:
            if "Physics" in entity.comps:
                entity.comps["Physics"].gravity_tick(delta_time)