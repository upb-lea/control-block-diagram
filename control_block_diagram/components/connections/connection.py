from pylatex import TikZDraw, TikZUserPath, TikZOptions, TikZNode
from ..component import Component
from ..blocks import Circle
from ..points import Point
from .generate_connection import generate_connection


class Connection(Component):

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
                 distance_y: float = 0.2, line_width: str = 'thin'):
        super().__init__()
        self._points = points
        self._tikz_option = '-latex' if arrow else ''
        self._line_width = line_width
        self._text = []
        self._text_position = []
        self._text_align = []
        self._align_distance_x = []
        self._align_distance_y = []
        self._text_kwargs = {'align': 'center', 'text width': '2cm'}
        if text is not None:
            self.add_text(text, text_position, text_align, distance_x, distance_y)

    def __add__(self, other):
        return Connection(self._points + other.points, other.arrow)

    def append(self, point: Point):
        if isinstance(point, Point):
            self._points.append(point)

    def add_text(self, text, text_position: str = 'middle', text_align: str = 'top', distance_x: float = 0.4,
                 distance_y: float = 0.2):
        if isinstance(text, str) and isinstance(text_position, (str, tuple, list)) and isinstance(text_align, str):
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
            path.append(self.tikz[0])
            for point in self.tikz[1:-1]:
                path.append(TikZUserPath('edge', TikZOptions(self._line_width)))
                path.append(point)
                path.append(point)
            path.append(TikZUserPath('edge', TikZOptions(self._tikz_option, self._line_width)))
            path.append(self._points[-1].tikz)

        text_position = self.get_text_position()
        for text, pos in zip(self._text, text_position):
            pic.append(TikZNode(text=text, at=pos, handle='box', options=self._text_kwargs))

    def get_text_position(self):
        positions = []
        for text_pos, align, distance_x, distance_y in zip(self._text_position, self._text_align,
                                                           self._align_distance_x, self._align_distance_y):
            if isinstance(text_pos, (list, tuple)):
                p1, p2 = self._points[text_pos[0]: text_pos[0] + 2]
                if text_pos[1] == 'start':
                    pos = p1
                elif text_pos == 'end':
                    pos = p2
                else:
                    pos = Point.get_mid(p1, p2)

            elif text_pos == 'start':
                pos = self._points[0]
            elif text_pos == 'end':
                pos = self._points[-1]
            else:
                if len(self._points) % 2 == 0:
                    p1 = self._points[int(len(self._points) / 2) - 1]
                    p2 = self._points[int(len(self._points) / 2)]
                    pos = Point.get_mid(p1, p2)
                else:
                    pos = self._points[int(len(self._points) / 2)]

            align = align.split('_', 1)
            if 'left' in align:
                pos = pos.sub_x(distance_x)
            if 'right' in align:
                pos = pos.add_x(distance_x)
            if 'top' in align:
                pos = pos.add_y(distance_y)
            if 'bottom' in align:
                pos = pos.sub_y(distance_y)

            positions.append(pos.tikz)
        return positions

    @staticmethod
    def connect(p1: Point, p2: Point, space_x: float = 1, space_y: float = 1, arrow: bool = True,
                line_width: str = 'thin', text: (str, iter) = None, text_position: (str, iter) = 'middle',
                text_align: (str, iter) = 'top', distance_x: float = 0.4,  distance_y: float = 0.2,
                start_direction: str = None, end_direction: str = None, doc=None):
        if isinstance(p1, (list, tuple)) and isinstance(p2, (list, tuple)):
            if isinstance(text, (list, tuple)):
                return [Connection.connect(p1_, p2_, space_x, space_y, arrow, line_width, text_, text_position,
                                           text_align, distance_x, distance_y, start_direction, end_direction, doc)
                        for p1_, p2_, text_ in zip(p1, p2, text)]
            else:
                return [Connection.connect(p1_, p2_, space_x, space_y, arrow, line_width, text, text_position,
                                           text_align, distance_x, distance_y, start_direction, end_direction, doc)
                        for p1_, p2_ in zip(p1, p2)]
        else:
            connection = Connection(generate_connection(p1, p2, space_x, space_y, start_direction, end_direction),
                                    arrow, line_width=line_width)
            if text is not None:
                connection.add_text(text, text_position, text_align, distance_x, distance_y)
            return connection

    @staticmethod
    def connect_to_line(con, point, arrow=True, line_width: str = 'thin', text: (str, iter) = None,
                        text_position: (str, iter) = 'middle', text_align: (str, iter) = 'top', distance_x: float = 0.4,
                        distance_y: float = 0.2, fill='black', draw=0.1):
        if isinstance(con, (list, tuple)) and isinstance(point, (list, tuple)):
            if isinstance(text, (list, tuple)):
                return [Connection.connect_to_line(con_, point_, arrow, line_width, text_, text_position, text_align,
                                                   distance_x, distance_y, fill, draw) for con_, point_, text_ in
                        zip(con, point, text)]
            else:
                return [Connection.connect_to_line(con_, point_, arrow, line_width, text, text_position, text_align,
                                                   distance_x, distance_y, fill, draw)
                        for con_, point_ in zip(con, point)]
        else:
            if con.begin.x == con.end.x:
                point_start = Point.merge(con.begin, point)
                if point_start.x > point.x:
                    output = 'left'
                else:
                    output = 'right'
            elif con.begin.y == con.end.y:
                point_start = Point.merge(point, con.begin)
                if point_start.y > point.y:
                    output = 'top'
                else:
                    output = 'bottom'
            else:
                raise Exception("Line and Point can't be connected")

            if isinstance(draw, float):
                circle = Circle(point_start, radius=draw, fill=fill, outputs={output: 1})
                point_start = circle.output[0]

            return Connection.connect(point_start, point, arrow=arrow, line_width=line_width, text=text,
                                      text_position=text_position, text_align=text_align, distance_x=distance_x,
                                      distance_y=distance_y)
