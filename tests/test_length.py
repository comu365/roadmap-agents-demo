"""Tests for P1-1 length conversion.

Expected values are computed independently from the implementation, using the
exact NIST SP 811 Appendix B definitions:
    1 in = 0.0254 m (exact)
    1 ft = 12 in = 0.3048 m (exact)
    1 yd = 3 ft = 0.9144 m (exact)
    1 mi = 5280 ft = 1609.344 m (exact)
    1 km = 1000 m, 1 cm = 0.01 m, 1 mm = 0.001 m (SI prefixes)
"""

import math

import pytest

import unitconv

ALL_UNITS = ["m", "km", "cm", "mm", "in", "ft", "yd", "mi"]


def test_mile_to_meter_exact():
    assert unitconv.convert(1, "mi", "m") == 1609.344


def test_foot_to_inch_exact():
    assert unitconv.convert(1, "ft", "in") == 12


def test_inch_to_cm_exact():
    assert unitconv.convert(1, "in", "cm") == 2.54


def test_km_to_m():
    # 1 km = 1000 m by the SI "kilo" prefix, independent of the implementation.
    assert unitconv.convert(2.5, "km", "m") == 2500.0


def test_mm_to_m():
    # 1 mm = 0.001 m by the SI "milli" prefix.
    assert unitconv.convert(500, "mm", "m") == 0.5


def test_yard_to_foot_exact():
    # 1 yd = 3 ft by definition.
    assert unitconv.convert(2, "yd", "ft") == 6


@pytest.mark.parametrize("a", ALL_UNITS)
@pytest.mark.parametrize("b", ALL_UNITS)
def test_round_trip(a, b):
    x = 3.14159
    once = unitconv.convert(x, a, b)
    back = unitconv.convert(once, b, a)
    assert back == pytest.approx(x, rel=1e-12)


def test_unknown_unit_from_raises_with_name():
    with pytest.raises(ValueError, match="parsec"):
        unitconv.convert(1, "parsec", "m")


def test_unknown_unit_to_raises_with_name():
    with pytest.raises(ValueError, match="parsec"):
        unitconv.convert(1, "m", "parsec")


def test_nan_input_raises():
    with pytest.raises(ValueError):
        unitconv.convert(math.nan, "m", "km")


def test_inf_input_raises():
    with pytest.raises(ValueError):
        unitconv.convert(math.inf, "m", "km")


def test_neg_inf_input_raises():
    with pytest.raises(ValueError):
        unitconv.convert(-math.inf, "m", "km")
