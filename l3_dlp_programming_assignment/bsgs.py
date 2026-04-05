import math


def baby_step_giant_step(g: int, h: int, p: int) -> int | None:
    if p <= 2:
        raise ValueError("p must be an odd prime greater than 2")
    if not (0 < g < p) or not (0 < h < p):
        raise ValueError("g and h must satisfy 0 < value < p")

    order = p - 1
    m = math.isqrt(order)
    if m * m < order:
        m += 1

    baby_steps: dict[int, int] = {}
    value = 1
    for j in range(m):
        if value not in baby_steps:
            baby_steps[value] = j
        value = (value * g) % p

    g_inv = pow(g, -1, p)
    g_inv_m = pow(g_inv, m, p)

    gamma = h
    for i in range(m + 1):
        j = baby_steps.get(gamma)
        if j is not None:
            x = i * m + j
            if pow(g, x, p) == h:
                return x
        gamma = (gamma * g_inv_m) % p

    return None


def _self_test() -> None:
    p = 1019
    g = 2
    secret = 137
    h = pow(g, secret, p)

    recovered = baby_step_giant_step(g, h, p)
    if recovered is None:
        raise RuntimeError("No discrete logarithm found in self-test.")
    assert pow(g, recovered, p) == h
    print(f"Self-test passed: recovered x = {recovered}")


if __name__ == "__main__":
    _self_test()
