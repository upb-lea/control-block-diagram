from pylatex import TikZDraw, TikZUserPath, TikZOptions, TikZNode
from ..component import Component
from ..blocks import Circle
from ..points import Point
from ..text import Text
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

    def __init__(self, points: [Point], arrow: bool = True, text: str = None,
                 text_position: str = 'middle', text_align: str = 'top', distance_x: float = 0.4,
                 distance_y: float = 0.2, move_text: tuple = (0, 0), **connection_configuration):
        super().__init__()
        self._points = points
        self._set_border(*self._points)
        self._tikz_option = '-latex' if arrow else ''
        self._line_width = connection_configuration.get('line_width', self._configuration['line_width'])
        self._draw = connection_configuration.get('draw', self._configuration['draw'])
        self._text = Text(text, self.get_text_position(text_position, text_align, distance_x, distance_y, move_text))

    def __add__(self, other):
        return Connection(self._points + other.points, other.arrow)

    def append(self, point: Point):
        if isinstance(point, Point):
            self._points.append(point)

    def reverse(self):
        self._points.reverse()

    def build(self, pic):
        with pic.create(TikZDraw()) as path:
            path.append(self.tikz[0])
            for point in self.tikz[1:-1]:
                path.append(TikZUserPath('edge', TikZOptions(self._draw, self._line_width)))
                path.append(point)
                path.append(point)
            path.append(TikZUserPath('edge', TikZOptions(self._draw, self._line_width, self._tikz_option)))
            path.append(self._points[-1].tikz)

    def get_text_position(self, text_pos, align, distance_x, distance_y, move_text):

        if isinstance(text_pos, (list, tuple)):
            p1, p2 = self._points[text_pos[0]: text_pos[0] + 2]
            if text_pos[1] == 'start':
                position = p1
            elif text_pos == 'end':
                position = p2
            else:
                position = Point.get_mid(p1, p2)

        elif text_pos == 'start':
            position = self._points[0]
        elif text_pos == 'end':
            position = self._points[-1]
        else:
            if len(self._points) % 2 == 0:
                p1 = self._points[int(len(self._points) / 2) - 1]
                p2 = self._points[int(len(self._points) / 2)]
                position = Point.get_mid(p1, p2)
            else:
                position = self._points[int(len(self._points) / 2)]

        align = align.split('_', 1)
        if 'left' in align:
            position = position.sub_x(distance_x)
        if 'right' in align:
            position = position.add_x(distance_x)
        if 'top' in align:
            position = position.add_y(distance_y)
        if 'bottom' in align:
            position = position.sub_y(distance_y)

        position = position.add(*move_text)

        return position

    @staticmethod
    def connect(p1: Point, p2: Point, space_x: float = 1, space_y: float = 1, arrow: bool = True,
                text: (str, iter) = None, text_position: (str, iter) = 'middle',
                text_align: (str, iter) = 'top', distance_x: float = 0.4,  distance_y: float = 0.25,
                move_text: tuple = (0, 0), start_direction: str = None, end_direction: str = None,
                **connection_configuration):
        if isinstance(p1, (list, tuple)) and isinstance(p2, (list, tuple)):
            if isinstance(text, (list, tuple)):
                return [Connection.connect(p1_, p2_, space_x, space_y, arrow, text_, text_position,
                                           text_align, distance_x, distance_y, move_text, start_direction,
                                           end_direction, **connection_configuration)
                        for p1_, p2_, text_ in zip(p1, p2, text)]
            else:
                return [Connection.connect(p1_, p2_, space_x, space_y, arrow, text, text_position,
                                           text_align, distance_x, distance_y, move_text, start_direction,
                                           end_direction, **connection_configuration)
                        for p1_, p2_ in zip(p1, p2)]
        else:
            connection = Connection(generate_connection(p1, p2, space_x, space_y, start_direction, end_direction),
                                    arrow, text=text, text_position=text_position,
                                    text_align=text_align, distance_x=distance_x, distance_y=distance_y,
                                    move_text=move_text, **connection_configuration)

            return connection

    @staticmethod
    def connect_to_line(con, point, arrow: bool = True, text: (str, iter) = None,
                        text_position: (str, iter) = 'middle', text_align: (str, iter) = 'top', distance_x: float = 0.4,
                        distance_y: float = 0.25, move_text: tuple = (0, 0), fill='black', draw=0.05, section=0,
                        **connection_configuration):
        if isinstance(con, (list, tuple)) and isinstance(point, (list, tuple)):
            if isinstance(text, (list, tuple)):
                return [Connection.connect_to_line(con_, point_, arrow, text_, text_position, text_align,
                                                   distance_x, distance_y, move_text, fill, draw,
                                                   **connection_configuration)
                        for con_, point_, text_ in zip(con, point, text)]
            else:
                return [Connection.connect_to_line(con_, point_, arrow, text, text_position, text_align,
                                                   distance_x, distance_y, move_text, fill, draw,
                                                   **connection_configuration)
                        for con_, point_ in zip(con, point)]
        else:
            if section >= len(con.points) - 1:
                raise Exception(f'Line has no {section} sections')
            else:
                begin = con.points[section]
                end = con.points[section + 1]

            if begin.x == end.x:
                point_start = Point.merge(begin, point)
                if point_start.x > point.x:
                    output = 'left'
                else:
                    output = 'right'
            elif begin.y == end.y:
                point_start = Point.merge(point, begin)
                if point_start.y > point.y:
                    output = 'bottom'
                else:
                    output = 'top'
            else:
                raise Exception("Line and Point can't be connected")

            if isinstance(draw, float):
                circle = Circle(point_start, radius=draw, fill=fill, outputs={output: 1})
                point_start = circle.output[0]

            return Connection.connect(point_start, point, arrow=arrow, text=text,
                                      text_position=text_position, text_align=text_align, distance_x=distance_x,
                                      distance_y=distance_y, move_text=move_text, **connection_configuration)
