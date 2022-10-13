import random
from bin.classes.car import Car
import math

class Road:

    def __init__(self, crossing_a, crossing_b):
        self._crossing_a = crossing_a
        self._crossing_b = crossing_b
        self._length = self.length()

        crossing_a.add_road(self)
        crossing_b.add_road(self)

        self._cars_a = []
        self._cars_b = []

    # Add a random car to the road in a random direction
    def add_random_car(self):
        if random.choice([True, False]):
            car = Car(self, 'a')
            self._cars_a.append( car )
            return car
        else:
            car = Car(self, 'b')
            self._cars_b.append( car )
            return car

    def add_car(self, car):
        if car._direction == 'a':
            self._cars_a.append(car)
        else:
            self._cars_b.append(car)

    def remove_car(self, car):
        if car._direction == 'a':
            self._cars_a.remove(car)
        else:
            self._cars_b.remove(car)
        
    def length(self):
        a = self._crossing_a.get_position()
        b = self._crossing_b.get_position()
        return math.sqrt( (a[0] - b[0])**2 + (a[1] - b[1])**2 )

    def get_car_a(self, i):
        return self._cars_a[i]

    def get_car_b(self, i):
        return self._cars_b[i]

    def __eq__(self, __o: object) -> bool:
        return self._crossing_a == __o._crossing_a and self._crossing_b == __o._crossing_b

    def __hash__(self) -> int:
        return hash((self._crossing_a, self._crossing_b))

