from .point import Point


class Center(Point):

    @property
    def horizontal(self):
        return self._horizontal

    @property
    def vertical(self):
        return self._vertical

    def __init__(self, x: float, y: float, direction: str = None, horizontal: bool = False, vertical: bool = False):
        super().__init__(x, y, direction)
        self._horizontal = horizontal
        self._vertical = vertical

    def __repr__(self):
        return f'Center({self.x}, {self.y})'

    @staticmethod
    def convert(point: Point, horizontal: bool = False, vertical: bool = False):
        return Center(point.x, point.y, point.direction, horizontal, vertical)
