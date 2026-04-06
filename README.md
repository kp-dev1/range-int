# RangeInt

A clamped numeric type for Python. Values are automatically kept within a `[min, max]` range — all arithmetic, assignment, and mutations clamp silently. Built for game dev, UI sliders, stat systems, animation, or anywhere you want a number that stays in bounds.

```python
from rangeint import RangeInt

hp = RangeInt(100, 0, 100)
hp -= 999
print(hp)  # 0  — never goes below min
```

---

## Install

```bash
pip install rangeint
```

---

## Quick Start

```python
from rangeint import RangeInt

volume = RangeInt(50, 0, 100)

volume += 80     # → 100  (clamped at max)
volume -= 200    # → 0    (clamped at min)

print(int(volume))    # 0
print(float(volume))  # 0.0
print(volume == 0)    # True
```

---

## API

### Constructor

```python
RangeInt(value, min_val, max_val)
```

Raises `ValueError` if `min_val == max_val`.

---

### Properties

| Property | Description |
|----------|-------------|
| `.value` | Current value (clamped on set) |
| `.min`   | Lower bound |
| `.max`   | Upper bound |

---

### Methods

#### `relative() -> float`
Returns the value's position as a float between `0.0` and `1.0`.
```python
RangeInt(75, 0, 100).relative()  # 0.75
```

#### `lerp_to(percentage) -> float`
Sets the value to a fractional position between min and max.
```python
r = RangeInt(0, 0, 200)
r.lerp_to(0.5)   # 100.0
```

#### `nudge_percentage(amt) -> int`
Shifts the value by a fraction of the total range.
```python
r = RangeInt(50, 0, 100)
r.nudge_percentage(0.1)   # 60
```

#### `set_range(min_val, max_val) -> RangeInt`
Updates the bounds and re-clamps the current value. Chainable.
```python
r = RangeInt(80, 0, 100)
r.set_range(0, 50)   # value clamped to 50
```

#### `edge_check(val_check) -> bool`
Returns `True` if the value is at `"min"` or `"max"`.
```python
RangeInt(0, 0, 100).edge_check("min")   # True
RangeInt(0, 0, 100).edge_check("max")   # False
```

#### `is_between(low, high) -> bool`
Returns `True` if the relative position falls within `[low, high]`.
```python
RangeInt(50, 0, 100).is_between(0.25, 0.75)  # True
```

#### `on_percentage(percentage, directional, through)`

Register a function to fire whenever the value crosses a relative threshold if through is set to False it will only fire if it is exact. if through is set to True it will fire if it passes through. Directional controls if it fires when its coming up 30 - 70 or down 70 - 30.
```python
health = RangeInt(0, 0, 100)
def low_health():
  print("Low Health: {health.value()}HP remaining")
health.on_percentage(0.5, low_health, directional="down", through=True)
health += 70
health -= 40 # Low Health: 30HP remaining
```
Note: Only one function can be assigned to each percentage level



### Operators

| Operator | Supported |
|----------|-----------|
| `+`, `-`, `*`, `/`, `//`, `%`, `**` | Yes |
| `+=`, `-=`, `*=`, `/=` | Yes |
| Reflected `+`, `-`, `*` | Yes |
| `-x`, `abs(x)` | Yes |
| `==`, `<`, `<=`, `>`, `>=` | Yes |
| `int()`, `float()`, `bool()` | Yes |

---

## License

MIT
