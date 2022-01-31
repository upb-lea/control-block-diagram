from .electric_motor import ElectricMotor


class DcShuntMotor(ElectricMotor):
    def __init__(self, position, input: str = 'left', output: str = 'right', output_number: int = 0, doc=None):
        super().__init__(position, ['DC', 'Shunt', 'Motor'], 1.5, input, 1, output, output_number, doc)
