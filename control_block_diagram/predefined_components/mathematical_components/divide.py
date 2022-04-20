from ..predefined_components import PredefinedComponent
from control_block_diagram.components import Box


class Divide(PredefinedComponent):
    """
        Rectangular divide block
    """

    def __init__(self, position, size: (tuple, list) = (0.4, 0.8), inputs: str = 'left', input_space=0.4,
                 operations='*/', text_configuration: dict = dict(), box_kwargs: dict = dict(), *args, **kwargs):
        """
        Initializes a divide block
            :param position:       position of the block
            :param size:           size of the block
            :param inputs:         side of the inputs
            :param input_space:    space between the inputs
            :param operations:     string of operations
            :param text_configuration: arguments passed to the text
            :param box_kwargs:     arguments passsed to the box

        """
        super().__init__(position)

        if inputs == 'left':
            output = 'right'
        elif inputs == 'right':
            output = 'left'
        elif inputs == 'bottom':
            output = 'top'
        elif inputs == 'top':
            output = 'bottom'
        else:
            raise Exception(f'{inputs} is an invalid side for the inputs.')

        input_text = []
        for op in operations:
            if op == '*':
                input_text.append(r'$\times$')
            elif op == '/':
                input_text.append(r'$\div$')

        self._box = Box(position, size, inputs={inputs: len(input_text), inputs + '_text': input_text,
                                                inputs + '_space': input_space, inputs + '_text_space': 0.2},
                        outputs={output: 1}, text_configuration=text_configuration, *args, **box_kwargs, **kwargs)

        self.input = self._box.input_dict
        self.output = self._box.output_dict
        self.border = self._box.border
