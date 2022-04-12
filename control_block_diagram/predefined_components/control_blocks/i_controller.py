from control_block_diagram.predefined_components import PredefinedComponent
from control_block_diagram.components import Box, Connection, Text


class IController(PredefinedComponent):
    def __init__(self, position, size: tuple = (1.5, 1), text: str = None, text_configuration: dict = {},
                 input: str = 'left', input_number: int = 1, output: str = 'right', output_number: int = 1,
                 additional_inputs: dict = dict(), additional_outputs: dict = dict(), input_space: float = 0.3,
                 output_space: float = 0.3, *args, **kwargs):
        super().__init__(position)
        additional_inputs[input] = input_number
        additional_inputs[input + '_space'] = input_space
        additional_outputs[output] = output_number
        additional_outputs[output + '_space'] = output_space
        self._box = Box(position, size=size, inputs=additional_inputs, outputs=additional_outputs, *args, **kwargs)
        self._connection1 = Connection([self._box.top_left.add(size[0] * 0.06, -size[1] * 0.09),
                                        self._box.bottom_left.add(size[0] * 0.06, size[1] * 0.09),
                                        self._box.bottom_right.add(-size[0] * 0.06, size[1] * 0.09)], arrow=False,
                                       *args, **kwargs)
        self._connection2 = Connection([self._box.bottom_left.add(size[0] * 0.06, size[1] * 0.09),
                                        self._box.top_right.add(-size[0] * 0.06, -size[1] * 0.2)], arrow=False,
                                       *args, **kwargs)

        if text is not None:
            self._text = Text(text, position.add_y(size[1]), text_configuration=text_configuration, *args, **kwargs)

        self.input = self._box.input_dict
        self.output = self._box.output_dict
        self.border = self._box.border
