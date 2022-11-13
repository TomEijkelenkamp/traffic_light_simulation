import random
from classes.road import Road
from classes.crossing import Crossing
from classes.point import Point
from enum import Enum

class Model(Enum):
    OVM = 1
    IDM = 2

class RoadNetwork:

    # Create a grid of roads
    # @param width: The width of the grid
    # @param height: The height of the grid
    # @param n: The number of crossings in each direction
    def __init__(self, height, width, n, deviation, border):

        x_positions = [ i*(width/n) + ((random.random()-0.5)*deviation if i not in (0,n) else 0) + border for i in range(0, n) ]
        y_positions = [ i*(height/n) + ((random.random()-0.5)*deviation if i not in (0,n) else 0) + border for i in range(0, n) ]
        
        self._crossings = [[Crossing( Point(x_positions[x], y_positions[y]) ) for y in range(n)] for x in range(n)]
        self._roads = set()
        self._cars = set()
        self._model = 2

        for x in range(n-1):
            for y in range(n-1):
                self.add_road( Road( self._crossings[x][y], self._crossings[x][y+1] ) )
                self.add_road( Road( self._crossings[x][y], self._crossings[x+1][y] ) )

        for y in range(n-1):
            self.add_road( Road( self._crossings[n-1][y], self._crossings[n-1][y+1] ) )

        for x in range(n-1):
            self.add_road( Road( self._crossings[x][n-1], self._crossings[x+1][n-1] ) )

        self._roads = sorted(self._roads)

    # Add a road to the network
    # @param road: The road to add
    def add_road(self, road):
        self._roads.add(road)

    # Add a car to a random road in the network
    def add_random_car(self):
        road = random.sample(self._roads, 1)[0]
        self._cars.add( road.add_random_car(self._model) )

    def get_roads(self):
        return self._roads

    def next(self):
        for car in self._cars:
            car.next()
            
        for car in self._cars:
            car.tick()

        for road in self._roads:
            road.next()

        for crossing in self.get_crossings():
            crossing.next()

    def get_crossings(self):
        crossings = []
        for row in self._crossings:
            for crossing in row:
                crossings.append(crossing)
        return crossings
