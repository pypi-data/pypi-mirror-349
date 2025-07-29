from textwrap import indent

import numpy as np

import dimpy.ufuncs as ufuncs
from dimpy.dimension_vector import Dvec


def _array_ufunc_(ufunc, method, *inputs, **kwargs):
    print(ufunc, end="\n\n")
    print(method, end="\n\n")
    print(inputs, end="\n\n")
    print(kwargs, end="\n\n")

    if ufunc in ufuncs.HANDLED_UFUNCS:
        return ufuncs.HANDLED_UFUNCS[ufunc](*inputs)
    else:
        return NotImplemented


class Darray(np.lib.mixins.NDArrayOperatorsMixin):
    def __init__(self, num: np.ndarray, dimension_vectors: Dvec | tuple[Dvec]):
        """Dimensioned array."""
        if isinstance(dimension_vectors, Dvec):
            dimension_vectors = (dimension_vectors,)
        Darray._verify_inputs(num, dimension_vectors)

        self._num = num
        self._basis = dimension_vectors[0].basis
        self._dvecs = dimension_vectors

    @property
    def num(self):
        return self._num

    @property
    def dvecs(self):
        return self._dvecs

    @property
    def basis(self):
        return self._basis

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        return _array_ufunc_(ufunc, method, *inputs, **kwargs)

    def __repr__(self):
        # TODO: Include dimension vectors. It'd be neat to have it format
        # alongside the numpy array.
        return (
            f"num:\n{indent(str(self.num), ' ')}\n"
            f"basis: {str(self.dvecs[0].basis)}"
        )

    def _verify_inputs(num, dvecs):
        # TODO: Define custom exceptions? Maybe for basis mismatch?
        # TODO: Split this into multiple methods.
        # Type checks
        if not isinstance(num, np.ndarray):
            raise ValueError("`num` must be `np.ndarray`")
        if any(not isinstance(item, Dvec) for item in dvecs):
            raise ValueError(
                "`dimension_vectors` must be `Dvec` or tuple of `Dvec`s"
            )

        # Check the number of dimensions
        if num.ndim != len(dvecs):
            raise ValueError(
                "`num.ndim` is not equal to the number of dimension vectors"
            )

        # Check the length of each dimension vector against that of num
        for axis in range(num.ndim):
            if num.shape[axis] != dvecs[axis].n:
                raise ValueError(
                    f"axis {axis} of `num` and length of dimension"
                    f" vector {axis} differ ({num.shape[axis]} !="
                    f" {dvecs[axis].n})"
                )

        # Check that each dimension vector uses the same basis
        for i, dim_vec in enumerate(dvecs[1:]):
            if dvecs[0].basis != dim_vec.basis:
                raise ValueError(
                    f"`dimension_vectors[{i}].basis` is different"
                    " from the other dimension vector bases"
                )
