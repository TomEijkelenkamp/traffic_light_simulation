import pygame
from pygame import gfxdraw
import bin.classes.turbo

class Window:

    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.scale = scale
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill((100, 100, 100))
        pygame.display.set_caption('Traffic Simulation')

    def draw(self, road_network):
        for road in road_network.get_roads():
            self.draw_road(road)

        for road in road_network.get_roads():
            for car in road._cars_a:
                self.draw_car(car)
            for car in road._cars_b:
                self.draw_car(car)

    def draw_car(self, car):
        position = car.get_current_position_2d()
        pygame.gfxdraw.filled_circle(self.screen, int(position.x), int(position.y), car._length, car.get_color())
        pygame.gfxdraw.aacircle(self.screen, int(position.x), int(position.y), car._length, car.get_color())

    def draw_road(self, road):
        pygame.draw.line(self.screen, (220,220,220), road._crossing_a.get_position(), road._crossing_b.get_position(), 10)

    def update(self):
        pygame.display.update()

    def clear(self):
        self.screen.fill((255, 255, 255))

    def quit(self):
        pygame.quit()
