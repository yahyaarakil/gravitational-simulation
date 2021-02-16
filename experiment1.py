from view import *
from vector import *
from world import *
from entity import *
from comps import *

# Paricle

# Constants
G = 10
FRICTION = 10
SIMULATION_TICK = 1
TARGET_FPS = 60

# Collider Shapes
CIRCLE = 0
SQUARE = 1
HEXAGON = 2
TRIANGLE = 3

class Particle(Entity):
    particles = []

    def __init__(self, pos, shape = CIRCLE, mass = 1):
        Entity.__init__(self)
        Particle.particles.append(self)
        self.add_comp(Position(pos))
        self.add_comp(Physics(mass))





# INIT
view = View()
world = view.WORLD

# Setup
x = Particle((0, -300, 0), mass=200)
x.comps["Physics"].velocity = Vector(50, 0, 0)
world.place_entity(x)
y = Particle((400, -600, 0), mass=200)
y.comps["Physics"].velocity = Vector(0, 50, 0)
world.place_entity(y)

delta_time = 0

while view.running == True:
    start = time.time()
    view.main_loop(delta_time)
    world.simulate_physics(delta_time)
    delta_time = time.time() - start