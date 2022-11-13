from classes.light import Light
from classes.orientation import Orientation
from classes.fuzzylogic_signals_control import fuzzylogicsignals

class Crossing:

    def __init__(self, point):
        self._position = point
        self._roads = [None, None, None, None]
        self._lights = set()
        self._green_time = 0
        self._green = Orientation.N
        self._sensor_position = 750
        self._recalculate_green_time = 50
        self._cars_sensored_last_iteration = 0
        self._cars_sensored_current_iteration = 0
        self._fuzz = fuzzylogicsignals()

    def get_position(self):
        return self._position

    def add_road(self, road, orientation):
        self._roads[orientation.value] = road
        self._lights.add( Light(self, road, orientation) )

    def get_position(self):
        return (self._position.x, self._position.y)

    def get_light_status(self, road):
        for light in self._lights:
            if light.get_road() == road:
                return light.get_state()

    def next(self):
        if self._green_time <= 0:
            self.rotate_to_next_green_light()
            self.set_green_time()
        else:
            self._green_time -= 1
        if self._green_time > 0 and self._green_time % self._recalculate_green_time == 0:
            self.set_green_time()

    def set_current_green_to_red(self):
        for light in self._lights:
            if light._orientation == self._green:
                light.set_state('R') 
            
    def rotate_to_next_green_light(self):
        self._green = Orientation.next(self._green)
        while not self._roads[self._green.value]:
            self._green = Orientation.next(self._green)
        for light in self._lights:
            light.set_state('G') if light._orientation == self._green else light.set_state('R')

    def set_green_time(self):
        self._cars_sensored_current_iteration = self.count_cars_sensored()
        self._green_time = self._fuzz.fuzzytime(self._cars_sensored_current_iteration, self._cars_sensored_current_iteration - self._cars_sensored_last_iteration)
        self._cars_sensored_last_iteration = self._cars_sensored_current_iteration

    def get_green_road(self):
        return self._roads[self._green.value]

    def get_cars_green_road(self):
        green_road = self.get_green_road()
        if green_road._crossing_a == self:
            return green_road._cars_a
        else:
            return green_road._cars_b

    def count_cars_sensored(self):
        green_road = self.get_green_road()
        cars_green_road = self.get_cars_green_road()
        cars_sensored = 0
        for car in cars_green_road:
            if car._current_position > green_road._length - self._sensor_position:
                cars_sensored += 1
        return cars_sensored

    def get_choices(self, excluding):
        choices = list()
        for road in self._roads:
            if road and road != excluding:
                choices.append(road)
        return choices

    def __eq__(self, __o: object) -> bool:
        return self._position == __o._position

    def __hash__(self) -> int:
        return hash(self._position)

    def get_lights(self):
        return self._lights



    