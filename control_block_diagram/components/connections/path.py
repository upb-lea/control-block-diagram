from pylatex import TikZDraw, TikZUserPath, TikZOptions, TikZNode
from .connection import Connection
from ..points import Point


class Path(Connection):

    def __init__(self, points: [Point], angles: (list, tuple) = None, arrow: bool = True, text: str = None,
                 text_position: str = 'middle', text_align: str = 'top', distance_x: float = 0.4,
                 distance_y: float = 0.2, move_text: tuple = (0, 0), **connection_configuration):
        super().__init__(points, arrow, text, text_position, text_align, distance_x, distance_y, move_text,
                         **connection_configuration)
        self._angles = angles

    def build(self, pic):
        with pic.create(TikZDraw()) as path:
            path.append(self.tikz[0])
            for point, angle in zip(self.tikz[1:-1], self._angles):
                path.append(TikZUserPath('edge', TikZOptions(self._line_width, self._draw, **angle)))
                path.append(point)
                path.append(point)
            path.append(TikZUserPath('edge', TikZOptions(self._draw, self._line_width, self._tikz_option,
                                                         **self._angles[-1])))
            path.append(self._points[-1].tikz)
