from bin.classes.window import Window
from bin.classes.road_network import RoadNetwork
import pygame

def main():
    road_network = RoadNetwork(800, 800, 5, 50, 50)

    for i in range(50):
        road_network.add_random_car()

    window = Window(850, 850, 1)

    done = False
    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        window.clear()
        road_network.next()

        window.draw( road_network )
        window.update()

        clock.tick(60)



if __name__ == "__main__":
    main()

