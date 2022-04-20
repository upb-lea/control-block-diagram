from pylatex import TikZCoordinate


class Point:
    """
        Class that represents 2D-coordinates
    """

    @property
    def coordinate(self):
        """Returns the coordinate of a point"""
        return self._coordinate

    @property
    def tikz(self):
        """Returns the tikz coordinate of a point"""
        return TikZCoordinate(self.x, self.y)

    @property
    def x(self):
        """Returns the x coordinate of a point"""
        return self._coordinate[0]

    @property
    def y(self):
        """Returns the y coordinate of a point"""
        return self._coordinate[1]

    @property
    def direction(self):
        """Returns the direction of a point"""
        return self._direction

    @property
    def abs(self):
        """Returns the length of a point"""
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __init__(self, x: float, y: float, direction: str = None):
        """
        Initilizes a point
            :param x:          x coordinate of the point
            :param y:          y coordinate of the point
            :param direction:  direction of the point
        """

        self._coordinate = (x, y)
        self._direction = direction if direction in ['north', 'west', 'south', 'east'] else False

    def __add__(self, other):
        """add two points"""
        if isinstance(other, list):
            return [self] + other

        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """subtract two points"""
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """multily a point by a scalar"""
        return Point(self.x * other, self.y * other)

    def __truediv__(self, other):
        """divide a point by a scalar"""
        return Point(self.x / other, self.y / other)

    def __getitem__(self, item):
        """get one coordinate of the point"""
        return self._coordinate[item]

    def __repr__(self):
        """represents a point"""
        return f'Point({self.x}, {self.y})'

    def add(self, x: float, y: float, direction: str = None):
        """add scalars to a point"""
        return Point(self.x + x, self.y + y, direction)

    def add_x(self, val: float, direction: str = None):
        """add a scalar to the x coordinate"""
        return Point(self.x + val, self.y, direction)

    def add_y(self, val: float, direction: str = None):
        """add a scalar to the y coordinate"""
        return Point(self.x, self.y + val, direction)

    def sub(self, x: float, y: float, direction: str = None):
        """substract scalars from a point"""
        return Point(self.x - x, self.y - y, direction)

    def sub_x(self, val: float, direction: str = None):
        """substract a scalar from the x coordinate"""
        return Point(self.x - val, self.y, direction)

    def sub_y(self, val: float, direction: str = None):
        """substract a scalar from the y coordinate"""
        return Point(self.x, self.y - val, direction)

    @staticmethod
    def merge(p1, p2):
        """get a new point with the x-coordinate of the first point and y-coordinate of the second point"""
        return Point(p1.x, p2.y)

    @staticmethod
    def get_mid(*points):
        """calculate the middle between multiple points"""
        x_mid = sum([p.x for p in points]) / len(points)
        y_mid = sum([p.y for p in points]) / len(points)
        return Point(x_mid, y_mid)
