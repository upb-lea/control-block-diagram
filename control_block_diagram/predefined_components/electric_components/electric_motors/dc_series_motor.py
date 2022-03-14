from .electric_motor import ElectricMotor


class DcSeriesMotor(ElectricMotor):
    def __init__(self, position, size=1.5, input: str = 'left', output: str = 'left', orientation: str = 'bottom',
                 input_space: float = 0.3):
        super().__init__(position, 'DC\nSeries', size, input, 2, output, orientation, input_space)