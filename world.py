PHYSICS_TICK_SIZE = 0.1

class World:
    def __init__(self):
        self.entities = []
        self.physics_tick = 0
        
    def place_entity(self, entity):
        self.entities.append(entity)

    def simulate_physics(self, delta_time):
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