from pylatex import TikZDraw, TikZUserPath, TikZOptions, TikZNode
from .connection import Connection
from ..points import Point
from ..text import Text


class Path(Connection):

    def __init__(self, points: [Point], angles: (list, tuple) = None, arrow: bool = True, text: str = None,
                 text_position: str = 'middle', text_align: str = 'top', distance_x: float = 0.4,
                 distance_y: float = 0.2):
        super().__init__(points, arrow, text, text_position, text_align, distance_x, distance_y)
        self._angles = angles

    def build(self, pic):
        with pic.create(TikZDraw()) as path:
            path.append(self.tikz[0])
            for point, angle in zip(self.tikz[1:-1], self._angles):
                path.append(TikZUserPath('edge', TikZOptions(**angle)))
                path.append(point)
                path.append(point)
            path.append(TikZUserPath('edge', TikZOptions(self._tikz_option, **self._angles[-1])))
            path.append(self._points[-1].tikz)
