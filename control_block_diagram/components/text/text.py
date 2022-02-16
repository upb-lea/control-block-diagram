from pylatex import TikZNode, TikZCoordinate, TikZOptions
from ..component import Component
from control_block_diagram.components.points import Point


class Text(Component):

    def __init__(self, text: any, position: Point = Point(0, 0), size: tuple = (2, 2), color: str = 'black',
                 fontsize=r'\normalsize', doc=None):
        super().__init__(doc)
        if isinstance(text, (list, tuple)):
            self._text = text
        elif text is None:
            self._text = ['']
        else:
            self._text = [str(text)]

        self._len_text = len(self._text)
        self._position = position
        self._size = size
        self._text_position = [position.tikz]
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

    def build(self, pic):
        for text, pos in zip(self._text, self._text_position):
            pic.append(TikZNode(text=text, at=pos, handle='box', options=TikZOptions(self._options)))
