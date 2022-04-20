from .electric_motor import ElectricMotor


class DcExtExMotor(ElectricMotor):
    """
        Externally Excited DC Motor with 4 inputs
    """
    def __init__(self, position, size=1.5, input: str = 'left', output: str = 'left',
                 orientation: str = 'bottom', input_space: float = 0.25, *args, **kwargs):
        """
            :param position:       position of the motor
            :param size:           size of the motor
            :param input:          side of the inputs
            :param output:         side of the output
            :param orientation:    orientation of the output shaft
            :param input_space:    space between the inputs
        """

        super().__init__(position, 'DC\nExt\nEx', size, input, 4, output, orientation, input_space, dict(), *args,
                         **kwargs)
