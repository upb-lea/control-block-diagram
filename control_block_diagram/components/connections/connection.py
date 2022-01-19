from pylatex import TikZDraw, TikZUserPath, TikZOptions, TikZNode
from ..points import Point
from .generate_connection import generate_connection


class Connection:

    @property
    def points(self):
        return self._points

    @property
    def tikz(self):
        return [point.tikz for point in self._points]

    @property
    def arrow(self):
        return self._tikz_option == '-latex'

    @arrow.setter
    def arrow(self, val: bool):
        self._tikz_option = '-latex' if val else ''

    @property
    def begin(self):
        return self._points[0]

    @property
    def end(self):
        return self._points[-1]

    def __init__(self, points: [Point], arrow: bool = True, text: (str, iter) = None,
                 text_position: (str, iter) = 'middle', text_align: (str, iter) = 'top', distance_x: float = 0.4,
                 distance_y: float = 0.2, doc=None):
        self._points = points
        self._tikz_option = '-latex' if arrow else ''
        self._text = []
        self._text_position = []
        self._text_align = []
        self._align_distance_x = []
        self._align_distance_y = []
        self._text_kwargs = {'align': 'center', 'text width': '2cm'}
        if text is not None:
            self.add_text(text, text_position, text_align, distance_x, distance_y)

        if doc is not None:
            doc.append(self)

    def __add__(self, other):
        return Connection(self._points + other.points, other.arrow)

    def append(self, point: Point):
        if isinstance(point, Point):
            self._points.append(point)

    def add_text(self, text, text_position: str = 'middle', text_align: str = 'top', distance_x: float = 0.4,
                 distance_y: float = 0.2):
        if isinstance(text, str) and isinstance(text_position, str) and isinstance(text_align, str):
            self._text.append(text)
            self._text_position.append(text_position)
            self._text_align.append(text_align)
            self._align_distance_x.append(distance_x)
            self._align_distance_y.append(distance_y)
        elif isinstance(text, (list, tuple)) and isinstance(text_position, (list, tuple)) and isinstance(text_align,
                                                                                                         (list, tuple)):
            for _text, _text_position, _text_align in zip(text, text_position, text_align):
                self.add_text(_text, _text_position, _text_align, distance_x, distance_y)

    def reverse(self):
        self._points.reverse()

    def build(self, pic):
        with pic.create(TikZDraw()) as path:
            path.append(self._points[0].tikz)
            for point in self.tikz[1:-1]:
                path.append(TikZUserPath('edge', TikZOptions()))
                path.append(point)
                path.append(point)
            path.append(TikZUserPath('edge', TikZOptions(self._tikz_option)))
            path.append(self._points[-1].tikz)
        text_position = self.get_text_position()
        for text, pos in zip(self._text, text_position):
            pic.append(TikZNode(text=text, at=pos, handle='box', options=self._text_kwargs))

    def get_text_position(self):
        positions = []
        for text_pos, align, distance_x, distance_y in zip(self._text_position, self._text_align,
                                                           self._align_distance_x, self._align_distance_y):
            if text_pos == 'start':
                pos = self._points[0]
            elif text_pos == 'end':
                pos = self._points[-1]
            else:
                p1 = self._points[int(len(self._points) / 2) - 1]
                p2 = self._points[int(len(self._points) / 2)]
                pos = Point.get_mid(p1, p2)

            align = align.split('_', 1)
            if 'left' in align:
                pos = pos.add_x(-distance_x)
            if 'right' in align:
                pos = pos.add_x(distance_x)
            if 'top' in align:
                pos = pos.add_y(distance_y)
            if 'bottom' in align:
                pos = pos.add_y(-distance_y)

            positions.append(pos.tikz)
        return positions

    @staticmethod
    def connect(p1: Point, p2: Point, space_x: float = 1, space_y: float = 1, arrow: bool = True,
                text: (str, iter) = None, text_position: (str, iter) = 'middle', text_align: (str, iter) = 'top',
                distance_x: float = 0.4,  distance_y: float = 0.2, start_direction: str = None,
                end_direction: str = None, doc=None):
        if isinstance(p1, (list, tuple)) and isinstance(p2, (list, tuple)):
            return [Connection.connect(p1_, p2_, space_x, space_y, arrow, text, text_position, text_align,
                                       distance_x, distance_y, start_direction, end_direction, doc) for p1_, p2_ in zip(p1, p2)]
        else:
            connection = Connection(generate_connection(p1, p2, space_x, space_y, start_direction, end_direction), arrow, doc=doc)
            if text is not None:
                connection.add_text(text, text_position, text_align, distance_x, distance_y)
            return connection
