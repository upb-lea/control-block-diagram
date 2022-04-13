from .electric_motor import ElectricMotor


class DcExtExMotor(ElectricMotor):
    """
        Externally Excited DC Motor with 4 inputs
    """
    def __init__(self, position, size=1.5, input: str = 'left', output: str = 'left',
                 orientation: str = 'bottom', input_space: float = 0.25, *args, **kwargs):
        """
            position:       position of the motor
            size:           size of the motor
            input:          side of the inputs
            output:         side of the output
            orientation:    orientation of the output shaft
            input_space:    space between the inputs
        """

        super().__init__(position, 'DC\nExt\nEx', size, input, 4, output, orientation, input_space, dict(), *args,
                         **kwargs)
