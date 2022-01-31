from control_block_diagram.predefined_components.predefined_components import PredefinedComponent
from control_block_diagram import Box, Connection, Text


class CoordinateTransformation(PredefinedComponent):

    def __init__(self, position, size, text_input, text_output, input: str = 'left', input_number: int = 2,
                 output: str = 'right', output_number: int = 2, in_out_space_right_left: float = 0,
                 in_out_space_top_bottom: float = 0, additional_input: str = '', additional_output: str = '', doc=None):
        super().__init__()
        self._box = Box(position, (size, size), inputs={input: input_number, additional_input: 1},
                        outputs={output: output_number, additional_output: 1},
                        in_out_space_right_left=in_out_space_right_left,
                        in_out_space_top_bottom=in_out_space_top_bottom)
        self._diagonal = Connection([self._box.bottom_left, self._box.top_right], arrow=False)

        pos_text_input = self._box.top_left.add(size / 4, -size / 4)
        pos_text_output = self._box.bottom_right.add(-size/4, size/4)
        if input in ['right', 'bottom']:
            (pos_text_input, pos_text_output) = (pos_text_output, pos_text_input)

        self._text_input = Text(text_input, position=pos_text_input)
        self._text_output = Text(text_output, position=pos_text_output)

        if doc is not None:
            doc.append(self)

    def build(self, pic):
        self._box.build(pic)
        self._diagonal.build(pic)
        self._text_input.build(pic)
        self._text_output.build(pic)