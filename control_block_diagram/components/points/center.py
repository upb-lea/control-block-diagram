from .point import Point


class Center(Point):
    """
        Centered Point
    """

    @property
    def horizontal(self):
        """Returns wether the point is centered horizontal"""
        return self._horizontal

    @property
    def vertical(self):
        """Returns wether the point is centered vertical"""
        return self._vertical

    def __init__(self, x: float, y: float, direction: str = None, horizontal: bool = False, vertical: bool = False):
        """initializes a centered point"""
        super().__init__(x, y, direction)
        self._horizontal = horizontal
        self._vertical = vertical

    def __repr__(self):
        """represents a center"""
        return f'Center({self.x}, {self.y})'

    @staticmethod
    def convert(point: Point, horizontal: bool = False, vertical: bool = False):
        """convert a point to a center"""
        return Center(point.x, point.y, point.direction, horizontal, vertical)
