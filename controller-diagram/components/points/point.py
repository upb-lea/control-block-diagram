from pylatex import TikZCoordinate


class Point:

    @property
    def coordinate(self):
        return self._coordinate

    @property
    def tikz(self):
        return TikZCoordinate(self.x, self.y)

    @property
    def x(self):
        return self._coordinate[0]

    @property
    def y(self):
        return self._coordinate[1]

    @property
    def direction(self):
        return self._direction

    def __init__(self, x: float, y: float, direction: str = None):
        self._coordinate = (x, y)
        self._direction = direction if direction in ['north', 'west', 'south', 'east'] else False

    def __add__(self, other):
        if isinstance(other, list):
            return [self] + other

        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def __getitem__(self, item):
        return self._coordinate[item]

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def add(self, x: float, y: float, direction: str = None):
        return Point(self.x + x, self.y + y, direction)

    def add_x(self, val: float, direction: str = None):
        return Point(self.x + val, self.y, direction)

    def add_y(self, val: float, direction: str = None):
        return Point(self.x, self.y + val, direction)

    @staticmethod
    def merge(p1, p2):
        return Point(p1.x, p2.x)

    @staticmethod
    def get_mid(p1, p2):
        return Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
      
