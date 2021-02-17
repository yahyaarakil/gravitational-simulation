from vector import *

class Component:
    def __init__(self, IDENTIFIER):
        self.IDENTIFIER = IDENTIFIER
        self.conditions = []

def require_position(entity):
    if "Position" in entity.comps.keys():
        return True
    else:
        return False

class Physics(Component):
    gravity_entities = []

    def __init__(self, mass = 1):
        Component.__init__(self, "Physics")
        self.conditions.append(require_position)
        self.mass = mass
        self.velocity = Vector(0, 0, 0)
        Physics.gravity_entities.append(self)

    def init(self, entity):
        self.entity = entity
        self.position = entity.comps["Position"]

    def gravity_tick(self, delta_time):
        self.position.translate(self.velocity * delta_time)

    def reset(self):
        self.velocity = Vector(0, 0, 0)

    def apply_friction(self):
        self.velocity *= 1
        # pass

    def _gravity(self, entity, distance, invert = False):
        if not invert:
            return 5 * (self.mass * entity.mass) / (distance)**2
        else:
            return (distance)**2 / (self.mass * entity.mass * 5)

    def recalc(self):
        for entity in Physics.gravity_entities:
            if entity == self:
                continue
            direction = Vector.vector_from_points(entity.position, self.position)
            distance = direction.length()
            if distance > entity.mass + self.mass or distance < 2:
                print("cont", distance)
                continue
            if distance < self.mass:
                culled_distance = self.mass
            else:
                culled_distance = distance
            gravity = self._gravity(entity, culled_distance, False)
            if distance > (self.mass + entity.mass) / 2:
                self.velocity -= (direction.normalize() * gravity)
            else:
                self.velocity = (direction.normalize() * gravity)
        self.apply_friction()
        print(self.velocity)
        # F = ma
        # a = F/m
        
    def recalc_closest(self):
        closest = Physics.gravity_entities[0]
        if closest == self:
            closest = Physics.gravity_entities[1]
        for entity in Physics.gravity_entities:
            if entity == self:
                continue
            if Vector.vector_from_points(self.position, entity.position).length() <\
                Vector.vector_from_points(self.position, closest.position).length():
                closest = entity
        
        entity = closest
        self.entity = closest

        direction = Vector.vector_from_points(entity.position, self.position)
        distance = direction.length()
        if distance > entity.mass + self.mass or distance < 2:
            print("cont", distance)
            return
        if distance < self.mass:
            culled_distance = self.mass
        else:
            culled_distance = distance
        gravity = self._gravity(entity, culled_distance, True)
        if distance > (self.mass + entity.mass) / 2:
            self.velocity -= (direction.normalize() * gravity)
        else:
            self.velocity = (direction.normalize() * gravity)
        self.apply_friction()
        print(self.velocity)
        # F = ma
        # a = F/m
        


class Position(Component):
    def __init__(self, pos = (0, 0, 0)):
        Component.__init__(self, "Position")
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

    def init(self, entity):
        self.entity = entity

    def translate(self, towards):
        self.x += towards.x
        self.y += towards.y
        self.z += towards.z