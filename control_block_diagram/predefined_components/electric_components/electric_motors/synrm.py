from .electric_motor import ElectricMotor


class SynRM(ElectricMotor):
    """
        Synchronous Reluctance Motor with 3 inputs
    """

    def __init__(self, position, size=1.5, input: str = 'left', output: str = 'left', orientation: str = 'bottom',
                 input_space: float = 0.3, *args, **kwargs):
        """
            :param position:       position of the motor
            :param size:           size of the motor
            :param input:          side of the inputs
            :param output:         side of the output
            :param orientation:    orientation of the output shaft
            :param input_space:    space between the inputs
        """

        super().__init__(position, 'SynRM', size, input, 3, output, orientation, input_space, *args, **kwargs)
