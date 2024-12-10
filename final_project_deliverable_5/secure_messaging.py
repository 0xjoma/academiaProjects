"""
Secure Messaging System Implementation
------------------------------------

This code implements a secure messaging system that enables confidential and verifiable 
message transmission between two parties using RSA and DES encryption.

Prerequisites:
-------------
The PyCryptodome library must be installed. Install it using:
   pip install pycryptodome

Required File Structure:
----------------------

1. Create a folder called 'D5-keys' containing:
  - KpubA.pem (Public key for Party A)
  - KpubB.pem (Public key for Party B) 
  - KprA.pem (Private key for Party A)
  - KprB.pem (Private key for Party B)
  - Ksecret.txt (DES secret key - must be exactly 8 ASCII characters)

2. Create plaintext.txt in the same directory as this script containing
  the message to encrypt in ASCII text format.

Running the Program:
------------------
1. Save this file as 'secure_messaging.py'
2. Open terminal/command prompt 
3. Navigate to the script's directory
4. Define the directory containing the cryptographic keys e.g. KEYS_DIR = './D5-keys/'
5. Run: python secure_messaging.py

The program will:
- Read plaintext from plaintext.txt
- Create three encrypted files: c1.bin, c2.bin, c3.bin
- Attempt to decrypt the message
- If successful: create plaintext2.txt with decrypted message
- If verification fails: print "REJECTED"

Contact:
Jomael Ortiz Perez - jomael.ortizperez.cv@proton.me
"""

from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

# Define the directory containing the cryptographic keys
KEYS_DIR = './D5-keys/'


def encrypt_message():
    """
    Implements the encryption process for Model 1's secure messaging system.

    The encryption process:
    1. Uses a hybrid cryptosystem (RSA + DES) for efficient encryption
    2. Creates a digital signature for non-repudiation
    3. Produces three components:
       - C1: RSA-encrypted DES key
       - C2: DES-encrypted message (with IV)
       - C3: Digital signature of C2
    """
    # Read the plaintext message and convert to bytes
    with open('./plaintext.txt', 'r') as f:
        message = f.read().encode('ASCII')

    # Read the DES secret key
    with open(KEYS_DIR + 'Ksecret.txt', 'r') as f:
        secret_key = f.read().encode('ASCII')

    # Load the required RSA keys
    public_key_b = RSA.import_key(open(KEYS_DIR + 'KpubB.pem').read())
    private_key_a = RSA.import_key(open(KEYS_DIR + 'KprA.pem').read())

    # Generate C1: RSA encryption of the DES key
    cipher_rsa = PKCS1_OAEP.new(public_key_b)
    c1 = cipher_rsa.encrypt(secret_key)

    # Generate C2: DES encryption of the message
    cipher_des = DES.new(secret_key, DES.MODE_OFB)
    c2 = cipher_des.iv + cipher_des.encrypt(message)

    # Generate C3: Digital signature of C2
    hash_obj = SHA256.new(c2)
    signer = pkcs1_15.new(private_key_a)
    c3 = signer.sign(hash_obj)

    # Write the three components to separate files
    with open('./c1.bin', 'wb') as f:
        f.write(c1)
    with open('./c2.bin', 'wb') as f:
        f.write(c2)
    with open('./c3.bin', 'wb') as f:
        f.write(c3)


def decrypt_message():
    """
    Implements the decryption process for Model 1's secure messaging system.

    The decryption process:
    1. Verifies the digital signature to ensure message integrity and non-repudiation
    2. Recovers the DES key using RSA decryption
    3. Decrypts the message using the recovered DES key

    If signature verification fails or decryption errors occur, the message is rejected.
    """
    # Read the three ciphertext components
    with open('./c1.bin', 'rb') as f:
        c1 = f.read()
    with open('./c2.bin', 'rb') as f:
        c2 = f.read()
    with open('./c3.bin', 'rb') as f:
        c3 = f.read()

    # Load the required RSA keys
    private_key_b = RSA.import_key(open(KEYS_DIR + 'KprB.pem').read())
    public_key_a = RSA.import_key(open(KEYS_DIR + 'KpubA.pem').read())

    try:
        # Verify the digital signature
        hash_obj = SHA256.new(c2)
        verifier = pkcs1_15.new(public_key_a)
        verifier.verify(hash_obj, c3)

        # Decrypt the DES key using RSA
        cipher_rsa = PKCS1_OAEP.new(private_key_b)
        secret_key = cipher_rsa.decrypt(c1)

        # Decrypt the message using DES
        iv = c2[:8]  # Extract the initialization vector
        ciphertext = c2[8:]  # Extract the actual ciphertext
        cipher_des = DES.new(secret_key, DES.MODE_OFB, iv=iv)
        plaintext = cipher_des.decrypt(ciphertext)

        # Write the decrypted message
        with open('./plaintext2.txt', 'w') as f:
            f.write(plaintext.decode('ASCII'))

    except Exception:
        # If any verification or decryption step fails, reject the message
        print("REJECTED")


if __name__ == "__main__":
    encrypt_message()
    decrypt_message()
