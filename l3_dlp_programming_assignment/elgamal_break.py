from bsgs import baby_step_giant_step


def int_to_text(value: int) -> str:
    byte_len = max(1, (value.bit_length() + 7) // 8)
    raw = value.to_bytes(byte_len, "big")
    decoded = raw.decode("ascii", errors="replace")
    return decoded if decoded.isprintable() else f"<non-text-bytes:{raw.hex()}>"


def main() -> None:
    p = 43223
    g = 378
    A = 6952
    c1 = 16241
    c2 = 17424

    a = baby_step_giant_step(g, A, p)
    if a is None:
        raise RuntimeError(
            "Could not recover private key a from public key A.")

    assert pow(g, a, p) == A

    shared_secret = pow(c1, a, p)
    shared_secret_inv = pow(shared_secret, -1, p)
    m = (c2 * shared_secret_inv) % p

    print(f"Recovered private key a = {a}")
    print(f"Recovered plaintext integer m = {m}")
    print("Secret message is the integer m above.")
    print(f"Byte/ASCII representation of m: {int_to_text(m)}")


if __name__ == "__main__":
    main()
