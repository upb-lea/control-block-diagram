from .point import Point


class Input(Point):
    def __init__(self, x: float, y: float, direction: str = None):
        super().__init__(x, y, direction)

    @staticmethod
    def convert(point: Point):
        return Input(point.x, point.y, point.direction)
