# DES implementation
# The array data is a python array of string 1's and 0's; e.g. ['1', '0', '0', '0', '1', '0', '0', '0']

from StringConversion import *
# Provides string,array XOR function and methods to convert between strings, arrays, etc.

IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9,  1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

IP_inv = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9,  49, 17, 57, 25]

EBox = [32, 1,  2,  3,  4,  5,
        4,  5,  6,  7,  8,  9,
        8,  9,  10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1]

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

PBox = [16, 7,  20, 21, 29, 12, 28, 17,
        1,  15, 23, 26, 5,  18, 31, 10,
        2,  8,  24, 14, 32, 27, 3,  9,
        19, 13, 30, 6,  22, 11, 4,  25]

# Key permutations
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1,  58, 50, 42, 34, 26, 18,
       10, 2,  59, 51, 43, 35, 27,
       19, 11, 3,  60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7,  62, 54, 46, 38, 30, 22,
       14, 6,  61, 53, 45, 37, 29,
       21, 13, 5,  28, 20, 12, 4]


PC2 = [14, 17, 11, 24, 1,  5,  3, 28,
       15, 6,  21, 10, 23, 19, 12, 4,
       26, 8,  16, 7,  27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40,
       51, 45, 33, 48, 44, 49, 39, 56,
       34, 53, 46, 42, 50, 36, 29, 32]

# DES functions implemented
# Input is plaintext/ciphertext of 64 bits
# Output is permuted array of 64 bits


def initial_permutation(array):
    permuted = []
    for x in IP:
        permuted.append(array[x - 1])
    return permuted

# Input is output from last round
# Output is ciphertext/plaintext of 64 bits


def final_permutation(array):
    permuted = []
    for x in IP_inv:
        permuted.append(array[x - 1])
    return permuted

# Input is array of 32 bits from right half of previous round
# Output is 48 bit array that results from EBox expansion


def e_box(half_array):
    expanded = []
    for x in EBox:
        expanded.append(half_array[x - 1])
    return expanded

# Input is array of 48 bits from EBox expansion XOR'ed with the round key
# Output is a 32 bit array that results from concatenating SBox outputs


def s_boxes(half_array):
    collapsed = []
    for x in range(8):
        block = half_array[(x * 6):((x * 6) + 6)]
        collapsed.extend(s_box(block, x))
    return collapsed

# Input is block of 6 bits and which SBox to look it up with
# Output is a 4 bit block that is a result of the SBox lookup


def s_box(block, i):
    row_block = []
    row_block.append(block[0])
    row_block.append(block[5])
    row = int(''.join(row_block), 2)
    col = int(''.join(block[1:5]), 2)
    return list(bin(SBox[i][row][col])[2:].zfill(4))

# Input is array of 32 bits from SBox output
# Output is 32 bit array result of round function f


def p_box(half_array):
    permuted = []
    for x in PBox:
        permuted.append(half_array[x - 1])
    return permuted

# Input is array of 32 bits from right half of previous round, and 48 bit round key
# Output is 32 bit array that is XOR'ed with left half of previous round
# Uses xor from StringConversion.py


def round_function_F(half_array, round_key):
    '''
    Implement the following expression using helper functions:
    PBox(SBoxes( EBox(half_array) ^ round_key))
    '''
    # XOR e_box output with round_key
    xor_val = xor(e_box(half_array), round_key)
    return p_box(s_boxes(xor_val))

# Pad a long message with the one and zeroes method
# Returns padded message


def addOneAndZeroesPadding(plaintext_message):
    """Add padding using OneAndZeroes method

    For block size B=8 bytes (64 bits):
    1. Always add 0x80 (10000000) first
    2. Then add zeros until reaching multiple of 64 bits
    """
    # Ensure we're working with a string
    plaintext = plaintext_message

    # Add padding marker (0x80)
    plaintext += "10000000"

    # Calculate padding needed
    padding_needed = 64 - (len(plaintext) % 64)
    if padding_needed == 64 and len(plaintext) > 0:
        # If already at block boundary, add full block of padding
        plaintext += "0" * 56  # 7 bytes of zeros after 0x80
    else:
        # Add zeros to reach block boundary
        plaintext += "0" * padding_needed

    return plaintext


def removeOneAndZeroesPadding(padded_plaintext_message):
    """Remove OneAndZeroes padding"""
    # Find the padding marker
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


def round_i(array, key_i, round_num=1):  # Add round_num parameter
    # Extract left and right halves
    L_i_minus_one = array[:32]
    R_i_minus_one = array[32:]

    # Compute f function with debugging
    E_output = e_box(R_i_minus_one)
    xor_result = list(xor(E_output, key_i))
    s_box_output = s_boxes(xor_result)
    f_result = p_box(s_box_output)

    # Compute new L and R
    L_i = R_i_minus_one  # Already a list
    R_i = list(xor(L_i_minus_one, f_result))

    return L_i + R_i

# COMPLETE
# Input is string array of 64 bits representing key, string array of 56 bits representing current intermediate key, and round number i
# Output is 48 bit string array that is the encryption round key for round i, and the intermediate key for next round
# Function is called 16 times during encryption, for i = 1 to 16


def encryption_round_key(key, intermediate_key, i):
    '''
    Generate the encryption round key for round i.
    '''
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

    current = initial_permutation(plaintext)

    intermediate_key = []

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
    """Generate round key for DES decryption"""
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

    # Initial permutation
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
    # Convert key to string array of bits:
    key = list(integerToBinaryString(int(key, 2)))

    # Then convert plaintext to string array of bits and then pad the input using the AddOneAndZeroesPadding method
    # padded_plaintext_message = addOneAndZeroesPadding(integerToBinaryString(int(plaintext_message, 2)));
    # print("padded_plaintext_message text",padded_plaintext_message)
    padded_plaintext_message = list(addOneAndZeroesPadding(
        integerToBinaryString(int(plaintext_message, 2))))

    # then break message into 64 bit chunks and encrypt each of the chunks, concatenating the chunks finally:
    ciphertext = []

    for x in range(int(len(padded_plaintext_message) / 64)):
        plaintext = padded_plaintext_message[(x * 64):((x * 64) + 64)]
        C_i_minus_one = encrypt(plaintext, key)
        ciphertext.extend(C_i_minus_one)

    return ''.join(ciphertext)

# Decrypt a long hexadecimal message using ECB mode
# ciphertext and decrypted plaintext returned are strings
# You will call decrypt


def decrypt_message(ciphertext_message, key):
    key = list(integerToBinaryString(int(key, 2)))
    ciphertext_message = list(
        integerToBinaryString(int(ciphertext_message, 2)))

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
    # Professor instructions
    # Call DES_decrypt and DES_decrypt as appropriate

    # Test case:
    # plaintext = "68656c6c6f", padded="68656C6C6F800000"
    # key = "413f4428472b4b62"
    # plaintext in binary= "0110100001100101011011000110110001101111"
    # key in binary = "0100000100111111010001000010100001000111001010110100101101100010"
    # expected ciphertext in binary, after encryption and padding = "1001100101110010110001001111110010001100010011101011101011010010"

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

    # Test case 2 using plainttext1.txt and keysecret2.txt
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
