from numbers import Number

import numpy as np

# Cannot use imports like `from dimpy import ...` due to circular imports.
import dimpy.dimensioned_array as da

# TODO: There's a lot of work to do with broadcasting, if even possible.
# TODO: If Dvecs are dimensionless, uniform, or ratioed, we can shortcut some
# Dvec computations.
HANDLED_UFUNCS = dict()


def implements(np_ufunc):
    def decorator(func):
        HANDLED_UFUNCS[np_ufunc] = func
        return func

    return decorator


@implements(np.positive)
def _positive(input, **kwargs):
    return da.Darray(input.num, input.dvecs)


@implements(np.negative)
def _negative(input, **kwargs):
    return da.Darray(-input.num, input.dvecs)


@implements(np.add)
def _add(left, right, **kwargs):
    # TODO: Broadcast.
    if left.dvecs != right.dvecs:
        raise ValueError("left and right dimension vectors do not match")

    return da.Darray(left.num + right.num, left.dvecs)


@implements(np.subtract)
def _subtract(left, right, **kwargs):
    return _add(left, -right, **kwargs)


@implements(np.multiply)
def _multiply(left, right, **kwargs):
    if isinstance(left, Number):
        left, right = right, left

    if isinstance(right, Number):
        return da.Darray(left.num * right, left.dvecs)

    if left.basis != right.basis:
        raise ValueError("operands use different bases")
    # TODO: Broadcast.
    if left.num.shape != right.num.shape:
        raise ValueError("operands have different shapes")

    # TODO: Work with domain and broadcasting.
    return da.Darray(
        left.num * right.num,
        left.codomain + right.codomain,
        None if left.domain is None else left.domain + right.domain,
    )


@implements(np.true_divide)
def _true_divide(*inputs, **kwargs):
    left, right = inputs

    if left.basis != right.basis:
        raise ValueError("operands use different bases")
    # TODO: Broadcast.
    if left.num.shape != right.num.shape:
        raise ValueError("operands have different shapes")

    # TODO: Work with domain and broadcasting.
    return da.Darray(
        left.num / right.num,
        left.codomain - right.codomain,
        None if left.domain is None else left.domain - right.domain,
    )


@implements(np.floor_divide)
def _floor_divide(*inputs, **kwargs):
    left, right = inputs

    if left.basis != right.basis:
        raise ValueError("operands use different bases")
    # TODO: Broadcast.
    if left.num.shape != right.num.shape:
        raise ValueError("operands have different shapes")

    # TODO: Work with domain and broadcasting.
    return da.Darray(
        left.num // right.num,
        left.codomain - right.codomain,
        None if left.domain is None else left.domain - right.domain,
    )


@implements(np.matmul)
def _matmul(*inputs, **kwargs):
    left, right = inputs

    # TODO
    if left.basis != right.basis:
        raise ValueError("operands use different bases")
    if left.domain != right.codomain:
        raise ValueError("codomains do not match")

    return da.Darray(left.num @ right.num, left.codomain, right.domain)
