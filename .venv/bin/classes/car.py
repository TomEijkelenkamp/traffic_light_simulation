
import math
import random
from bin.classes.turbo import Turbo

class Car:

    # Create a random car
    # @param average_speed: The average speed of the car
    # @param max_speed: The maximum speed of the car
    # @param acceleration: The acceleration of the car
    # @param deceleration: The deceleration of the car
    # @param length: The length of the car
    def __init__(self, road, direction):
        self._road = road
        self._direction = direction

        self._mass = random.randint(1000, 2000)
        self._friction = random.randint(100, 200)
        self._sensitify = 1 / random.randint(40, 80)
        self._force = 0

        self._safety_distance = 50
        self._max_speed = 50
        self._length = 10
        
        self._current_speed = 0
        self._current_position = 0

        self._next_speed = 0
        self._next_position = 0

        self._choice = self.choice()

    def tick(self):
        if (self._next_position > self._road._length):
            self._next_position = self._next_position - self._road._length
            self._road.remove_car(self)
            
            if self._direction == 'a':
                self._direction = 'b' if self._road._crossing_a == self._choice._crossing_a else 'a'
            else:
                self._direction = 'b' if self._road._crossing_b == self._choice._crossing_a else 'a'

            self._road = self._choice
            self._road.add_car(self)
            self._choice = self.choice()

        self._current_position = self._next_position
        self._current_speed = self._next_speed

    def next(self):
        self._force = self._sensitify * self.optimal_velocity() - self._current_speed
        self._next_speed = self._current_speed + self._force
        self._next_position = self._current_position + self._current_speed

    def optimal_velocity(self):
        return self._max_speed / 2 * ( math.tanh( self.headway() - self._safety_distance ) + math.tanh( self._safety_distance ) )

    def headway(self):
        if self.leading_vehicle() == self:
            a = self.get_current_position_2d()
            b = self._road._crossing_a._position if self._direction == 'a' else self._road._crossing_b._position
            headway = math.sqrt( (a.x - b.x)**2 + (a.y - b.y)**2 )

            if self._direction == 'a':
                if headway > 30 and self._road._crossing_a.get_light_status(self._road) == 'R':
                    return headway
            else:
                if headway > 30 and self._road._crossing_b.get_light_status(self._road) == 'R':
                    return headway

            if self._direction == 'a':
                if self._road._crossing_a == self._choice._crossing_a:
                    if len(self._choice._cars_b) > 0:
                        c = self._choice._cars_b[-1].get_current_position_2d()
                        headway += math.sqrt( (c.x - b.x)**2 + (c.y - b.y)**2 )
                    else:
                        headway += self._choice._length
                else:
                    if len(self._choice._cars_a) > 0:
                        c = self._choice._cars_a[-1].get_current_position_2d()
                        headway += math.sqrt( (c.x - b.x)**2 + (c.y - b.y)**2 )
                    else:
                        headway += self._choice._length
            else:
                if self._road._crossing_b == self._choice._crossing_a:
                    if len(self._choice._cars_b) > 0:
                        c = self._choice._cars_b[-1].get_current_position_2d()
                        headway += math.sqrt( (c.x - b.x)**2 + (c.y - b.y)**2 )
                    else:
                        headway += self._choice._length
                else:
                    if len(self._choice._cars_a) > 0:
                        c = self._choice._cars_a[-1].get_current_position_2d()
                        headway += math.sqrt( (c.x - b.x)**2 + (c.y - b.y)**2 )
                    else:
                        headway += self._choice._length
            return headway
        return self.leading_vehicle().get_current_position_1d() - self._current_position + self._length

    def leading_vehicle(self):
        if self.get_number_in_queue() == 0:
            return self
        if self._direction == "a":
            return self._road.get_car_a(self.get_number_in_queue() - 1)
        else:
            return self._road.get_car_b(self.get_number_in_queue() - 1)

    def choice(self):
        if ( self._direction == "a" ):
            choices = self._road._crossing_a._roads
        else:
            choices = self._road._crossing_b._roads

        # Weight probabilities, backwards road are less likely  
        return random.choices(list(choices), weights=[0 if road == self._road else 5 for road in choices], k=1)[0]

    # Getters
    def get_current_position_1d(self):
        return self._current_position

    def get_current_position_2d(self):
        a = self._road._crossing_a._position
        b = self._road._crossing_b._position

        if self._direction == "b":
            return a + (b-a) / self._road._length * self._current_position
        else:
            return b + (a-b) / self._road._length * self._current_position

    def get_current_position_2d_front(self):
        a = self._road._crossing_a._position
        b = self._road._crossing_b._position

        if self._direction == "b":
            return a + (b-a) / self._road._length * (self._current_position + self._length)
        else:
            return b + (a-b) / self._road._length * (self._current_position + self._length)


    def get_length(self):
        return self._length

    def get_number_in_queue(self):
        return self._road._cars_a.index(self) if self._direction == 'a' else self._road._cars_b.index(self)

    def get_color(self):
        color = Turbo.interpolate_or_clip_grey(self.headway() / (10.0*self._length))
        return color