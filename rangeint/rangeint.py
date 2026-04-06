class RangeInt:
    __slots__ = ['_value', '_min', '_max', '_callbacks']

    def __init__(self, value, min_val, max_val):
        if min_val == max_val:
            raise ValueError("min_val cannot equal max_val")
        self._min = min_val
        self._max = max_val
        self._callbacks = {}  # Stores {0.5: my_function}
        self.value = value

    # ── Core value property ──────────────────────────────────────────────────

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_val):
        if not hasattr(self, '_value'):
            self._value = max(self._min, min(new_val, self._max))
            return
        
        old_pct = self.relative()
        self._value = max(self._min, min(new_val, self._max))
        new_pct = self.relative()

        for pct, (command, direction, through) in self._callbacks.items():
            moved_up = old_pct < pct <= new_pct
            moved_down = old_pct > pct >= new_pct
            
            # Check if we landed EXACTLY on the spot (with a tiny margin for math errors)
            landed_exactly = abs(new_pct - pct) < 1e-9

            if direction == "up" and moved_up:
                if through or landed_exactly:
                    command()
            elif direction == "down" and moved_down:
                if through or landed_exactly:
                    command()                
            elif direction == "both" and (moved_up or moved_down):
                if through or landed_exactly:
                    command()
              
            


    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _get_val(self, other):
        return other.value if isinstance(other, RangeInt) else other

    def _ensure_range_defined(self):
        if self._min is None or self._max is None:
            raise ValueError("Operation requires both min and max to be defined")

    # ── Arithmetic operators ─────────────────────────────────────────────────

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

    # ── Comparison operators ─────────────────────────────────────────────────

    def __eq__(self, other): return self.value == self._get_val(other)
    def __lt__(self, other): return self.value <  self._get_val(other)
    def __le__(self, other): return self.value <= self._get_val(other)
    def __gt__(self, other): return self.value >  self._get_val(other)
    def __ge__(self, other): return self.value >= self._get_val(other)

    # ── Type conversions ─────────────────────────────────────────────────────

    def __index__(self):  return int(self.value)
    def __int__(self):    return int(self.value)
    def __float__(self):  return float(self.value)
    def __bool__(self):   return bool(self.value)
    def __neg__(self):    return RangeInt(-self.value, self._min, self._max)
    def __abs__(self):    return RangeInt(abs(self.value), self._min, self._max)
    def __repr__(self):   return f"RangeInt({self.value}, min={self._min}, max={self._max})"
    def __str__(self):    return str(self.value)

    # ── Methods ──────────────────────────────────────────────────────────────

    def set_range(self, min_val: int, max_val: int) -> "RangeInt":
        """Sets the min/max range and re-clamps the current value within it."""
        if min_val == max_val:
            raise ValueError("min_val cannot equal max_val")
        self._min = min_val
        self._max = max_val
        self.value = self._value  # re-clamp to new range
        return self

    def relative(self) -> float:
        """
        Returns the value's position as a float between 0.0 and 1.0.
        e.g. min=0, max=100, value=72  →  0.72
        """
        self._ensure_range_defined()
        return (self._value - self._min) / (self._max - self._min)

    def nudge_percentage(self, amt: float) -> int:
        """Shifts the value by a fraction of the total range. e.g. amt=0.1 nudges by 10%."""
        self._ensure_range_defined()
        self.value += int((self._max - self._min) * amt)
        return self._value

    def lerp_to(self, percentage: float) -> float:
        """Sets the value to a position between min and max. e.g. percentage=0.5 → midpoint."""
        self._ensure_range_defined()
        self.value = self._min + percentage * (self._max - self._min)
        return self._value

    def edge_check(self, val_check: str) -> bool:
        """Returns True if the value is at 'min' or 'max' edge."""
        if val_check == "min":
            return self._value == self._min
        elif val_check == "max":
            return self._value == self._max
        raise ValueError(f"val_check must be 'min' or 'max', got '{val_check}'")

    def is_between(self, low: float, high: float) -> bool:
        """
        Returns True if the relative position is within [low, high].
        Both low and high should be floats between 0.0 and 1.0.
        e.g. is_between(0.25, 0.75) checks if value is in the middle half of the range.
        """
        self._ensure_range_defined()
        if not (0.0 <= low <= 1.0 and 0.0 <= high <= 1.0):
            raise ValueError("low and high must be between 0.0 and 1.0")
        return low <= self.relative() <= high
    def on_percentage(self, percentage: float, func, directional="both", through=False):
        """Initialise a callback where if it crosses the percentage based on directional
        a function fires. If through == True it will run if it passes through the value if through == False it will run
        only if it hits the exact value"""
        self._callbacks[percentage] = (func, directional, through)
        return self
