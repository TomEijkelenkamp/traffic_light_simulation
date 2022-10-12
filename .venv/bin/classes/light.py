
class Light:

    def __init__(self):
        self._state = False

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def toggle(self):
        self._state = not self._state

    def __str__(self):
        return 'Light is ' + str(self._state)

    def __repr__(self):
        return 'Light(' + str(self._state) + ')'