from classes.orientation import Orientation

class Light:

    def __init__(self, crossing, road, orientation):
        self._state = 'G' if orientation == Orientation.N else 'R'
        self._crossing = crossing
        self._road = road
        self._orientation = orientation
        self._position = self._crossing.get_position()
        if self._orientation == Orientation.N:
            self._position = (self._position[0], self._position[1] - 20)
        elif self._orientation == Orientation.E:
            self._position = (self._position[0] + 20, self._position[1])
        elif self._orientation == Orientation.S:
            self._position = (self._position[0], self._position[1] + 20)
        elif self._orientation == Orientation.W:
            self._position = (self._position[0] - 20, self._position[1])

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def get_position(self):
        return self._position

    def get_color(self):
        return (50, 164, 49) if self._state == 'G' else (187, 30, 16)

    def get_road(self):
        return self._road

    