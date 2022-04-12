from pylatex import TikZDraw, TikZUserPath, TikZOptions, TikZNode
from .connection import Connection
from ..points import Point


class Path(Connection):
    """
        Connection between list of points with different input and output angles
    """

    def __init__(self, points: [Point], angles: (list, tuple) = None, arrow: bool = True, text: str = None,
                 text_position: str = 'middle', text_align: str = 'top', distance_x: float = 0.4,
                 distance_y: float = 0.2, move_text: tuple = (0, 0), *args,
                 **kwargs):
        """
        Initilizes a path
            points:         list of points
            angles:         list of angles
            arrow:          arrow at the end of a path
            text:           text at a path
            text_position:  position of the text
            text_align:     align of the text
            distance_x:     distance of the text to the connection in x direction
            distance_y:     distance of the text to the connection in y direction
            move_text:      free movement of the text

        """
        super().__init__(points, arrow, text, text_position, text_align, distance_x, distance_y, move_text, *args,
                         **kwargs)
        self._angles = angles

    def build(self, pic):
        """Funtion to add the Latex code to the Latex document"""
        with pic.create(TikZDraw()) as path:
            path.append(self.tikz[0])
            for point, angle in zip(self.tikz[1:-1], self._angles):
                path.append(TikZUserPath('edge', TikZOptions(self._line_width, self._line_style, self._draw, **angle)))
                path.append(point)
                path.append(point)
            path.append(TikZUserPath('edge', TikZOptions(self._draw, self._line_width, self._line_style,
                                                         self._tikz_option, **self._angles[-1])))
            path.append(self._points[-1].tikz)
