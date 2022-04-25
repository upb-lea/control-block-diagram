from pylatex import TikZDraw, TikZOptions, TikZPathList
from ..block import Block
from ...points import Point
from ...text import Text


class CustomBlock(Block):
    """Block with a custom shape"""

    @property
    def points(self):
        """Returns the points of a custom block"""
        return self._points

    def __init__(self, points: [Point], text: (Text, str) = None, text_configuration: dict = dict(), level: int = 0,
                 *args, **kwargs):
        """
        Initialization of a custom block

            :param points:      list of the corner points of the block
            :param text:        text inside the block
            :param text_configuration: dictionary of arguments passed to the text
            :param level:       level of the component
        """

        x_val = [p.x for p in points]
        y_val = [p.y for p in points]
        size = (max(x_val) - min(x_val), max(y_val) - min(y_val))
        position = Point.get_mid(*points)

        super().__init__(position, text, size, text_configuration, level, *args, **kwargs)
        self._points = points

    def build(self, pic):
        """Funtion to add the Latex code to the Latex document"""
        points = []
        for p in self._points:
            points.extend([p.tikz, '--'])
        points.extend([self._points[0].tikz, '--', self._points[1].tikz])
        custom_block = TikZDraw(points, TikZOptions(*self._style_args, **self._tikz_options))
        pic.append(custom_block)
        super().build(pic)
