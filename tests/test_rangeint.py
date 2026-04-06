import pytest
from rangeint import RangeInt


def test_normal_init():
    assert RangeInt(50, 0, 100).value == 50

def test_clamp_above_max():
    assert RangeInt(200, 0, 100).value == 100

def test_clamp_below_min():
    assert RangeInt(-50, 0, 100).value == 0

def test_equal_min_max_raises():
    with pytest.raises(ValueError):
        RangeInt(5, 10, 10)

def test_min_max_properties():
    r = RangeInt(50, 0, 100)
    assert r.min == 0
    assert r.max == 100

def test_add():
    assert (RangeInt(50, 0, 100) + 30).value == 80

def test_add_clamps():
    assert (RangeInt(50, 0, 100) + 999).value == 100

def test_sub():
    assert (RangeInt(50, 0, 100) - 20).value == 30

def test_sub_clamps():
    assert (RangeInt(50, 0, 100) - 999).value == 0

def test_mul():
    assert (RangeInt(50, 0, 100) * 2).value == 100

def test_radd():
    assert (10 + RangeInt(50, 0, 100)).value == 60

def test_rmul():
    assert (3 * RangeInt(50, 0, 100)).value == 100

def test_iadd():
    r = RangeInt(50, 0, 100)
    r += 25
    assert r.value == 75

def test_isub_clamps():
    r = RangeInt(50, 0, 100)
    r -= 999
    assert r.value == 0

def test_imul():
    r = RangeInt(40, 0, 100)
    r *= 2
    assert r.value == 80

def test_itruediv():
    r = RangeInt(80, 0, 100)
    r /= 2
    assert r.value == 40

def test_lt():
    assert RangeInt(40, 0, 100) < RangeInt(60, 0, 100)

def test_gt():
    assert RangeInt(60, 0, 100) > RangeInt(40, 0, 100)

def test_eq():
    assert RangeInt(40, 0, 100) == 40

def test_le():
    assert RangeInt(40, 0, 100) <= 40

def test_ge():
    assert RangeInt(60, 0, 100) >= 60

def test_int():
    assert int(RangeInt(75, 0, 100)) == 75

def test_float():
    assert float(RangeInt(75, 0, 100)) == 75.0

def test_bool_truthy():
    assert bool(RangeInt(1, 0, 100)) is True

def test_bool_falsy():
    assert bool(RangeInt(0, 0, 100)) is False

def test_neg_clamps():
    assert (-RangeInt(75, 0, 100)).value == 0

def test_neg_signed():
    assert (-RangeInt(30, -100, 100)).value == -30

def test_abs():
    assert abs(RangeInt(-10, -100, 100)).value == 10

def test_repr():
    assert repr(RangeInt(5, 0, 10)) == "RangeInt(5, min=0, max=10)"

def test_str():
    assert str(RangeInt(5, 0, 10)) == "5"

def test_relative_midpoint():
    assert RangeInt(75, 0, 100).relative() == 0.75

def test_relative_at_min():
    assert RangeInt(0, 0, 100).relative() == 0.0

def test_relative_at_max():
    assert RangeInt(100, 0, 100).relative() == 1.0

def test_lerp_to_midpoint():
    r = RangeInt(0, 0, 200)
    r.lerp_to(0.5)
    assert r.value == 100.0

def test_lerp_to_min():
    r = RangeInt(50, 0, 200)
    r.lerp_to(0.0)
    assert r.value == 0.0

def test_lerp_to_max():
    r = RangeInt(0, 0, 200)
    r.lerp_to(1.0)
    assert r.value == 200.0

def test_nudge_positive():
    r = RangeInt(50, 0, 100)
    r.nudge_percentage(0.1)
    assert r.value == 60

def test_nudge_negative():
    r = RangeInt(50, 0, 100)
    r.nudge_percentage(-0.2)
    assert r.value == 30

def test_edge_check_at_min():
    assert RangeInt(0, 0, 100).edge_check("min") is True

def test_edge_check_not_at_min():
    assert RangeInt(50, 0, 100).edge_check("min") is False

def test_edge_check_at_max():
    assert RangeInt(100, 0, 100).edge_check("max") is True

def test_edge_check_not_at_max():
    assert RangeInt(50, 0, 100).edge_check("max") is False

def test_edge_check_bad_arg():
    with pytest.raises(ValueError):
        RangeInt(50, 0, 100).edge_check("middle")

def test_is_between_true():
    assert RangeInt(50, 0, 100).is_between(0.25, 0.75) is True

def test_is_between_at_boundary():
    assert RangeInt(50, 0, 100).is_between(0.5, 1.0) is True

def test_is_between_false():
    assert RangeInt(50, 0, 100).is_between(0.6, 1.0) is False

def test_is_between_bad_low():
    with pytest.raises(ValueError):
        RangeInt(50, 0, 100).is_between(-0.1, 1.0)

def test_is_between_bad_high():
    with pytest.raises(ValueError):
        RangeInt(50, 0, 100).is_between(0.0, 1.1)

def test_set_range_clamps_value():
    r = RangeInt(80, 0, 100)
    r.set_range(0, 50)
    assert r.value == 50

def test_set_range_updates_max():
    r = RangeInt(10, 0, 100)
    r.set_range(0, 50)
    assert r.max == 50

def test_set_range_equal_raises():
    with pytest.raises(ValueError):
        RangeInt(10, 0, 100).set_range(5, 5)

def test_callback_fires_crossing_up():
    fired = []
    r = RangeInt(0, 0, 100)
    r._callbacks[0.5] = lambda: fired.append("hit")
    r.value = 60
    assert fired == ["hit"]

def test_callback_fires_crossing_down():
    fired = []
    r = RangeInt(100, 0, 100)
    r._callbacks[0.5] = lambda: fired.append("hit")
    r.value = 30
    assert fired == ["hit"]

def test_callback_does_not_fire_without_crossing():
    fired = []
    r = RangeInt(30, 0, 100)
    r._callbacks[0.5] = lambda: fired.append("hit")
    r.value = 35
    assert fired == []
