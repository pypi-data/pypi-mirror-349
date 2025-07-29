class Basis:
    def __init__(self, units: tuple[str]):
        """

        Parameters
        ----------
        units
            A sequence of units represented by strings, e.g., ("m", "s", "kg"),
            (for meters, seconds, and kilograms).
        """
        Basis._verify_inputs(units)
        self._units = units
        self._m = len(self.units)

    @property
    def units(self):
        return self._units

    @property
    def m(self):
        return self._m

    def __eq__(self, other):
        if not isinstance(other, Basis):
            return False
        return self.units == other.units

    def __repr__(self):
        return str(self.units)

    def _verify_inputs(units):
        if len(units) == 0:
            raise ValueError("no units provided")
        if not all(isinstance(unit, str) for unit in units):
            raise ValueError("not all units are strings")
