import itertools as it

from StringConversion import *

# This file implements a block cipher algorithm that encrypts B bits at a time
# using XOR, permutation, and modular multiplication operations.

# The total runtime is ~1.49 seconds
# The runtime can be improved further by using "lru_cache" to store the results of the block_encrypt function


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

###################################################
# Part B - Question 1
###################################################


def question1():
    """
    This function calculates the number of keys that encrypt a specific
    7-bit plaintext to a given ciphertext. It explores the entire keyspace
    to determine how many keys produce the desired encryption.
    """
    print("Question 1:")
    B = 7  # Block size
    x = "1010110"  # Plaintext
    y = "0011011"  # Ciphertext
    keyspace = 0  # Total number of possible keys
    numKeys = 0  # Number of keys that produce the correct ciphertext

    # Iterate through all possible permutations
    for P in [list(t) for t in it.permutations(range(B))]:
        # Iterate through all possible 7-bit strings for w
        for w in it.product("01", repeat=B):
            # Iterate through all possible odd numbers from 1 to 127 for k
            for k in range(1, 2**B, 2):
                w_str = "".join(w)
                # Check if this key (w, P, k) produces the correct ciphertext
                if block_encrypt(x, w_str, P, k) == y:
                    numKeys += 1
                keyspace += 1
    print(f"Total keyspace: {keyspace}, Number of valid keys {numKeys}")


# Testing question 1:
question1()

###################################################
# Part B - Question 2
###################################################


def question2():
    """
    This function calculates the number of keys that correctly encrypt two
    different plaintext-ciphertext pairs. It demonstrates how additional
    known plaintext-ciphertext pairs can reduce the number of valid keys.
    """
    print("\nQuestion 2:")
    B = 7  # Block size
    x1 = "1010110"  # First known plaintext
    y1 = "0011011"  # First known ciphertext
    x2 = "0010111"  # Second known plaintext
    y2 = "1100100"  # Second known ciphertext
    keyspace = 0  # Total number of possible keys
    numKeys = 0  # Number of keys that produce the correct ciphertext

    # Iterate through all possible permutations
    for P in [list(t) for t in it.permutations(range(B))]:
        # Iterate through all possible 7-bit strings for w
        for w in it.product("01", repeat=B):
            # Iterate through all possible odd numbers from 1 to 127 for k
            for k in range(1, 2**B, 2):
                w_str = "".join(w)
                # Check if this key (w, P, k) produces the correct ciphertext for both ciphertexts
                if block_encrypt(x1, w_str, P, k) == y1 and block_encrypt(x2, w_str, P, k) == y2:
                    numKeys += 1
                keyspace += 1

    print(f"Total keyspace: {keyspace}, Number of valid keys {numKeys}")


# Testing question2:
question2()

###################################################
# Part B - Question 3
###################################################


def question3():
    """
    This function examines the diffusion property of the block cipher.
    It encrypts a given plaintext, then changes each bit of the plaintext
    one at a time and observes how many bits change in the resulting ciphertext.
    The average number of bits changed is calculated to assess the strength
    of the cipher's diffusion property.
    """
    print("\nQuestion 3:")
    X = "1100100100111010101101110"  # Original plaintext
    B = 7  # Block size
    w = "1111000"  # Known w value
    P = [6, 5, 4, 3, 2, 1, 0]  # Known permutation
    k = 17  # Known k value

    # Step 3(a): Encrypt the original plaintext
    Y = encrypt(X, w, P, k)
    print(f"Original ciphertext: {Y}")

    # Step 3(b): Change each bit and count differences
    total_diff = 0
    for i in range(len(X)):
        # Flip the i-th bit of the plaintext
        X_modified = X[:i] + ("1" if X[i] == "0" else "0") + X[i+1:]
        # Encrypt the modified plaintext
        Y_modified = encrypt(X_modified, w, P, k)
        # Count the number of differing bits in the ciphertext
        diff = sum(y1 != y2 for y1, y2 in zip(Y, Y_modified))
        total_diff += diff
        print(f"Bit {i+1} changed: {diff} bits different in ciphertext")

    # Step 3(c): Compute average
    avg_diff = total_diff / len(X)
    print(f"Average number of bits changed: {avg_diff}")


# Testing question3:
question3()
