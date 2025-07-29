from enum import Enum
from numbers import Number
from textwrap import indent

import numpy as np

from dimpy.basis import Basis


class DvecType(Enum):
    """
    DIMENSIONLESS: All dimensional exponents are zero.
    UNIFORM: All numerical values have the same units (so all rows of
        `Dvec.vector` are identical).
    RATIOED: Each numerical value differs from the preceding one by the same
        dimensioned constant.
    ARBITRARY: Any `Dvec` that does not fit one of these patterns.
    """

    # TODO: The units of a UNIFORM `Dvec` can be represented by one dimensional
    # constant, and the units of a RATIOED Dvec can be represented by two (a
    # base and a common ratio). This structure could be used to implement more
    # efficient comparisons of `Dvec`s and operations on them.
    DIMENSIONLESS = 0
    UNIFORM = 1
    RATIOED = 2
    ARBITRARY = 3


class Dvec:
    def __init__(
        self,
        vector: np.ndarray,
        basis: Basis,
    ):
        """Dimension vector.

        Parameters
        ----------
        vector : shape (n, m) | (m,)
            If (n, m), then the (i, j) entry is the exponent of jth unit of
            the basis for the ith numerical value.
        basis
            The instance of `Basis` used by the dimension vector. Must have m
            components.

        Attributes
        ----------
        vector
            The dimension vector. See description in Parameters section.
        basis
            The instance of `Basis` used by the dimension vector.
        n
            The number of numerical values.
        m
            The number of elements in `basis`.
        vectype
            The dimension vector type, taking one of the values of the
            `DvecType` enum.

        Examples
        --------
        Assume `basis` is (m, s, kg) in each of the following.

        - If `vector` is [[1, 2, 3], [-1, 0, 1]], then (n, m) = (2, 3).
        The 0th numerical value has units m s^2 kg^3 and
        the 1st numerical value has units kg / m.

        - If `vector` is [[1, 2, 3]], then (n, m) = (1, 3).
        The 0th (and only) numerical value has units m s^2 kg^3.

        - If `vector` is [1, 2, 3], then m = 3 and n is assumed to be 1.
        The 0th (and only) numerical value has units m s^2 kg^3.

        Notes
        -----
        If `vector.ndim == 1`, e.g., [1, 2, 3], an extra 0th dimension is
            added so that `vector` is [[1, 2, 3]].
        """
        # If `vector` has shape (m,), expand the 0th dimension so that its shape
        # is (1, m).
        if vector.ndim == 1:
            vector = np.expand_dims(vector, 0)
        Dvec._verify_inputs(vector, basis)

        self._vector = vector
        self._basis = basis
        self._n = self.vector.shape[0]
        self._vectype = Dvec._determine_vectype(vector)

    @property
    def vector(self):
        return self._vector

    @property
    def basis(self):
        return self._basis

    @property
    def n(self):
        return self._n

    @property
    def m(self):
        return self.basis.m

    @property
    def vectype(self):
        return self._vectype

    def __repr__(self):
        return (
            f"basis: {repr(self.basis)}"
            "\nvector:"
            f"\n{indent(repr(self.vector), ' ')}"
        )

    def __eq__(self, other):
        if not isinstance(other, Dvec):
            return False
        return self.basis == other.basis and np.allclose(
            self.vector, other.vector
        )

    def __add__(self, other):
        if not isinstance(other, Dvec):
            raise TypeError("right operand is not Dvec")
        if self.basis != other.basis:
            raise ValueError("left basis and right basis do not match")
        if self.n != other.n:
            raise ValueError(
                f"`left.n` ({self.n}) does not equal `right.n` ({other.n})"
            )

        # TODO: May be efficient to check certain conditions on the `vectype`s
        # that produce other `vectypes`.
        return Dvec(self.vector + other.vector, self.basis)

    def __sub__(self, other):
        return self + -1 * other

    def __mul__(self, other):
        if isinstance(other, Number):
            return Dvec(self.vector * other, self.basis)
        # TODO: This may need work.
        # TODO: Multiplication by dimensioned scalar
        # TODO: Element-wise multiplication
        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def _determine_vectype(vector):
        if np.allclose(0, vector):
            return DvecType.DIMENSIONLESS

        n = vector.shape[0]
        if n == 1:
            return DvecType.UNIFORM
        if np.allclose(vector[0], vector[1:]):
            return DvecType.UNIFORM

        if n == 2:
            return DvecType.RATIOED
        diffs = np.diff(vector, axis=0)
        if np.allclose(diffs[0], diffs[1:]):
            return DvecType.RATIOED

        return DvecType.ARBITRARY

    def _verify_inputs(vector, basis):
        if vector.shape[1] != basis.m:
            raise ValueError("`vector` and `basis` do not match sizes")
        if vector.ndim > 2:
            raise ValueError(
                "`vector` has too many dimensions (`vector.ndim` ="
                f" {vector.ndim} > 2)"
            )
