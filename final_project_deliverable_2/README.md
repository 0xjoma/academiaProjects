# RSA (Rivest-Shamir-Adleman) Implementation
This project implements the RSA public-key cryptography system in Python, providing both encryption and decryption functionality using a 512-bit strong encryption.

## Project Structure
```
.
├── .DS_Store              # macOS system file
├── README.md              # Main documentation file
├── RSA.py                # Main RSA implementation with test cases
├── StringConversion.py    # Utility functions for binary/string/integer conversions
├── __pycache__/          # Python cache directory
├── keyPri1.txt           # First private key file (hex format)
├── keyPri2.txt           # Second private key file (hex format)
├── keyPub1.txt           # First public key file (hex format)
├── keyPub2.txt           # Second public key file (hex format)
├── plaintext1.txt        # First sample plaintext file
├── plaintext3.txt        # Second sample plaintext file
├── resources/            # Contains academic research and documentation about RSA
├── results/             # Contains output files from encryption/decryption
│   ├── ciphertext.txt   # Encrypted output from Test Case 1
│   ├── plaintext2.txt   # Decrypted output from Test Case 1
│   ├── ciphertext2.txt  # Encrypted output from Test Case 2
│   └── plaintext4.txt   # Decrypted output from Test Case 2
└── selfAssessment/       # Contains self-assessment documentation
    └── README_selfAssessment.md  # Detailed self-assessment against rubric
```

## Documentation
- Main implementation documentation is in this README
- The implementation follows the RSA specification as outlined in RFC 8017
- Academic research and references can be found in the resources/ directory

## Prerequisites
- Python 3.x

## Files Required
1. Input plaintext file containing ASCII text (maximum 62 characters)
2. Key files in hexadecimal format containing:
   - First line: n (512-bit modulus) as 128 hexadecimal digits
   - Second line: e (public exponent) or d (private exponent) in hexadecimal

## Key File Format Example
```
00B660F96FA958685E9C6C7981E7FB909F48C394AF59379CDAAB6D6E84CCF3107D8883057428F05E2F84CEDC0E81DDB32152E4171FD8EB068EAE55A734B0D3E05B
010001
```

## Running the Implementation
```bash
python RSA.py
```

This will automatically run two test cases that demonstrate encryption and decryption:

### Test Case 1
Uses plaintext1.txt with first key pair (keyPub1.txt/keyPri1.txt):
- Encrypts using the public key and generates ciphertext.txt
- Decrypts using the private key and generates plaintext2.txt

### Test Case 2
Uses plaintext3.txt with second key pair (keyPub2.txt/keyPri2.txt):
- Encrypts using the public key and generates ciphertext2.txt
- Decrypts using the private key and generates plaintext4.txt

## Implementation Details
- Uses 512-bit RSA encryption (n is 512 bits)
- Implements core RSA components:
  - Modular exponentiation using repeated squares method
  - Public key encryption
  - Private key decryption
  - String-to-integer and integer-to-string conversions
- Messages must be 62 characters or less (to fit within 510 bits)
- Uses helper functions from StringConversion.py for type conversions

## Core Functions
1. `encrypt(n, e, M)`: RSA encryption with public key
2. `decrypt(n, d, C)`: RSA decryption with private key
3. `modularExponent(a, e, m)`: Efficient modular exponentiation
4. `RSA_encrypt(plaintextFileName, publicKeyFileName, ciphertextFileName)`
5. `RSA_decrypt(ciphertextFileName, privateKeyFileName, plaintextFileName)`

## Current Implementation Notes
- The implementation assumes:
  - Input files exist and are accessible
  - Plaintext messages are 62 characters or less
  - Key files follow the correct format with valid hexadecimal values
  - Input values will not cause integer overflow

Note: For a more robust implementation, error handling could be added for:
- File operations
- Input validation
- Key format verification
- Integer overflow checks

## Setup and Installation

You can get the project files in one of two ways:

### Option 1: Clone via GitHub
```bash
# Clone the academia projects repository
git clone https://github.com/0xjoma/academiaProjects.git

# Navigate to the RSA implementation directory
cd academiaProjects/final_project_deliverable_2
```

### Option 2: Manual Download
1. Visit https://github.com/0xjoma/academiaProjects/tree/main/final_project_deliverable_2
2. Download the following files:
   - RSA.py
   - StringConversion.py
   - plaintext1.txt
   - plaintext3.txt
   - keyPub1.txt
   - keyPri1.txt
   - keyPub2.txt
   - keyPri2.txt
3. Create a new directory for the project
4. Place all downloaded files in the directory
5. Create a 'results' subdirectory for output files

### Set Up Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# No additional packages required for this implementation
```

### Directory Setup
```bash
# Create results directory if it doesn't exist
mkdir -p results
```

## Security Considerations
- This implementation uses 512-bit RSA which, while suitable for educational purposes, is not considered secure for production use
- Modern applications should use at least 2048-bit RSA
- The implementation does not include padding schemes required for secure real-world usage
- This is an academic implementation and should not be used for actual encryption needs

## Deactivating Virtual Environment
When you're done working with the project:
```bash
deactivate
```

## License
[MIT License](https://opensource.org/licenses/MIT)

## Contact
Jomael Ortiz Perez - jomael.ortizperez.cv@proton.me\
Project Link: https://github.com/0xjoma/academiaProjects/tree/main/final_project_deliverable_2