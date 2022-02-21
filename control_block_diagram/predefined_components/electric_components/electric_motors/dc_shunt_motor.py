from .electric_motor import ElectricMotor


class DcShuntMotor(ElectricMotor):
    def __init__(self, position, input: str = 'left', output: str = 'left', orientation: str = 'bottom',
                 input_space: float = 0.3):
        super().__init__(position, 'DC\nShunt\nMotor', 1.5, input, 1, output, orientation, input_space)
