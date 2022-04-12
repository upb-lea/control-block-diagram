from .point import Point


class Input(Point):
    """
        Input of a block
    """
    def __init__(self, x: float, y: float, direction: str = None):
        """initializes an input"""
        super().__init__(x, y, direction)

    def __repr__(self):
        """represents an input"""
        return f'Input({self.x}, {self.y})'

    @staticmethod
    def convert(point: Point):
        """convert a point to an input"""
        return Input(point.x, point.y, point.direction)
