# An implementation of the MMO algorithm

from StringConversion import *
import os

# splits X into 128-bit chunks, left padding with 0's if necessary
# Then run the MMO hash function using H0, g and e as defined in the assignment description


def MMO(H0, X):
    """
    Implements the MMO hash function.
    Args:
        H0: Initial hash value (integer)
        X: Message to hash (integer)
    Returns:
        Final hash value (integer)
    """
    # Convert X to its binary representation
    X_bin = format(X, 'b')

    # Pad X to make its length a multiple of 128 bits
    block_size = 128
    padding_length = (block_size - (len(X_bin) % block_size)) % block_size
    X_bin = '0' * padding_length + X_bin

    # Split X into 128-bit blocks
    num_blocks = len(X_bin) // block_size
    blocks = [int(X_bin[i*block_size:(i+1)*block_size], 2)
              for i in range(num_blocks)]

    # Initialize H_prev
    H_prev = H0

    for M_i in blocks:
        # Compute k_i = g(H_prev)
        k_i = g(H_prev)
        # Compute E_k(M_i)
        E = E_k(M_i, k_i)
        # Compute H_i = E_k(M_i) XOR M_i XOR H_prev
        H_i = E ^ M_i ^ H_prev
        # Update H_prev
        H_prev = H_i

    return H_prev


def g(s):
    """
    Modified g function as per the assignment.
    If the last bit of s is 1, return s.
    If the last bit of s is 0, change the last bit to 1 and return.
    """
    # Convert to binary string of 128 bits
    s_bin = format(s, '0128b')

    # If the last bit is 1, return unchanged
    if s_bin[-1] == '1':
        return s

    # If the last bit is 0, change to 1 and convert back to integer
    s_bin = s_bin[:-1] + '1'
    return int(s_bin, 2)


def E_k(M, k):
    """
    Encryption function E_k(M) = (k * M) mod 2^128
    """
    modulo = 2 ** 128
    return (k * M) % modulo

# hashes the text in the file named by the first parameter
# the hash is written to the file named by the second parameter.


def MMO_hash(plaintextFileName, hashedValueFileName):
    # Generate a random 128-bit integer as H0
    import random
    global H0
    H0 = random.getrandbits(128)

    # Read plaintext from file
    with open(plaintextFileName, 'r') as infile:
        plaintext = infile.read()

    # Convert plaintext to integer
    X = stringToInteger(plaintext)

    # Compute the hash value
    final_H = MMO(H0, X)

    # Write the hash to the output file
    with open(hashedValueFileName, 'w') as outfile:
        outfile.write(str(final_H))


# main function to start off program
def main():
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Ensure the results directory exists
    results_dir = os.path.join(script_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)

    # Test Case 1
    global H0
    test1_input = os.path.join(script_dir, 'test1.txt')
    test1_output = os.path.join(script_dir, 'results', 'hash1.txt')

    # Force H0 to a specific value for reproducible testing
    H0 = 12345  # Fixed value for test case 1
    MMO_hash(test1_input, test1_output)

    # Test Case 2
    test2_input = os.path.join(script_dir, 'test2.txt')
    test2_output = os.path.join(script_dir, 'results', 'hash2.txt')

    # Different H0 value for test case 2
    H0 = 67890  # Fixed value for test case 2
    MMO_hash(test2_input, test2_output)


if __name__ == "__main__":
    main()
