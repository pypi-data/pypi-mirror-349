from timeir import holiday_occasion


def test_holiday():
    assert holiday_occasion(1403, 1, 1) == 'جشن نوروز/جشن سال نو'


def test_not_a_holiday():
    assert holiday_occasion(1403, 6, 21) is None
