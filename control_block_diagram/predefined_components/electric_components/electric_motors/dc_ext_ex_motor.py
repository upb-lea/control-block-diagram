from .electric_motor import ElectricMotor


class DcExtExMotor(ElectricMotor):
    def __init__(self, position, size=1.5, input: str = 'left', output: str = 'left',
                 orientation: str = 'bottom', input_space: float = 0.25, *args, **kwargs):

        super().__init__(position, 'DC\nExt\nEx', size, input, 4, output, orientation, input_space, dict(), *args,
                         **kwargs)
