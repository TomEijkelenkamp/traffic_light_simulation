from bin.classes.light import Light
from bin.classes.orientation import Orientation

class Crossing:

    def __init__(self, point):
        self._position = point
        self._roads = set()
        self._lights = set()
        self._time = 200
        self._green = Orientation.N

    def get_position(self):
        return self._position

    def add_road(self, road, orientation):
        self._roads.add(road)
        self._lights.add( Light(self, road, orientation) )

    def get_position(self):
        return (self._position.x, self._position.y)

    def get_light_status(self, road):
        for light in self._lights:
            if light.get_road() == road:
                return light.get_state()

    def next(self):
        if self._time == 0:
            self._green = Orientation.next(self._green)
            for light in self._lights:
                light.set_state('G') if light._orientation == self._green else light.set_state('R')
            self._time = 200
        else:
            self._time -= 1
            
    def __eq__(self, __o: object) -> bool:
        return self._position == __o._position

    def __hash__(self) -> int:
        return hash(self._position)

    def get_lights(self):
        return self._lights



    