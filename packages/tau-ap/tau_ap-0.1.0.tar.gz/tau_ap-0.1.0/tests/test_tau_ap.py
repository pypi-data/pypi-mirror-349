from tau_ap import tau_ap

def test_tau_ap():
    x = [1, 2, 3, 4, 5, 6]
    y = [3, 1, 2, 4, 6, 5]
    expected = 0.32000000000000006
    result = tau_ap(x, y)
    assert abs(result - expected) < 1e-9, f"Expected {expected}, got {result}"
