from .electric_motor import ElectricMotor


class DcExtExMotor(ElectricMotor):
    def __init__(self, position, size=1.5, input: (list, tuple) = ['left', 'right'], output: str = 'left',
                 orientation: str = 'bottom', input_space: float = 0.3):
        additional_inputs = dict()
        additional_inputs[input[1]] = 2
        additional_inputs[input[1] + '_space'] = input_space
        super().__init__(position, 'DC\nExt\nEx', size, input[0], 2, output, orientation, input_space,
                         additional_inputs)