"""Tests, that are run against all implemented versions of aggregate."""

import itertools
import warnings

import numpy as np
import pytest

from . import (
    _impl_name,
    _implementations,
    _wrap_notimplemented_skip,
    func_list,
    _is_implemented,
)


@pytest.fixture(params=_implementations, ids=_impl_name)
def aggregate_all(request):
    impl = request.param
    if impl is None:
        pytest.skip("Implementation not available")
    name = _impl_name(impl)
    return _wrap_notimplemented_skip(impl.aggregate, "aggregate_" + name)


def _deselect_purepy(aggregate_all, *args, **kwargs):
    # purepy implementations does not handle nan values and ndim correctly.
    # So it needs to be excluded from several tests."""
    return aggregate_all.__name__.endswith("purepy")


def _deselect_purepy_and_pandas(aggregate_all, *args, **kwargs):
    # purepy and pandas implementation handle some nan cases differently.
    # So they need to be excluded from several tests."""
    return aggregate_all.__name__.endswith(("pandas", "purepy"))


def _deselect_purepy_and_invalid_axis(aggregate_all, func, size, axis):
    impl_name = aggregate_all.__name__.split("_")[-1]
    if impl_name == "purepy":
        # purepy does not handle axis parameter
        return True
    if axis >= len(size):
        return True
    if not _is_implemented(impl_name, func):
        return True
    return False


def _deselect_not_implemented(aggregate_all, func, *args, **kwargs):
    impl_name = aggregate_all.__name__.split("_")[-1]
    return not _is_implemented(impl_name, func)


def test_preserve_missing(aggregate_all):
    res = aggregate_all(np.array([0, 1, 3, 1, 3]), np.arange(101, 106, dtype=int))
    np.testing.assert_array_equal(res, np.array([101, 206, 0, 208]))
    if not isinstance(res, list):
        assert "int" in res.dtype.name


@pytest.mark.parametrize("group_idx_type", [int, "uint32", "uint64"])
def test_uint_group_idx(aggregate_all, group_idx_type):
    group_idx = np.array([1, 1, 2, 2, 2, 2, 4, 4], dtype=group_idx_type)
    res = aggregate_all(group_idx, np.ones(group_idx.size), dtype=int)
    np.testing.assert_array_equal(res, np.array([0, 2, 4, 0, 2]))
    if not isinstance(res, list):
        assert "int" in res.dtype.name


def test_start_with_offset(aggregate_all):
    group_idx = np.array([1, 1, 2, 2, 2, 2, 4, 4])
    res = aggregate_all(group_idx, np.ones(group_idx.size), dtype=int)
    np.testing.assert_array_equal(res, np.array([0, 2, 4, 0, 2]))
    if not isinstance(res, list):
        assert "int" in res.dtype.name


@pytest.mark.parametrize(
    "floatfunc", [np.std, np.var, np.mean], ids=lambda x: x.__name__
)
def test_float_enforcement(aggregate_all, floatfunc):
    group_idx = np.arange(10).repeat(3)
    a = np.arange(group_idx.size)
    res = aggregate_all(group_idx, a, floatfunc)
    if not isinstance(res, list):
        assert "float" in res.dtype.name
    assert np.all(np.array(res) > 0)


def test_start_with_offset_prod(aggregate_all):
    group_idx = np.array([2, 2, 4, 4, 4, 7, 7, 7])
    res = aggregate_all(group_idx, group_idx, func=np.prod, dtype=int)
    np.testing.assert_array_equal(res, np.array([0, 0, 4, 0, 64, 0, 0, 343]))


def test_no_negative_indices(aggregate_all):
    for pos in (0, 10, -1):
        group_idx = np.arange(5).repeat(5)
        group_idx[pos] = -1
        pytest.raises(ValueError, aggregate_all, group_idx, np.arange(len(group_idx)))


def test_parameter_missing(aggregate_all):
    pytest.raises(TypeError, aggregate_all, np.arange(5))


def test_shape_mismatch(aggregate_all):
    pytest.raises(ValueError, aggregate_all, np.array((1, 2, 3)), np.array((1, 2)))


def test_create_lists(aggregate_all):
    res = aggregate_all(
        np.array([0, 1, 3, 1, 3]), np.arange(101, 106, dtype=int), func=list
    )
    np.testing.assert_array_equal(np.array(res[0]), np.array([101]))
    assert res[2] == 0
    np.testing.assert_array_equal(np.array(res[3]), np.array([103, 105]))


def test_item_counting(aggregate_all):
    group_idx = np.array([0, 1, 2, 3, 3, 3, 3, 4, 5, 5, 5, 6, 5, 4, 3, 8, 8])
    a = np.arange(group_idx.size)
    res = aggregate_all(group_idx, a, func=lambda x: len(x) > 1)
    np.testing.assert_array_equal(res, np.array([0, 0, 0, 1, 1, 1, 0, 0, 1]))


@pytest.mark.parametrize(
    ["func", "fill_value"], [(np.array, None), (np.sum, -1)], ids=["array", "sum"]
)
def test_fill_value(aggregate_all, func, fill_value):
    group_idx = np.array([0, 2, 2], dtype=int)
    res = aggregate_all(
        group_idx,
        np.arange(len(group_idx), dtype=int),
        func=func,
        fill_value=fill_value,
    )
    assert res[1] == fill_value


@pytest.mark.parametrize("order", ["C", "F"])
def test_array_ordering(aggregate_all, order, size=10):
    mat = np.zeros((size, size), order=order, dtype=float)
    mat.flat[:] = np.arange(size * size)
    assert aggregate_all(np.zeros(size, dtype=int), mat[0, :], order=order)[0] == sum(
        range(size)
    )


@pytest.mark.deselect_if(func=_deselect_purepy)
@pytest.mark.parametrize("size", [None, (10, 2)])
def test_ndim_group_idx(aggregate_all, size):
    group_idx = np.vstack((np.repeat(np.arange(10), 10), np.repeat([0, 1], 50)))
    aggregate_all(group_idx, 1, size=size)


@pytest.mark.deselect_if(func=_deselect_purepy)
@pytest.mark.parametrize(["ndim", "order"], itertools.product([1, 2, 3], ["C", "F"]))
def test_ndim_indexing(aggregate_all, ndim, order, outsize=10):
    nindices = int(outsize**ndim)
    outshape = tuple([outsize] * ndim)
    group_idx = np.random.randint(0, outsize, size=(ndim, nindices))
    a = np.random.random(group_idx.shape[1])
    res = aggregate_all(group_idx, a, size=outshape, order=order)
    if ndim > 1 and order == "F":
        # 1d arrays always return False here
        assert np.isfortran(res)
    else:
        assert not np.isfortran(res)
    assert res.shape == outshape


def test_len(aggregate_all, group_size=5):
    group_idx = np.arange(0, 100, 2, dtype=int).repeat(group_size)
    a = np.arange(group_idx.size)
    res = aggregate_all(group_idx, a, func="len")
    ref = aggregate_all(group_idx, 1, func="sum")
    if isinstance(res, np.ndarray):
        assert issubclass(res.dtype.type, np.integer)
    else:
        assert isinstance(res[0], int)
    np.testing.assert_array_equal(res, ref)
    group_idx = np.arange(0, 100, dtype=int).repeat(group_size)
    a = np.arange(group_idx.size)
    res = aggregate_all(group_idx, a, func=len)
    if isinstance(res, np.ndarray):
        assert np.all(res == group_size)
    else:
        assert all(x == group_size for x in res)


def test_nan_len(aggregate_all):
    group_idx = np.arange(0, 20, 2, dtype=int).repeat(5)
    a = np.random.random(group_idx.size)
    a[::4] = np.nan
    a[::5] = np.nan
    res = aggregate_all(group_idx, a, func="nanlen")
    ref = aggregate_all(group_idx[~np.isnan(a)], 1, func="sum")
    if isinstance(res, np.ndarray):
        assert issubclass(res.dtype.type, np.integer)
    else:
        assert isinstance(res[0], int)
    np.testing.assert_array_equal(res, ref)


@pytest.mark.parametrize("first_last", ["first", "last"])
def test_first_last(aggregate_all, first_last):
    group_idx = np.arange(0, 100, 2, dtype=int).repeat(5)
    a = np.arange(group_idx.size)
    res = aggregate_all(group_idx, a, func=first_last, fill_value=-1)
    ref = np.zeros(np.max(group_idx) + 1)
    ref.fill(-1)
    ref[::2] = np.arange(
        0 if first_last == "first" else 4, group_idx.size, 5, dtype=int
    )
    np.testing.assert_array_equal(res, ref)


@pytest.mark.parametrize(
    ["first_last", "nanoffset"], itertools.product(["nanfirst", "nanlast"], [0, 2, 4])
)
def test_nan_first_last(aggregate_all, first_last, nanoffset):
    group_idx = np.arange(0, 100, 2, dtype=int).repeat(5)
    a = np.arange(group_idx.size, dtype=float)

    a[nanoffset::5] = np.nan
    res = aggregate_all(group_idx, a, func=first_last, fill_value=-1)
    ref = np.zeros(np.max(group_idx) + 1)
    ref.fill(-1)

    if first_last == "nanfirst":
        ref_offset = 1 if nanoffset == 0 else 0
    else:
        ref_offset = 3 if nanoffset == 4 else 4
    ref[::2] = np.arange(ref_offset, group_idx.size, 5, dtype=int)
    np.testing.assert_array_equal(res, ref)


@pytest.mark.parametrize(["func", "ddof"], itertools.product(["var", "std"], [0, 1, 2]))
def test_ddof(aggregate_all, func, ddof, size=20):
    group_idx = np.zeros(20, dtype=int)
    a = np.random.random(group_idx.size)
    res = aggregate_all(group_idx, a, func, ddof=ddof)
    ref_func = {"std": np.std, "var": np.var}.get(func)
    ref = ref_func(a, ddof=ddof)
    assert abs(res[0] - ref) < 1e-10


@pytest.mark.parametrize("func", ["sum", "prod", "mean", "var", "std"])
def test_scalar_input(aggregate_all, func):
    group_idx = np.arange(0, 100, dtype=int).repeat(5)
    if func not in ("sum", "prod"):
        pytest.raises(
            (ValueError, NotImplementedError), aggregate_all, group_idx, 1, func=func
        )
    else:
        res = aggregate_all(group_idx, 1, func=func)
        ref = aggregate_all(group_idx, np.ones_like(group_idx, dtype=int), func=func)
        np.testing.assert_array_equal(res, ref)


@pytest.mark.parametrize("func", ["sum", "prod", "mean", "var", "std", "all", "any"])
def test_nan_input(aggregate_all, func, groups=100):
    if aggregate_all.__name__.endswith("pandas"):
        pytest.skip("pandas always skips nan values")
    group_idx = np.arange(0, groups, dtype=int).repeat(5)
    a = np.random.random(group_idx.size)
    a[::2] = np.nan

    if func in ("all", "any"):
        ref = np.ones(groups, dtype=bool)
    else:
        ref = np.full(groups, np.nan, dtype=float)
    res = aggregate_all(group_idx, a, func=func)
    np.testing.assert_array_equal(res, ref)


def test_nan_input_len(aggregate_all, groups=100, group_size=5):
    if aggregate_all.__name__.endswith("pandas"):
        pytest.skip("pandas always skips nan values")
    group_idx = np.arange(0, groups, dtype=int).repeat(group_size)
    a = np.random.random(len(group_idx))
    a[::2] = np.nan
    ref = np.full(groups, group_size, dtype=int)
    res = aggregate_all(group_idx, a, func=len)
    np.testing.assert_array_equal(res, ref)


def test_argmin_argmax_nonans(aggregate_all):
    group_idx = np.array([0, 0, 0, 0, 3, 3, 3, 3])
    a = np.array([4, 4, 3, 1, 10, 9, 9, 11])

    res = aggregate_all(group_idx, a, func="argmax", fill_value=-1)
    np.testing.assert_array_equal(res, [0, -1, -1, 7])

    res = aggregate_all(group_idx, a, func="argmin", fill_value=-1)
    np.testing.assert_array_equal(res, [3, -1, -1, 5])


@pytest.mark.deselect_if(func=_deselect_purepy)
def test_argmin_argmax_nans(aggregate_all):
    if aggregate_all.__name__.endswith("pandas"):
        pytest.skip("pandas always ignores nans")

    group_idx = np.array([0, 0, 0, 0, 3, 3, 3, 3])
    a = np.array([4, 4, 3, 1, np.nan, 1, 2, 3])

    res = aggregate_all(group_idx, a, func="argmax", fill_value=-1)
    np.testing.assert_array_equal(res, [0, -1, -1, -1])

    res = aggregate_all(group_idx, a, func="argmin", fill_value=-1)
    np.testing.assert_array_equal(res, [3, -1, -1, -1])


@pytest.mark.deselect_if(func=_deselect_purepy)
def test_nanargmin_nanargmax_nans(aggregate_all):
    if aggregate_all.__name__.endswith("pandas"):
        pytest.skip(
            "pandas doesn't fill indices for all-nan groups with fill_value but with -inf instead"
        )

    group_idx = np.array([0, 0, 0, 0, 3, 3, 3, 3])
    a = np.array([4, 4, np.nan, 1, np.nan, np.nan, np.nan, np.nan])

    res = aggregate_all(group_idx, a, func="nanargmax", fill_value=-1)
    np.testing.assert_array_equal(res, [0, -1, -1, -1])

    res = aggregate_all(group_idx, a, func="nanargmin", fill_value=-1)
    np.testing.assert_array_equal(res, [3, -1, -1, -1])


def test_nanargmin_nanargmax_nonans(aggregate_all):
    group_idx = np.array([0, 0, 0, 0, 3, 3, 3, 3])
    a = np.array([4, 4, 3, 1, 10, 9, 9, 11])

    res = aggregate_all(group_idx, a, func="nanargmax", fill_value=-1)
    np.testing.assert_array_equal(res, [0, -1, -1, 7])

    res = aggregate_all(group_idx, a, func="nanargmin", fill_value=-1)
    np.testing.assert_array_equal(res, [3, -1, -1, 5])


def test_min_max_inf(aggregate_all):
    # https://github.com/ml31415/numpy-groupies/issues/40
    res = aggregate_all(
        np.array([0, 1, 2, 0, 1, 2]),
        np.array([-np.inf, 0, -np.inf, -np.inf, 0, 0]),
        func="max",
    )
    np.testing.assert_array_equal(res, [-np.inf, 0, 0])

    res = aggregate_all(
        np.array([0, 1, 2, 0, 1, 2]),
        np.array([np.inf, 0, np.inf, np.inf, 0, 0]),
        func="min",
    )
    np.testing.assert_array_equal(res, [np.inf, 0, 0])


def test_argmin_argmax_inf(aggregate_all):
    # https://github.com/ml31415/numpy-groupies/issues/40
    res = aggregate_all(
        np.array([0, 1, 2, 0, 1, 2]),
        np.array([-np.inf, 0, -np.inf, -np.inf, 0, 0]),
        func="argmax",
        fill_value=-1,
    )
    np.testing.assert_array_equal(res, [0, 1, 5])

    res = aggregate_all(
        np.array([0, 1, 2, 0, 1, 2]),
        np.array([np.inf, 0, np.inf, np.inf, 0, 0]),
        func="argmin",
        fill_value=-1,
    )
    np.testing.assert_array_equal(res, [0, 1, 5])


def test_mean(aggregate_all):
    group_idx = np.array([0, 0, 0, 0, 3, 3, 3, 3])
    a = np.arange(len(group_idx))

    res = aggregate_all(group_idx, a, func="mean")
    np.testing.assert_array_equal(res, [1.5, 0, 0, 5.5])


def test_cumsum(aggregate_all):
    group_idx = np.array([4, 3, 3, 4, 4, 1, 1, 1, 7, 8, 7, 4, 3, 3, 1, 1])
    a = np.array([3, 4, 1, 3, 9, 9, 6, 7, 7, 0, 8, 2, 1, 8, 9, 8])
    ref = np.array([3, 4, 5, 6, 15, 9, 15, 22, 7, 0, 15, 17, 6, 14, 31, 39])

    res = aggregate_all(group_idx, a, func="cumsum")
    np.testing.assert_array_equal(res, ref)


@pytest.mark.deselect_if(func=_deselect_purepy_and_pandas)
def test_nancumsum(aggregate_all):
    # https://github.com/ml31415/numpy-groupies/issues/79
    group_idx = [0, 0, 0, 1, 1, 0, 0]
    a = [2, 2, np.nan, 2, 2, 2, 2]
    ref = [2.0, 4.0, 4.0, 2.0, 4.0, 6.0, 8.0]

    res = aggregate_all(group_idx, a, func="nancumsum")
    np.testing.assert_array_equal(res, ref)


def test_cummax(aggregate_all):
    group_idx = np.array([4, 3, 3, 4, 4, 1, 1, 1, 7, 8, 7, 4, 3, 3, 1, 1])
    a = np.array([3, 4, 1, 3, 9, 9, 6, 7, 7, 0, 8, 2, 1, 8, 9, 8])
    ref = np.array([3, 4, 4, 3, 9, 9, 9, 9, 7, 0, 8, 9, 4, 8, 9, 9])

    res = aggregate_all(group_idx, a, func="cummax")
    np.testing.assert_array_equal(res, ref)


@pytest.mark.parametrize("order", ["normal", "reverse"])
def test_list_ordering(aggregate_all, order):
    group_idx = np.repeat(np.arange(5), 4)
    a = np.arange(group_idx.size)
    if order == "reverse":
        a = a[::-1]
    ref = a[:4]

    res = aggregate_all(group_idx, a, func=list)
    np.testing.assert_array_equal(np.array(res[0]), ref)


@pytest.mark.parametrize("order", ["normal", "reverse"])
def test_sort(aggregate_all, order):
    group_idx = np.array([3, 3, 3, 2, 2, 2, 1, 1, 1])
    a = np.array([3, 2, 1, 3, 4, 5, 5, 10, 1])
    ref_normal = np.array([1, 2, 3, 3, 4, 5, 1, 5, 10])
    ref_reverse = np.array([3, 2, 1, 5, 4, 3, 10, 5, 1])
    reverse = order == "reverse"
    ref = ref_reverse if reverse else ref_normal

    res = aggregate_all(group_idx, a, func="sort", reverse=reverse)
    np.testing.assert_array_equal(res, ref)


@pytest.mark.deselect_if(func=_deselect_purepy_and_invalid_axis)
@pytest.mark.parametrize("axis", (0, 1))
@pytest.mark.parametrize("size", ((12,), (12, 5)))
@pytest.mark.parametrize("func", func_list)
def test_along_axis(aggregate_all, func, size, axis):
    group_idx = np.zeros(size[axis], dtype=int)
    a = np.random.randn(*size)

    # add some NaNs to test out nan-skipping
    if "nan" in func and "nanarg" not in func:
        a[[1, 4, 5], ...] = np.nan
    elif "nanarg" in func and a.ndim > 1:
        a[[1, 4, 5], 1] = np.nan
    if func in ["any", "all"]:
        a = a > 0.5

    # construct expected values for all cases
    if func == "len":
        expected = np.array(size[axis])
    elif func == "nanlen":
        expected = np.array((~np.isnan(a)).sum(axis=axis))
    elif func == "anynan":
        expected = np.isnan(a).any(axis=axis)
    elif func == "allnan":
        expected = np.isnan(a).all(axis=axis)
    elif func == "sumofsquares":
        expected = np.sum(a * a, axis=axis)
    elif func == "nansumofsquares":
        expected = np.nansum(a * a, axis=axis)
    else:
        with warnings.catch_warnings():
            # Filter  expected warnings:
            # - RuntimeWarning: All-NaN slice encountered
            # - RuntimeWarning: Mean of empty slice
            # - RuntimeWarning: Degrees of freedom <= 0 for slice.
            warnings.simplefilter("ignore", RuntimeWarning)
            expected = getattr(np, func)(a, axis=axis)

    # The default fill_value is 0, the following makes the output match numpy
    fill_value = {
        "nanprod": 1,
        "nanvar": np.nan,
        "nanstd": np.nan,
        "nanmax": np.nan,
        "nanmin": np.nan,
        "nanmean": np.nan,
    }.get(func, 0)

    actual = aggregate_all(group_idx, a, axis=axis, func=func, fill_value=fill_value)
    assert actual.ndim == a.ndim

    # argmin, argmax don't support keepdims, so we can't use that to construct expected
    # instead we squeeze out the extra dims in actual.
    np.testing.assert_allclose(actual.squeeze(), expected)


@pytest.mark.deselect_if(func=_deselect_purepy)
def test_not_last_axis_reduction(aggregate_all):
    group_idx = np.array([1, 2, 2, 0, 1])
    a = np.array([[1.0, 2.0], [4.0, 4.0], [5.0, 2.0], [np.nan, 3.0], [8.0, 7.0]])
    func = "nanmax"
    fill_value = np.nan
    axis = 0
    actual = aggregate_all(group_idx, a, axis=axis, func=func, fill_value=fill_value)
    expected = np.array([[np.nan, 3.0], [8.0, 7.0], [5.0, 4.0]])
    np.testing.assert_allclose(expected, actual)


@pytest.mark.deselect_if(func=_deselect_purepy)
def test_custom_callable(aggregate_all):
    def custom_callable(x):
        return x.sum()

    size = (10,)
    axis = -1

    group_idx = np.zeros(size, dtype=int)
    a = np.random.randn(*size)

    expected = a.sum(axis=axis, keepdims=True)
    actual = aggregate_all(group_idx, a, axis=axis, func=custom_callable, fill_value=0)
    assert actual.ndim == a.ndim

    np.testing.assert_allclose(actual, expected)


@pytest.mark.deselect_if(func=_deselect_purepy)
def test_argreduction_nD_array_1D_idx(aggregate_all):
    # https://github.com/ml31415/numpy-groupies/issues/41
    group_idx = np.array([0, 0, 2, 2, 2, 1, 1, 2, 2, 1, 1, 0], dtype=int)
    a = np.array([[1] * 12, [1] * 12])
    actual = aggregate_all(group_idx, a, axis=-1, func="argmax")
    expected = np.array([[0, 5, 2], [0, 5, 2]])
    np.testing.assert_equal(actual, expected)


@pytest.mark.deselect_if(func=_deselect_purepy)
def test_argreduction_negative_fill_value(aggregate_all):
    if aggregate_all.__name__.endswith("pandas"):
        pytest.skip("pandas always skips nan values")

    group_idx = np.array([0, 0, 2, 2, 2, 1, 1, 2, 2, 1, 1, 0], dtype=int)
    a = np.array([[1] * 12, [np.nan] * 12])
    actual = aggregate_all(group_idx, a, axis=-1, fill_value=-1, func="argmax")
    expected = np.array([[0, 5, 2], [-1, -1, -1]])
    np.testing.assert_equal(actual, expected)


@pytest.mark.deselect_if(func=_deselect_not_implemented)
@pytest.mark.parametrize(
    "nan_inds", (None, tuple([[1, 4, 5], Ellipsis]), tuple((1, (0, 1, 2, 3))))
)
@pytest.mark.parametrize("ddof", (0, 1))
@pytest.mark.parametrize("func", ("nanvar", "nanstd"))
def test_var_with_nan_fill_value(aggregate_all, ddof, nan_inds, func):
    a = np.ones((12, 5))
    group_idx = np.zeros(a.shape[-1:], dtype=int)

    if nan_inds is not None:
        a[nan_inds] = np.nan

    with warnings.catch_warnings():
        # Filter RuntimeWarning: Degrees of freedom <= 0 for slice.
        warnings.simplefilter("ignore", RuntimeWarning)
        expected = getattr(np, func)(a, keepdims=True, axis=-1, ddof=ddof)

    actual = aggregate_all(
        group_idx, a, axis=-1, fill_value=np.nan, func=func, ddof=ddof
    )
    np.testing.assert_equal(actual, expected)


def test_cumsum_accuracy(aggregate_all):
    array = np.array(
        [0.00000000e00, 0.00000000e00, 0.00000000e00, 3.27680000e04, 9.99999975e-06]
    )
    group_idx = np.array([0, 0, 0, 0, 1])

    actual = aggregate_all(group_idx, array, axis=-1, func="cumsum")
    expected = array
    np.testing.assert_allclose(actual, expected)
