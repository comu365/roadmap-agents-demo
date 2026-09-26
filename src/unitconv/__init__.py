"""Tiny unit converter. Features are added one ROADMAP item at a time."""

import math
from fractions import Fraction

__version__ = "0.0.1"

# Length conversion factors: meters per 1 unit, kept as exact Fractions so that
# chained multiply/divide never introduces binary-float rounding error before
# the final result is produced (e.g. convert(1, "ft", "in") must be exactly 12).
# Source: NIST SP 811 (2008 ed.), Appendix B.
#   - "meter (m)" is the SI base unit for length -> factor 1.
#   - "inch (in) ... 0.0254 m" (exact, by international yard-and-pound agreement, 1959)
#   - "foot (ft) ... 0.3048 m" (exact: 12 in = 12 * 0.0254 m, listed directly in Appendix B)
#   - "yard (yd) ... 0.9144 m" (exact: 3 ft = 3 * 0.3048 m, listed directly in Appendix B)
#   - "mile (mi) (international) ... 1.609 344 E+03 m" (exact: 5280 ft = 5280 * 0.3048 m)
#   - "centimeter" and "kilometer" are SI-prefixed meters: 1 cm = 1e-2 m, 1 km = 1e3 m
#     (SI prefixes "centi" = 10^-2 and "kilo" = 10^3, NIST SP 811 Section 4 / Table 5).
#   - "millimeter": 1 mm = 1e-3 m (SI prefix "milli" = 10^-3).
_LENGTH_TO_METERS = {
    "m": Fraction(1),
    "km": Fraction(1000),
    "cm": Fraction(1, 100),
    "mm": Fraction(1, 1000),
    "in": Fraction("0.0254"),
    "ft": Fraction("0.3048"),
    "yd": Fraction("0.9144"),
    "mi": Fraction("1609.344"),
}


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert ``value`` from ``from_unit`` to ``to_unit``.

    Currently supports length units: m, km, cm, mm, in, ft, yd, mi.

    Raises:
        ValueError: if ``from_unit`` or ``to_unit`` is not a known unit, or if
            ``value`` is not a finite number (NaN/inf are rejected — no silent
            NaN output).
    """
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"value must be a real number, got {value!r}")
    if not math.isfinite(value):
        raise ValueError(f"value must be finite, got {value!r}")

    if from_unit not in _LENGTH_TO_METERS:
        raise ValueError(f"unknown unit: {from_unit!r}")
    if to_unit not in _LENGTH_TO_METERS:
        raise ValueError(f"unknown unit: {to_unit!r}")

    # Do the whole computation in exact rational arithmetic and only round to
    # the nearest double at the very end (Fraction -> float is correctly
    # rounded), so intermediate binary-float error can't creep in.
    ratio = _LENGTH_TO_METERS[from_unit] / _LENGTH_TO_METERS[to_unit]
    return float(Fraction(value) * ratio)
