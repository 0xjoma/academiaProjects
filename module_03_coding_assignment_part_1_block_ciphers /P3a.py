from StringConversion import *

# This file implements a block cipher algorithm that encrypts B bits at a time
# using XOR, permutation, and modular multiplication operations.


def permute(P, d):
    """
    Apply a permutation to a binary string.

    Args:
    P (list): Permutation array with values 0 to len(P)-1, each appearing once.
    d (str): Binary string of the same length as P.

    Returns:
    str: Permuted binary string.
    """
    permuted = ""
    for i in range(0, len(P)):
        permuted += d[P[i]]
    return permuted


def block_encrypt(x, w, P, k):
    """
    Encrypt a single block of binary data.

    Args:
    x (str): Input binary string to be encrypted.
    w (str): Binary string for XOR operation.
    P (list): Permutation array.
    k (int): Odd integer for modular multiplication.

    Returns:
    str: Encrypted binary string.
    """
    # Step 1: XOR x and w
    x_xor_w = xor(x, w)

    # Step 2: Apply permutation P
    x_permuted = permute(P, x_xor_w)

    # Step 3: Convert to integer, multiply by k, and take mod 2^B
    B = len(x)  # Block size is deduced from the length of x
    x_int = binaryStringToInteger(x_permuted)
    result = (x_int * k) % (2**B)

    # Convert result back to B-bit binary string
    return integerToBinaryString(result, B)


def encrypt(X, w, P, k):
    """
    Encrypt an arbitrary length binary string using block encryption.

    Args:
    X (str): Input binary string of arbitrary length.
    w (str): Binary string for XOR operation in each block.
    P (list): Permutation array for each block.
    k (int): Odd integer for modular multiplication in each block.

    Returns:
    str: Encrypted binary string.
    """
    B = len(w)  # Block size is deduced from the length of w

    # Pad X to make its length a multiple of B
    X = pad(X, B)

    # Split X into chunks of B bits
    chunks = [X[i:i+B] for i in range(0, len(X), B)]

    # Encrypt each chunk and concatenate the results
    Y = ''
    for chunk in chunks:
        Y += block_encrypt(chunk, w, P, k)
    return Y


# Test cases
if __name__ == "__main__":
    print("Test cases for block_encrypt")
    print(block_encrypt("11101", "01011", [4, 3, 1, 0, 2], 19))
    # Expected output: 10001
    print(block_encrypt("10100", "01001", [4, 3, 1, 0, 2], 17))
    # Expected output: 00111

    print("\nTest cases for encrypt:")
    print(encrypt("1101001011101", "01011", [4, 3, 1, 0, 2], 19))
    # Expected output: 011110001010001
    print(encrypt("1001111", "01011", [3, 1, 2, 4, 0], 17))
    # Expected output: 0101000100
    print(encrypt("11101100100101101011011010001101",
          "01011", [4, 3, 1, 0, 2], 19))
    # Expected output: 01100101011100001011010110110101011
