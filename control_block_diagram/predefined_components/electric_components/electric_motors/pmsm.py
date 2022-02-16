from .electric_motor import ElectricMotor


class PMSM(ElectricMotor):
    def __init__(self, position, size=1.5, input: str = 'left', output: str = 'left', orientation: str = 'bottom',
                 input_space: float = 0.3, doc=None):
        super().__init__(position, ['PMSM'], size, input, 3, output, orientation, input_space)
