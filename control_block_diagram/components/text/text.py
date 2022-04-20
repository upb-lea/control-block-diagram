from pylatex import TikZNode, TikZCoordinate, TikZOptions
from ..component import Component
from control_block_diagram.components.points import Point


class Text(Component):
    """
        Class to write text in a block diagram
    """

    @property
    def top_left(self):
        """Returns the top left point of a text"""
        return self._position.add(-self._size[0] / 2, self._size[1] / 2)

    @property
    def top_right(self):
        """Returns the top right point of a text"""
        return self._position.add(self._size[0] / 2, self._size[1] / 2)

    @property
    def bottom_left(self):
        """Returns the bottom left point of a text"""
        return self._position.add(-self._size[0] / 2, -self._size[1] / 2)

    @property
    def bottom_right(self):
        """Returns the bottom right point of a text"""
        return self._position.add(self._size[0] / 2, -self._size[1] / 2)

    def __init__(self, text: str = '', position: Point = Point(0, 0), size: tuple = (2, 1),
                 text_configuration: dict = dict(), level: int = 0, *args, **kwargs):
        """
            Initializes a text
                text:               string of the text
                position:           position of the text
                size:               size of the text box
                text_configuration: visual presentation of the text (possible keys: text_color, fontsize, rotate)
                level:              level of the text
        """

        super().__init__(level, *args, **kwargs)

        if text is None:
            text = ''

        self._text = Text.split_string(text)    # split the text into lines
        self._len_text = len(self._text)        # get the number of lines
        self._position = position
        self._move_text = text_configuration.get('move_text', (0, 0))
        self._size = size

        # set the position of the text
        pos = self._position.add(*self._move_text)
        self._text_position = [TikZCoordinate(pos.x, pos[1] + self._size[1] / 2 - (i + 1) / (self._len_text + 1) *
                                              self._size[1]) for i in range(self._len_text)]
        self._set_border(self.top_left, self.top_right, self.bottom_left, self.bottom_right)

        # set the configuration of the text
        self._color = text_configuration.get('text_color', self._configuration['text_color'])
        self._font_size = text_configuration.get('fontsize', self._configuration['fontsize'])
        self._font = text_configuration.get('font', self._configuration['font'])
        self._rotate = text_configuration.get('rotate', 0)
        self._options = {'align': 'center', 'text width': str(self._size[0]) + 'cm', 'text': self._color,
                         'font': self._font_size + self._font, 'rotate': self._rotate}

    def define(self, **kwargs):
        """Function to change position and visual representation of the text afterwards"""
        self._position = kwargs.get('position', self._position)
        self._move_text = kwargs.get('move_text', self._move_text)
        self._size = kwargs.get('size', self._size)
        self._font_size = kwargs.get('fontsize', self._font_size)
        self._font = kwargs.get('font', self._font)
        self._rotate = kwargs.get('rotate', self._rotate)
        self._options = {'align': 'center', 'text width': str(self._size[0]) + 'cm', 'text': self._color,
                         'font': self._font_size + self._font, 'rotate': self._rotate}

        pos = self._position.add(*self._move_text)
        top = pos[1] + self._size[1] / 2
        self._text_position = [TikZCoordinate(pos.x, top - (i + 1) / (self._len_text + 1) * self._size[1])
                               for i in range(self._len_text)]

    @staticmethod
    def split_string(string: str):
        """Split a string into lines"""
        if string.find('\n') == -1:
            return Text._split_rstring(string)
        else:
            return string.split('\n')

    @staticmethod
    def _split_rstring(string: str):
        """Split a string into lines"""
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
        """Funtion to add the Latex code to the Latex document"""
        for text, pos in zip(self._text, self._text_position):
            if text != '':
                pic.append(TikZNode(text=text, at=pos, handle='box', options=TikZOptions(**self._options)))
