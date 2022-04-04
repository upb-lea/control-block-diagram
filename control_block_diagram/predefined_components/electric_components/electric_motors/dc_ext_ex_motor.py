from .electric_motor import ElectricMotor


class DcExtExMotor(ElectricMotor):
    def __init__(self, position, size=1.5, input: (list, tuple) = ['left', 'right'], output: str = 'left',
                 orientation: str = 'bottom', input_space: float = 0.25):

        super().__init__(position, 'DC\nExt\nEx', size, input, 4, output, orientation, input_space, dict())
