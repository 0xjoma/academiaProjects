# DES (Data Encryption Standard) Implementation
This project implements the DES (Data Encryption Standard) encryption algorithm in Python, including both encryption and decryption functionality using Electronic Codebook (ECB) mode.

## Project Structure
```
.
.
├── DES.py                  # Main DES implementation with test cases
├── StringConversion.py     # Utility functions for binary/string conversions
├── plaintext1.txt         # Sample plaintext file containing binary input
├── keySecret1.txt         # First sample key file (binary format)
├── keySecret2.txt         # Second sample key file (hex format)
├── resources/            # Contains academic research and documentation about DES
└── results/             # Contains output files from encryption/decryption
    ├── ciphertext.txt   # Encrypted output from Test Case 1
    ├── plaintext2.txt   # Decrypted output from Test Case 1
    ├── ciphertext2.txt  # Encrypted output from Test Case 2
    └── plaintext3.txt   # Decrypted output from Test Case 2
```

## Prerequisites
- Python 3.x

## Files Required
1. Input plaintext file containing binary string (e.g., "0110100001100101011011000110110001101111")
2. Key file containing either:
   - 64-bit binary string
   - 16-character hexadecimal string

## Running the Implementation
```bash
python DES.py
```

This will automatically run two test cases that demonstrate encryption and decryption:

### Test Case 1
Uses plaintext1.txt and keySecret1.txt:
- Plaintext (binary): 0110100001100101011011000110110001101111 (hello)
- Key (binary): 0100000100111111010001000010100001000111001010110100101101100010
- Generates ciphertext.txt and plaintext2.txt

### Test Case 2
Uses plaintext1.txt and keySecret2.txt:
- Plaintext (binary): Same as Test Case 1
- Key (hex): 51655468576D5A71
- Generates ciphertext2.txt and plaintext3.txt

## Output Format
The program provides detailed output for both encryption and decryption operations:

### Encryption Results
```
DES Encryption Results
--------------------------
Input:
Plaintext Binary: [binary string]
Key: [key used]
Output:
Ciphertext: [encrypted binary string]
```

### Decryption Results
```
DES Decryption Results:
--------------------------
Input:
Ciphertext: [encrypted binary string]
Key: [key used]
Output:
Decrypted Binary: [decrypted binary string]
Decrypted Hex: [hexadecimal representation]
```

## Implementation Details
- Uses OneAndZeroes padding scheme for messages not exactly 64 bits
- Implements standard DES components:
  - Initial and Final Permutations
  - 16 Feistel rounds
  - Expansion, Substitution, and Permutation boxes
  - Key scheduling
- Handles both binary and hexadecimal key formats
- Uses ECB (Electronic Codebook) mode for encryption/decryption

## Error Handling
The implementation includes error checking for:
- File not found errors
- Invalid key formats or lengths
- Key format validation (binary or hexadecimal)

## Verification
Results can be verified by:
1. Running the test cases
2. Comparing the decrypted output with the original input
3. Checking that the decrypted hex matches the expected value (e.g., "68656c6c6f" for "hello")