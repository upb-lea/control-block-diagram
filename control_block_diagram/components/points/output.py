from .point import Point


class Output(Point):
    """
        Output of a block
    """
    def __init__(self, x: float, y: float, direction: str = None):
        """Initilizes an output"""
        super().__init__(x, y, direction)

    def __repr__(self):
        """represents an output"""
        return f'Output({self.x}, {self.y})'

    @staticmethod
    def convert(point: Point):
        """convert a point to an output"""
        return Output(point.x, point.y, point.direction)
