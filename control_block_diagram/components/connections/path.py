from pylatex import TikZDraw, TikZUserPath, TikZOptions, TikZNode
from .connection import Connection
from ..points import Point


class Path(Connection):

    def __init__(self, points: [Point], angles: (list, tuple) = None, arrow: bool = True, text: (str, iter) = None,
                 text_position: (str, iter) = 'middle', text_align: (str, iter) = 'top', distance_x: float = 0.4,
                 distance_y: float = 0.2, doc=None):
        super().__init__(points, arrow, text, text_position, text_align, distance_x, distance_y, doc)
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
        text_position = self.get_text_position()
        for text, pos in zip(self._text, text_position):
            pic.append(TikZNode(text=text, at=pos, handle='box', options=self._text_kwargs))
