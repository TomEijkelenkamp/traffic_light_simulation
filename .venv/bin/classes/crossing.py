from bin.classes.light import Light

class Crossing:

    def __init__(self, point):
        self._position = point
        self._roads = set()
        self._lights = set()

    def get_position(self):
        return self._position

    def add_road(self, road):
        self._roads.add(road)
        self._lights.add( Light() )

    def get_position(self):
        return (self._position.x, self._position.y)

    def __eq__(self, __o: object) -> bool:
        return self._position == __o._position

    def __hash__(self) -> int:
        return hash(self._position)