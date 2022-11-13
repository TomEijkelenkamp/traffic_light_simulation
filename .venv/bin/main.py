from classes.window import Window
from classes.road_network import RoadNetwork
from classes.fuzzylogic_signals_control import fuzzylogicsignals
import pygame

def main():
    road_network = RoadNetwork(950, 950, 3, 50, 50)

    for i in range(30):
        road_network.add_random_car()

    window = Window(1000, 1000, 1)

    # testing fuzzy logic
    fz = fuzzylogicsignals()
    fz.fuzzytime(7,3) # input to the function count and change in count

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

