from pylatex import TikZNode, TikZCoordinate, TikZOptions
from ..component import Component
from control_block_diagram.components.points import Point


class Text(Component):

    def __init__(self, text: any = '', position: Point = Point(0, 0), size: tuple = (2, 2), color: str = 'black',
                 fontsize=r'\normalsize'):
        super().__init__()

        if text is None:
            text = ''

        self._text = Text.split_string(text)
        self._len_text = len(self._text)
        self._position = position
        self._size = size
        self._text_position = [TikZCoordinate(self._position.x,
                                              self._position[1] + self._size[1] / 2 - (i + 1) / (self._len_text + 1) *
                                              self._size[1]) for i in range(self._len_text)]
        self._color = color
        self._font_size = fontsize
        self._options = {'align': 'center', 'text width': str(self._size[0]) + 'cm', 'text': self._color,
                         'font': self._font_size}

    def define(self, **kwargs):
        self._position = kwargs.get('position', self._position)
        self._size = kwargs.get('size', self._size)
        self._font_size = kwargs.get('fontsize', self._font_size)
        self._options = {'align': 'center', 'text width': str(self._size[0]) + 'cm', 'text': self._color,
                         'font': self._font_size}
        top = self._position[1] + self._size[1] / 2
        self._text_position = [TikZCoordinate(self._position.x, top - (i + 1) / (self._len_text + 1) * self._size[1])
                               for i in range(self._len_text)]

    @staticmethod
    def split_string(string):
        if string.find('\n') == -1:
            return Text._split_rstring(string)
        else:
            return string.split('\n')

    @staticmethod
    def _split_rstring(string):
        liste = []
        new_string = ''
        for idx, c in enumerate(string):
            if c == '\\' and string[idx + 1] == 'n':
                liste.append(fr'{new_string}')
                new_string = ''
            elif c == 'n' and string[idx - 1] == '\\':
                pass

            elif idx == len(string) - 1:
                new_string = new_string + c
                liste.append(fr'{new_string}')
            else:
                new_string = new_string + c
        return liste

    def build(self, pic):
        for text, pos in zip(self._text, self._text_position):
            if text != '':
                pic.append(TikZNode(text=text, at=pos, handle='box', options=TikZOptions(self._options)))
