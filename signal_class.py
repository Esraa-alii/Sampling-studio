class Signal():
    """
    A class used to represent a Signal

    ...

    Attributes
    ----------
    amplitude : float
        the amplitude of the signal
    frequency : float
        the frequancy of the signal
    phase : float
        the phase of the signal

    
    """

    def __init__(self, amplitude, frequency, phase):
        """
        Parameters
        ----------
        amplitude : float
            the amplitude of the signal
        frequency : float
            the frequancy of the signal
        phase : float
            the phase of the signal
        """
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase