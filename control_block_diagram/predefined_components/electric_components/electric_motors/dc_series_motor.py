from .electric_motor import ElectricMotor


class DcSeriesMotor(ElectricMotor):
    """
        DC Series Motor with 2 inputs
    """

    def __init__(self, position, size=1.5, input: str = 'left', output: str = 'left', orientation: str = 'bottom',
                 input_space: float = 0.3, *args, **kwargs):
        """
            position:       position of the motor
            size:           size of the motor
            input:          side of the inputs
            output:         side of the output
            orientation:    orientation of the output shaft
            input_space:    space between the inputs
        """

        super().__init__(position, 'DC\nSeries', size, input, 2, output, orientation, input_space, *args, **kwargs)