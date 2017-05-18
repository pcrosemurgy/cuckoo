import math
import time

class TouchHandler:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._t = 0

    def press(self, x, y):
        self._x = x
        self._y = y
        self._t = time.time()

    def release(self, x, y):
        d = math.sqrt((self._x-x)**2+(self._y-y)**2)
        if d > 50:
            return 'drag'
        elif time.time()-self._t < 0.5:
            return 'short'
        else:
            return 'long'
