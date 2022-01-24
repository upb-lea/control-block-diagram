from .electric_motor import ElectricMotor


class SCIM(ElectricMotor):
    def __init__(self, position, size=1.5, input: str ='left', output: str = None, output_number: int = 0, doc=None):
        super().__init__(position, 'SCIM', size, input, 3, output, output_number, doc)
