# DES (Data Encryption Standard) Implementation
# This implementation processes data as arrays of binary strings, where each element
# is either '0' or '1'. Example: ['1', '0', '0', '0', '1', '0', '0', '0']

from StringConversion import *
# StringConversion.py provides utility functions:
# - XOR operations between binary strings
# - Conversion methods between strings, arrays, and binary formats

# Initial Permutation (IP) table
# Rearranges the 64 input bits according to this fixed pattern
# Example: bit 58 of input becomes bit 1 of output, bit 50 becomes bit 2, etc.

IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9,  1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Final Permutation (IP^-1) table
# Reverses the initial permutation. Used as the final step of both encryption and decryption
IP_inv = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9,  49, 17, 57, 25]

# Expansion Box (E-box) table
# Expands 32-bit input to 48 bits by repeating certain bits
# Used in the Feistel function before XOR with round key
EBox = [32, 1,  2,  3,  4,  5,
        4,  5,  6,  7,  8,  9,
        8,  9,  10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1]

# S-boxes (Substitution boxes)
# Each S-box transforms 6 input bits into 4 output bits
# This is the core of DES security, providing non-linearity
SBox = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
     ],

    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
     ],

    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
     ],

    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
     ],

    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
     ],

    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
     ],

    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
     ],

    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
     ]
]

# Permutation Box (P-box) table
# Performs straight permutation on 32-bit input after S-box substitution
PBox = [16, 7,  20, 21, 29, 12, 28, 17,
        1,  15, 23, 26, 5,  18, 31, 10,
        2,  8,  24, 14, 32, 27, 3,  9,
        19, 13, 30, 6,  22, 11, 4,  25]

# Key Schedule Permutations

# Permuted Choice 1 (PC-1)
# Reduces 64-bit key to 56 bits by removing parity bits
# Also permutes the bits according to this table
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1,  58, 50, 42, 34, 26, 18,
       10, 2,  59, 51, 43, 35, 27,
       19, 11, 3,  60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7,  62, 54, 46, 38, 30, 22,
       14, 6,  61, 53, 45, 37, 29,
       21, 13, 5,  28, 20, 12, 4]

# Permuted Choice 2 (PC-2)
# Reduces 56-bit key to 48 bits for each round
# Also permutes the bits according to this table
PC2 = [14, 17, 11, 24, 1,  5,  3, 28,
       15, 6,  21, 10, 23, 19, 12, 4,
       26, 8,  16, 7,  27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40,
       51, 45, 33, 48, 44, 49, 39, 56,
       34, 53, 46, 42, 50, 36, 29, 32]


def initial_permutation(array):
    """
    Performs the initial permutation (IP) on the 64-bit input block.

    Args:
        array: List of 64 binary digits (as strings)

    Returns:
        List of 64 binary digits after permutation
    """
    permuted = []
    for x in IP:
        permuted.append(array[x - 1])
    return permuted


def final_permutation(array):
    """
    Performs the final permutation (IP^-1) on the 64-bit block. This is the inverse
    of the initial permutation and is the last step in both encryption and decryption.

    Args:
        array: List of 64 binary digits (as strings) from the last round

    Returns:
        List of 64 binary digits representing the final ciphertext/plaintext block
    """
    permuted = []
    for x in IP_inv:
        permuted.append(array[x - 1])
    return permuted


def e_box(half_array):
    """
    Performs the expansion permutation (E-box) on a 32-bit half-block.
    Expands the input from 32 bits to 48 bits by duplicating certain bits.
    This expansion matches the 48-bit round key size for the XOR operation.

    Args:
        half_array: List of 32 binary digits (right half of the current block)

    Returns:
        List of 48 binary digits after expansion
    """
    expanded = []
    for x in EBox:
        expanded.append(half_array[x - 1])
    return expanded


def s_boxes(half_array):
    """
    Applies all eight S-box transformations to convert 48 bits back to 32 bits.
    Each S-box takes 6 bits and produces 4 bits, providing the critical
    non-linear component of DES.

    Args:
        half_array: List of 48 binary digits (from E-box XOR with round key)

    Returns:
        List of 32 binary digits after S-box substitutions
    """
    collapsed = []
    for x in range(8):
        # Process each 6-bit block through its corresponding S-box
        block = half_array[(x * 6):((x * 6) + 6)]
        collapsed.extend(s_box(block, x))
    return collapsed


def s_box(block, i):
    """
    Performs substitution using a single S-box.
    The 6 input bits are used as follows:
    - Bits 1 and 6 form the row number (0-3) in binary
    - Bits 2-5 form the column number (0-15) in binary

    Args:
        block: List of 6 binary digits to process
        i: Index (0-7) indicating which S-box to use

    Returns:
        List of 4 binary digits representing the S-box output
    """
    row_block = []
    row_block.append(block[0])    # First bit
    row_block.append(block[5])    # Last bit
    row = int(''.join(row_block), 2)    # Convert to row number (0-3)
    col = int(''.join(block[1:5]), 2)    # Convert to column number (0-15)
    return list(bin(SBox[i][row][col])[2:].zfill(4))


def p_box(half_array):
    """
    Performs the straight permutation (P-box) after S-box substitution.
    This permutation helps diffuse the S-box outputs across the entire block.

    Args:
        half_array: List of 32 binary digits from S-box output

    Returns:
        List of 32 binary digits after permutation
    """
    permuted = []
    for x in PBox:
        permuted.append(half_array[x - 1])
    return permuted


def round_function_F(half_array, round_key):
    """
    Implements the Feistel (F) function used in each round of DES.
    The F function steps are:
    1. Expand 32 bits to 48 bits (E-box)
    2. XOR with 48-bit round key
    3. Transform through S-boxes back to 32 bits 
    4. Permute the result (P-box)

    Args:
        half_array: List of 32 binary digits (right half of current block)
        round_key: List of 48 binary digits (key for this round)

    Returns:
        List of 32 binary digits to be XORed with the left half
    """
    xor_val = xor(e_box(half_array), round_key)
    return p_box(s_boxes(xor_val))


def addOneAndZeroesPadding(plaintext_message):
    """
    Implements the OneAndZeroes padding scheme for messages not multiple of 64 bits.

    Padding rules:
    1. Always append '10000000' (0x80 in hex)
    2. Then append zeros until the message length is a multiple of 64 bits
    If message is already a multiple of 64 bits, add a full block of padding.

    Args:
        plaintext_message: Binary string to be padded

    Returns:
        Padded binary string with length multiple of 64 bits
    """
    plaintext = plaintext_message
    plaintext += "10000000"

    padding_needed = 64 - (len(plaintext) % 64)
    if padding_needed == 64 and len(plaintext) > 0:
        plaintext += "0" * 56
    else:
        plaintext += "0" * padding_needed

    return plaintext


def removeOneAndZeroesPadding(padded_plaintext_message):
    """
    Removes OneAndZeroes padding after decryption.
    Locates the first '10000000' marker and removes it and all subsequent padding.

    Args:
        padded_plaintext_message: Binary string with padding

    Returns:
        Original message with padding removed
    """
    marker_pos = padded_plaintext_message.find('10000000')
    if marker_pos != -1:
        return padded_plaintext_message[:marker_pos]
    return padded_plaintext_message

# COMPLETE THESE FUNCTIONS
# ---------------------------------------------------------------

# COMPLETE
# Input is string array of 64 bits, output is string array of 64 bits for next round
# Used in both encryption and decryption phases
# Use xor from StringConversion.py
# Pseudo code below


def round_i(array, key_i, round_num=1):
    """
    Performs one round of the DES Feistel network.
    Each round performs these steps:
    1. Split input block into left and right halves
    2. New left half = old right half
    3. New right half = old left half XOR F(old right half, round key)

    Args:
        array: List of 64 binary digits (current block state)
        key_i: List of 48 binary digits (round key)
        round_num: Current round number (1-16)

    Returns:
        List of 64 binary digits for next round
    """
    L_i_minus_one = array[:32]    # Left half
    R_i_minus_one = array[32:]    # Right half

    # Apply Feistel function F
    E_output = e_box(R_i_minus_one)
    xor_result = list(xor(E_output, key_i))
    s_box_output = s_boxes(xor_result)
    f_result = p_box(s_box_output)

    # Compute new L and R values
    L_i = R_i_minus_one  # Right becomes new left
    R_i = list(xor(L_i_minus_one, f_result))    # New right = left XOR f(right)

    return L_i + R_i

# COMPLETE
# Input is string array of 64 bits representing key, string array of 56 bits representing current intermediate key, and round number i
# Output is 48 bit string array that is the encryption round key for round i, and the intermediate key for next round
# Function is called 16 times during encryption, for i = 1 to 16


def encryption_round_key(key, intermediate_key, i):
    """
    Generates the round key for encryption round i.
    The process involves:
    1. First round: Apply PC-1 to reduce 64-bit key to 56 bits
    2. Split into 28-bit C and D halves
    3. Perform left circular shifts based on the round number
    4. Apply PC-2 to generate 48-bit round key

    Args:
        key: List of 64 binary digits (original key)
        intermediate_key: List of 56 binary digits (from previous round)
        i: Round number (1-16)

    Returns:
        Tuple (round_key, intermediate_key):
            round_key: List of 48 binary digits for this round
            intermediate_key: List of 56 binary digits for next round
    """
    # Left shifts per round
    shifts_per_round = [1, 1, 2, 2, 2, 2, 2, 2,
                        1, 2, 2, 2, 2, 2, 2, 1]

    # First round: perform PC1 permutation
    if i == 1:
        # Apply the PC1 permutation to the key
        intermediate_key = [key[x - 1] for x in PC1]

    # Split into C and D blocks (28 bits each)
    C = intermediate_key[:28]
    D = intermediate_key[28:]

    # Determine the number of left shifts for this round
    shifts = shifts_per_round[i - 1]

    # Perform circular left shifts
    C = C[shifts:] + C[:shifts]
    D = D[shifts:] + D[:shifts]

    # Combine C and D
    combined_key = C + D

    # Update intermediate_key for the next round
    intermediate_key = combined_key

    # Apply the PC2 permutation to get the round key
    round_key = [combined_key[x - 1] for x in PC2]

    return round_key, intermediate_key

# COMPLETE
# Input is plaintext string array of 64 bits, key string array of 64 bits
# Output is 64 bit string array ciphertext
# Uses encryption_round_key() and round_i() methods


def encrypt(plaintext, key):
    """
    Main DES encryption function that processes a 64-bit block.
    The encryption process consists of:
    1. Initial permutation
    2. 16 rounds of Feistel network operations
    3. Final 32-bit half swap
    4. Final permutation

    Args:
        plaintext: List of 64 binary digits to encrypt
        key: List of 64 binary digits (original key)

    Returns:
        List of 64 binary digits representing encrypted block
    """
    current = initial_permutation(plaintext)
    intermediate_key = []

    # Perform 16 rounds of encryption
    for i in range(1, 17):
        round_key, intermediate_key = encryption_round_key(
            key, intermediate_key, i)
        current = round_i(current, round_key, i)  # Pass round number

    current = current[32:] + current[:32]  # Final swap

    result = final_permutation(current)

    return result

    # COMPLETE
    # Input is string array of 64 bits representing key, string array of 56 bits representing current intermediate key, and round number i
    # Output is 48 bit string array that is the decryption round key for round i, and the intermediate key for next round
    # Function is called 16 times during decryption, for i = 16 down to 1


def decryption_round_key(key, intermediate_key, i):
    """
    Generates round keys for DES decryption.
    For decryption, we use the same keys as encryption but in reverse order.
    Round i of decryption uses the key from round (17-i) of encryption.

    Args:
        key: List of 64 binary digits (original key)
        intermediate_key: List of 56 binary digits (unused in decryption)
        i: Current decryption round (1-16)

    Returns:
        Tuple (round_key, intermediate_key):
            round_key: List of 48 binary digits for this round
            intermediate_key: Preserved for consistency with encryption
    """
    # For decryption, we use the encryption keys in reverse order
    encryption_keys = []
    temp_intermediate = []

    # Generate all encryption keys first
    for j in range(1, 17):
        k, temp_intermediate = encryption_round_key(key, temp_intermediate, j)
        encryption_keys.append(k)

    # Return the appropriate key - for round i of decryption, use round (17-i) of encryption
    return encryption_keys[16-i], intermediate_key

# COMPLETE
# Input is ciphertext string array of 64 bits, key string array of 64 bits
# Output is 64 bit string array plaintext
# Uses decryption_round_key() and round_i() methods


def decrypt(ciphertext, key):
    """
    Main DES decryption function that processes a 64-bit block.
    Decryption uses the same algorithm as encryption but with keys in reverse order.
    Steps are:
    1. Initial permutation
    2. 16 rounds using decryption keys (encryption keys in reverse)
    3. Final 32-bit half swap
    4. Final permutation

    Args:
        ciphertext: List of 64 binary digits to decrypt
        key: List of 64 binary digits (original key)

    Returns:
        List of 64 binary digits representing decrypted block
    """
    current = initial_permutation(ciphertext)

    # Generate all encryption round keys
    encryption_keys = []
    intermediate_key = []
    for i in range(1, 17):
        round_key, intermediate_key = encryption_round_key(
            key, intermediate_key, i)
        encryption_keys.append(round_key)

    # Reverse the keys for decryption
    decryption_keys = encryption_keys[::-1]

    # Perform 16 rounds with reversed keys
    for i in range(1, 17):
        round_key = decryption_keys[i - 1]
        current = round_i(current, round_key, i)

    # Swap the halves after the 16th round
    current = current[32:] + current[:32]

    # Final permutation
    result = final_permutation(current)

    return result

    # The methods below have also been implemented for you
    # --------------------------------------------------------------------------------
    # Encrypt a long hexadecimal message using ECB mode
    # plaintext message and encrypted ciphertext returned are strings
    # You will call encrypt


def encrypt_message(plaintext_message, key):
    """
    Encrypts a message of arbitrary length using DES in ECB mode.
    Electronic Code Book (ECB) mode processes each 64-bit block independently.
    Steps:
    1. Convert key to binary
    2. Pad message to multiple of 64 bits
    3. Split into 64-bit blocks
    4. Encrypt each block separately
    5. Concatenate results

    Args:
        plaintext_message: Binary string to encrypt
        key: Binary string of 64 bits

    Returns:
        Binary string containing concatenated encrypted blocks
    """
    # Convert key to binary array
    key = list(integerToBinaryString(int(key, 2)))

    # Convert and pad plaintext message
    padded_plaintext_message = list(addOneAndZeroesPadding(
        integerToBinaryString(int(plaintext_message, 2))))

    # Encrypt each 64-bit block
    ciphertext = []

    for x in range(int(len(padded_plaintext_message) / 64)):
        plaintext = padded_plaintext_message[(x * 64):((x * 64) + 64)]
        C_i_minus_one = encrypt(plaintext, key)
        ciphertext.extend(C_i_minus_one)

    return ''.join(ciphertext)


def decrypt_message(ciphertext_message, key):
    """
    Decrypts a message encrypted with DES in ECB mode.
    Steps:
    1. Convert key and ciphertext to binary
    2. Split ciphertext into 64-bit blocks
    3. Decrypt each block separately
    4. Concatenate results
    5. Remove padding

    Args:
        ciphertext_message: Binary string containing encrypted data
        key: Binary string of 64 bits

    Returns:
        Original plaintext with padding removed
    """
    key = list(integerToBinaryString(int(key, 2)))
    ciphertext_message = list(
        integerToBinaryString(int(ciphertext_message, 2)))

    # Process each 64-bit block
    plaintext = []
    for x in range(int(len(ciphertext_message) / 64)):
        C_i = ciphertext_message[(x * 64):((x * 64) + 64)]
        P_i = decrypt(C_i, key)
        plaintext.extend(P_i)

    padded_plaintext_message = ''.join(plaintext)

    plaintext_message = removeOneAndZeroesPadding(padded_plaintext_message)

    return plaintext_message


'''
Encrypts the text in the file named by the first parameter with the 64 bit key in the file  named in the second parameter. 
The encrypted text is output to the file named by the  third parameter
'''


def DES_encrypt(plaintextFileName, keyFileName, ciphertextFileName):
    """
    File-based interface for DES encryption.
    Reads plaintext and key from files, encrypts data, writes result to file.
    Supports multiple key formats:
    - 64-bit binary string
    - 16-character hex string
    - ASCII string (converted to binary)

    Args:
        plaintextFileName: Input file containing plaintext
        keyFileName: Input file containing encryption key
        ciphertextFileName: Output file for encrypted data
    """
    # Read plaintext
    try:
        with open(plaintextFileName, "r") as textfile:
            plaintext = textfile.readline().rstrip()
    except FileNotFoundError:
        print(f"Error: The file {plaintextFileName} does not exist.")
        return

    # Read key
    with open(keyFileName, "r") as textfile:
        key = textfile.readline().rstrip()

    # Detect key format and convert to binary if necessary
    if all(c in '01' for c in key) and len(key) == 64:
        # Key is already a 64-bit binary string
        pass
    elif all(c in '0123456789abcdefABCDEF' for c in key) and len(key) == 16:
        # Key is a 16-character hexadecimal string
        key = bin(int(key, 16))[2:].zfill(64)
    else:
        # Assume key is in ASCII format, convert to binary
        key = ''.join(format(ord(c), '08b') for c in key)
        key = key[:64]  # Ensure the key is 64 bits

    if len(key) != 64:
        print("Error: The key must be a 64-bit binary string.")
        return

    # Encrypt
    ciphertext = encrypt_message(plaintext, key)

    print("\nDES Encryption Results")
    print("--------------------------")
    print("Input:")
    print(f"Plaintext Binary: {plaintext}")
    print(f"Key: {key}")
    print("\nOutput:")
    print(f"Ciphertext: {ciphertext}")
    print("--------------------------")

    # Write encrypted ciphertext
    with open(ciphertextFileName, "w") as textfile:
        textfile.write(ciphertext)


'''
Decrypts the text in the file named by the first parameter with the 64 bit key in the file  named in the second parameter. 
The decrypted text is written to the file named by the  third parameter. 
'''


def DES_decrypt(ciphertextFileName, keyFileName, plaintextFileName):
    """
    File-based interface for DES decryption.
    Reads ciphertext and key from files, decrypts data, writes result to file.
    Supports same key formats as encryption.
    Also converts decrypted binary back to hex for verification.

    Args:
        ciphertextFileName: Input file containing encrypted data
        keyFileName: Input file containing decryption key
        plaintextFileName: Output file for decrypted data
    """
    # Read ciphertext
    with open(ciphertextFileName, "r") as textfile:
        ciphertext = textfile.readline().rstrip()

    # Read key
    with open(keyFileName, "r") as textfile:
        key = textfile.readline().rstrip()

    # Detect key format and convert to binary if necessary
    if all(c in '01' for c in key) and len(key) == 64:
        # Key is already a 64-bit binary string
        pass
    elif all(c in '0123456789abcdefABCDEF' for c in key) and len(key) == 16:
        # Key is a 16-character hexadecimal string
        key = bin(int(key, 16))[2:].zfill(64)
    else:
        # Assume key is in ASCII format, convert to binary
        key = ''.join(format(ord(c), '08b') for c in key)
        key = key[:64]  # Ensure the key is 64 bits

    if len(key) != 64:
        print("Error: The key must be a 64-bit binary string.")
        return

    # Decrypt
    plaintext = decrypt_message(ciphertext, key)

    print("\nDES Decryption Results:")
    print("--------------------------")
    print("Input:")
    print(f"Ciphertext: {ciphertext}")
    print(f"Key: {key}")
    print("\nOutput:")
    print(f"Decrypted Binary: {plaintext}")
    decrypted_hex = format(int(plaintext, 2), 'x')
    print(f"Decrypted Hex: {decrypted_hex}")
    print("--------------------------")

    # Write decrypted plaintext
    with open(plaintextFileName, "w") as textfile:
        textfile.write(plaintext)

# Function to test DES


def testEncryptionAndDecryption():
    """
    Test function for DES implementation.
    Runs two test cases:
    1. Using plaintext1.txt with keysecret1.txt
    2. Using plaintext1.txt with keysecret2.txt

    Test values:
    - Sample plaintext (hex): "68656c6c6f"
    - Sample padded: "68656C6C6F800000"
    - Sample key: "413f4428472b4b62"
    - Binary representations are shown in comments

    Verifies encryption/decryption cycle produces original plaintext
    """
    print("\nTest Case 1 - Using plaintext1.txt and keysecret1.txt")
    # Hard code the file names here
    plaintextFileName = "final_project_deliverable_1/plaintext1.txt"
    secretKeyFileName = "final_project_deliverable_1/keySecret1.txt"

    ciphertextFileName = "ciphertext.txt"  # generated by encrypt process
    # Run the encrypt process
    DES_encrypt(plaintextFileName, secretKeyFileName, ciphertextFileName)

    plaintextFileName2 = "plaintext2.txt"  # generated by decrypt process
    # Run the decrypt process
    DES_decrypt(ciphertextFileName, secretKeyFileName, plaintextFileName2)

    # Test case 2 using plaintext1.txt and keysecret2.txt
    print("\nTest Case 2 - keysecret2.txt")
    secretKeyFileName2 = "final_project_deliverable_1/keySecret2.txt"
    ciphertextFileName2 = "ciphertext2.txt"
    DES_encrypt(plaintextFileName, secretKeyFileName2, ciphertextFileName2)
    plaintextFileName3 = "plaintext3.txt"
    DES_decrypt(ciphertextFileName2, secretKeyFileName2, plaintextFileName3)

# Professor instructions
# Now visually compare plaintextFileName and plaintextFileName2 to verify they are identical

# main function to start off program; it may call helper functions


def main():
    testEncryptionAndDecryption()


if __name__ == "__main__":
    main()
