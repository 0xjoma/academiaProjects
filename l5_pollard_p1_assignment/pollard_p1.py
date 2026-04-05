import math


def pollard_p1(n: int, max_steps: int = 2_000_000) -> int | None:
    """Return a non-trivial factor of n using Pollard's p-1 method.

    The search is bounded by max_steps to avoid infinite loops.
    """
    a = 2
    b = a % n
    j = 2

    while j <= max_steps:
        b = pow(b, j, n)
        d = math.gcd(b - 1, n)

        if 1 < d < n:
            return d

        if d == n:
            return None

        j += 1

    return None


def main() -> None:
    N = 1034101221388914603469
    p = pollard_p1(N)

    if p is None:
        raise RuntimeError("Pollard's p-1 failed within the step limit.")

    q = N // p
    assert p * q == N

    print(f"N = {N}")
    print(f"p = {p}")
    print(f"q = {q}")


if __name__ == "__main__":
    main()
