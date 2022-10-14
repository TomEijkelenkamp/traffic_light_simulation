
from enum import Enum


class Orientation(Enum):
    N = 0
    E = 1
    S = 2
    W = 3

    def next(self):
        return Orientation((self.value + 1) % 4)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)