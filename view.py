import pygame
import time
from world import *
from vector import *
from entity import *
from comps import *

# Constants
RED = (255, 0, 0)
FADE_RED = (255, 0, 0, 100)
GREEN = (0, 255, 0)
FADE_GREEN = (0, 255, 0, 200)
BLUE = (0, 0, 255)
screen_width = 800
screen_height = 600

class View:
    # Init
    def __init__(self, WORLD = None):
        self.x = 0
        self.y = 0
        self.moveto = Vector(0, 0, 0)
        self.pan_speed = 100
        self.view_scale = 1

        pygame.init()
        self.FONT = pygame.font.Font('freesansbold.ttf', 32)
        if WORLD == None:
            self.WORLD = World()
        else:
            self.WORLD = WORLD

        # Create screen
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        # Title
        pygame.display.set_caption("Blobbing Experiments")
        # pygame.display.set_icon(pygame.image.load(""))

        # # init controlling variables
        self.running = True
        self.clock = pygame.time.Clock()
        self.physics_suspended = False

    # Helper Fucntions
    def write_text(self, text, location):
        text = self.FONT.render(text, True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.topleft = (location[0], location[1])
        self.screen.blit(text, textRect)

    def drawCircle(self, color, location, radius):
        pygame.draw.circle(self.screen, color, location, radius)

    def draw_circle_alpha(self, color, location, radius):
        target_rect = pygame.Rect(location, (0, 0)).inflate((radius * 2, radius * 2))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.circle(shape_surf, color, (radius, radius), radius)
        self.screen.blit(shape_surf, target_rect)

    def resolve_entity_position_to_screen(self, entity):
        x = entity.comps["Position"].x - self.x
        y = (entity.comps["Position"].y - self.y) * -1
        # if x > screen_width or y > screen_height or x < 0 or y < 0:
        #     return None
        return (x, y)

    def resolve_point_to_screen(self, point):
        x = point.x - self.x
        y = point.y - self.y * -1
        # if x > screen_width or y > screen_height or x < 0 or y < 0:
        #     return None
        return (x, y)

    def main_loop(self, delta_time):
        # # Main Loop
        # start

        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.moveto += Vector(0, 1, 0)
                if event.key == pygame.K_a:
                    self.moveto += Vector(-1, 0, 0)
                if event.key == pygame.K_s:
                    self.moveto += Vector(0, -1, 0)
                if event.key == pygame.K_d:
                    self.moveto += Vector(1, 0, 0)
                if event.key == pygame.K_LSHIFT:
                    self.pan_speed *= 3
                if event.key == pygame.K_i:
                    self.view_scale += 0.1
                if event.key == pygame.K_o:
                    self.view_scale -= 0.1
                if event.key == pygame.K_p:
                    self.physics_suspended = not self.physics_suspended
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.moveto += Vector(0, -1, 0)
                if event.key == pygame.K_a:
                    self.moveto += Vector(1, 0, 0)
                if event.key == pygame.K_s:
                    self.moveto += Vector(0, 1, 0)
                if event.key == pygame.K_d:
                    self.moveto += Vector(-1, 0, 0)
                if event.key == pygame.K_LSHIFT:
                    self.pan_speed /= 3

        # Move view
        self.x += self.moveto.x * delta_time * self.pan_speed
        self.y += self.moveto.y * delta_time * self.pan_speed

        # start rendering
        self.screen.fill((0, 0, 0))

        # Layer 1
        for entity in self.WORLD.entities:
            if "Physics" in entity.comps:
                pos = self.resolve_entity_position_to_screen(entity)
                if pos == None:
                    continue
                self.draw_circle_alpha(FADE_RED, (pos[0], pos[1]), entity.comps["Physics"].mass * self.view_scale)

        # Layer 2
        for entity in self.WORLD.entities:
            if "Physics" in entity.comps:
                pos = self.resolve_entity_position_to_screen(entity)
                if pos == None:
                    continue
                self.draw_circle_alpha(FADE_GREEN, (pos[0], pos[1]), entity.comps["Physics"].mass * self.view_scale / 2)

        # Layer 2
        for entity in self.WORLD.entities:
            if "Position" in entity.comps:
                pos = self.resolve_entity_position_to_screen(entity)
                if pos == None:
                    continue
                self.drawCircle(BLUE, (pos[0], pos[1]), 4 * self.view_scale)

        # Directions

        # Layer 3
        for entity in self.WORLD.entities:
            if "Position" in entity.comps:
                position = entity.comps["Position"]
                pos = self.resolve_entity_position_to_screen(entity)
                if pos == None:
                    continue
            self.write_text("({},{})".format(int(position.x), int(position.y)), (pos[0], pos[1]))

        # GUI
        self.write_text("FPS: {} - ({},{})".format(int(self.clock.get_fps()),
        int(self.x), int(self.y)), (0, 0))

        # end rendering
        pygame.display.update()
        self.clock.tick(60)
