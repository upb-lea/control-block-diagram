from .electric_motor import ElectricMotor


class PMSM(ElectricMotor):
    def __init__(self, position, size=1.5, input: str = 'left', output: str = 'right', output_number: int = 2,
                 doc=None):
        super().__init__(position, ['PMSM'], size, input, 3, output, output_number, doc)
