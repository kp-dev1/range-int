class RangeInt:
    """
    A numeric type that automatically clamps its value within a [min, max] range.

    All arithmetic operations, assignments, and mutations keep the value within
    bounds. Supports threshold callbacks, relative positioning, lerp, and more.

    Args:
        value: The initial value. Will be clamped to [min_val, max_val].
        min_val: The lower bound of the range.
        max_val: The upper bound of the range.

    Raises:
        ValueError: If min_val equals max_val.

    Example:
        >>> hp = RangeInt(100, 0, 100)
        >>> hp -= 999
        >>> print(hp)
        0
    """

    __slots__ = ['_value', '_min', '_max', '_callbacks']

    def __init__(self, value, min_val, max_val):
        if min_val == max_val:
            raise ValueError("min_val cannot equal max_val")
        self._min = min_val
        self._max = max_val
        self._callbacks = {}
        self.value = value

    @property
    def value(self):
        """The current clamped value."""
        return self._value

    @value.setter
    def value(self, new_val):
        old_percent = self.relative() if hasattr(self, '_value') else None
        self._value = max(self._min, min(new_val, self._max))
        new_percent = self.relative()
        if old_percent is not None:
            for pct, command in self._callbacks.items():
                if (old_percent < pct <= new_percent) or (old_percent > pct >= new_percent):
                    command()

    @property
    def min(self):
        """The lower bound of the range."""
        return self._min

    @property
    def max(self):
        """The upper bound of the range."""
        return self._max

    def _get_val(self, other):
        return other.value if isinstance(other, RangeInt) else other

    def _ensure_range_defined(self):
        if self._min is None or self._max is None:
            raise ValueError("Operation requires both min and max to be defined")

    def __add__(self, other):      return RangeInt(self.value + self._get_val(other), self._min, self._max)
    def __sub__(self, other):      return RangeInt(self.value - self._get_val(other), self._min, self._max)
    def __mul__(self, other):      return RangeInt(self.value * self._get_val(other), self._min, self._max)
    def __truediv__(self, other):  return RangeInt(self.value / self._get_val(other), self._min, self._max)
    def __floordiv__(self, other): return RangeInt(self.value // self._get_val(other), self._min, self._max)
    def __mod__(self, other):      return RangeInt(self.value % self._get_val(other), self._min, self._max)
    def __pow__(self, other):      return RangeInt(self.value ** self._get_val(other), self._min, self._max)

    def __radd__(self, other): return self.__add__(other)
    def __rsub__(self, other): return RangeInt(self._get_val(other) - self.value, self._min, self._max)
    def __rmul__(self, other): return self.__mul__(other)

    def __iadd__(self, other):
        self.value += self._get_val(other)
        return self

    def __isub__(self, other):
        self.value -= self._get_val(other)
        return self

    def __imul__(self, other):
        self.value *= self._get_val(other)
        return self

    def __itruediv__(self, other):
        self.value /= self._get_val(other)
        return self

    def __eq__(self, other): return self.value == self._get_val(other)
    def __lt__(self, other): return self.value <  self._get_val(other)
    def __le__(self, other): return self.value <= self._get_val(other)
    def __gt__(self, other): return self.value >  self._get_val(other)
    def __ge__(self, other): return self.value >= self._get_val(other)

    def __index__(self):  return int(self.value)
    def __int__(self):    return int(self.value)
    def __float__(self):  return float(self.value)
    def __bool__(self):   return bool(self.value)
    def __neg__(self):    return RangeInt(-self.value, self._min, self._max)
    def __abs__(self):    return RangeInt(abs(self.value), self._min, self._max)
    def __repr__(self):   return f"RangeInt({self.value}, min={self._min}, max={self._max})"
    def __str__(self):    return str(self.value)

    def set_range(self, min_val: int, max_val: int) -> "RangeInt":
        """
        Update the min/max bounds and re-clamp the current value.

        Args:
            min_val: New lower bound.
            max_val: New upper bound.

        Returns:
            self, for chaining.

        Raises:
            ValueError: If min_val equals max_val.

        Example:
            >>> r = RangeInt(80, 0, 100)
            >>> r.set_range(0, 50)
            >>> print(r.value)
            50
        """
        if min_val == max_val:
            raise ValueError("min_val cannot equal max_val")
        self._min = min_val
        self._max = max_val
        self.value = self._value
        return self

    def relative(self) -> float:
        """
        Return the value's position as a float between 0.0 and 1.0.

        Returns:
            A float where 0.0 is min and 1.0 is max.

        Example:
            >>> r = RangeInt(75, 0, 100)
            >>> r.relative()
            0.75
        """
        self._ensure_range_defined()
        return (self._value - self._min) / (self._max - self._min)

    def nudge_percentage(self, amt: float) -> int:
        """
        Shift the value by a fraction of the total range.

        Args:
            amt: Fraction to shift by. Positive moves toward max, negative toward min.
                 e.g. 0.1 shifts by 10% of the range.

        Returns:
            The new clamped value.

        Example:
            >>> r = RangeInt(50, 0, 100)
            >>> r.nudge_percentage(0.1)
            60
        """
        self._ensure_range_defined()
        self.value += int((self._max - self._min) * amt)
        return self._value

    def lerp_to(self, percentage: float) -> float:
        """
        Set the value to a fractional position between min and max.

        Args:
            percentage: Target position as a float between 0.0 and 1.0.
                        0.0 sets the value to min, 1.0 sets it to max.

        Returns:
            The new value.

        Example:
            >>> r = RangeInt(0, 0, 200)
            >>> r.lerp_to(0.5)
            100.0
        """
        self._ensure_range_defined()
        self.value = self._min + percentage * (self._max - self._min)
        return self._value

    def edge_check(self, val_check: str) -> bool:
        """
        Check whether the value is sitting at the min or max boundary.

        Args:
            val_check: Either "min" or "max".

        Returns:
            True if the value equals the specified boundary, False otherwise.

        Raises:
            ValueError: If val_check is not "min" or "max".

        Example:
            >>> r = RangeInt(0, 0, 100)
            >>> r.edge_check("min")
            True
        """
        if val_check == "min":
            return self._value == self._min
        elif val_check == "max":
            return self._value == self._max
        raise ValueError(f"val_check must be 'min' or 'max', got '{val_check}'")

    def is_between(self, low: float, high: float) -> bool:
        """
        Check whether the relative position falls within [low, high].

        Args:
            low: Lower bound as a float between 0.0 and 1.0.
            high: Upper bound as a float between 0.0 and 1.0.

        Returns:
            True if the relative position is within [low, high].

        Raises:
            ValueError: If low or high are outside [0.0, 1.0].

        Example:
            >>> r = RangeInt(50, 0, 100)
            >>> r.is_between(0.25, 0.75)
            True
        """
        self._ensure_range_defined()
        if not (0.0 <= low <= 1.0 and 0.0 <= high <= 1.0):
            raise ValueError("low and high must be between 0.0 and 1.0")
        return low <= self.relative() <= high
