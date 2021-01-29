from math import isnan
from typing import Any

from django.core.validators import MaxValueValidator

CLICK_POSITION_PERCENTAGE_VALIDATOR = MaxValueValidator(
    100, message="Click position percentage must be in range of 0 to 100"
)


def float_or_raise(value: Any) -> float:
    """
    Return float if given value can be converted to float.
    If the result is nan raise ValueError.

    :param value: anything to convert to float
    :return: float
    """
    value = float(value)

    if isnan(value) is True:
        raise ValueError("value is nan")

    return value
