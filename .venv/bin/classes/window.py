from numpy import  int64, short
import pygame
from pygame import gfxdraw
from pygame import font
import bin.classes.turbo

class Window:

    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.scale = scale
        pygame.init()
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

        for crossing in road_network.get_crossings():
            self.draw_crossing(crossing)

    def draw_car(self, car):
        position = car.get_current_position_2d()
        pygame.gfxdraw.filled_circle(self.screen, int(position.x), int(position.y), car._length, car.get_color())

        front = car.get_current_position_2d_front()
        pygame.gfxdraw.filled_circle(self.screen, int(front.x), int(front.y), int(car._length / 3), (0,0,0))

        # draw the current_position_in_queue as text
        font = pygame.font.SysFont('Arial', 20, (0, 0, 0), (0, 0, 0))
        text = font.render(str(car.get_number_in_queue()), True, (0, 0, 0))
        self.screen.blit(text, (position.x, position.y))

        

    def draw_road(self, road):
        pygame.draw.line(self.screen, (220,220,220), road._crossing_a.get_position(), road._crossing_b.get_position(), 20)

    def draw_crossing(self, crossing):
        for light in crossing.get_lights():
            self.draw_light(light)
        # font = pygame.font.SysFont('Arial', 20, (0, 0, 0), (0, 0, 0))
        # text = font.render(str(crossing._time), True, (0, 0, 0))
        # self.screen.blit(text, (crossing.get_position()[0], crossing.get_position()[1]))

    def draw_light(self, light):
        pygame.gfxdraw.filled_circle(self.screen, int(light.get_position()[0]), int(light.get_position()[1]), 10, light.get_color())

    def update(self):
        pygame.display.update()

    def clear(self):
        self.screen.fill((255, 255, 255))

    def quit(self):
        pygame.quit()
