# A basic implementation of RSA
# Messages to be signed are a maximum of 510 bits.
# Keys used are 512 bits for n (128 hexadecimal digits),  with e or d (both in hexadecimal digits) following
# on the next line in the key files

from StringConversion import *

# performs RSA encryption
# return the ciphertext produced by RSA for the input plaintext M. Note that M and ciphertext are integers
# This method may not send anything to standard output.


def encrypt(n, e, M):
    return modularExponent(M, e, n)

# performs RSA decryption
# return the plaintext produced by RSA for the ciphertext C. Note that C and plaintext are integers
# This method may not send anything to standard output.


def decrypt(n, d, C):
    return modularExponent(C, d, n)

# This method computes the modular exponent a^e mod m  using the repeated squares method
# It must be implemented from scratch
# Used by encrypt and decrypt above


def modularExponent(a, e, m):
    result = 1
    a = a % m  # Update 'a' if 'a' >= m

    binary_e = bin(e)[2:]

    for bit in binary_e:
        result = (result * result) % m
        if bit == '1':
            result = (result * a) % m

    return result


# encrypts the text in the file named by the first parameter with the public  key in the file named in the second parameter.
# the encrypted text is written to the file named by the third parameter.
# the string text in the plaintextFileName should be 62 characters or less
def RSA_encrypt(plaintextFileName, publicKeyFileName, ciphertextFileName):
    infile = open(plaintextFileName, "r")
    outfile = open(ciphertextFileName, "w")
    # Convert plaintext to an integer representation
    strg = infile.read()
    M = stringToInteger(strg)

    keyfile = open(publicKeyFileName, "r")
    n = int(keyfile.readline().strip(), 16)
    e = int(keyfile.readline().strip(), 16)
    keyfile.close()

    C = encrypt(n, e, M)
    outfile.write(str(C))
    infile.close()
    outfile.close()
    return


# decrypts the text in the file named by the first parameter with the private key in the file named in the second parameter.
# the decrypted text is written to the file named by the third parameter.
def RSA_decrypt(ciphertextFileName, privateKeyFileName, plaintextFileName):
    infile = open(ciphertextFileName, "r")
    outfile = open(plaintextFileName, "w")
    # read cipher from file
    C = int(infile.read())

    # read privateKeyFileName to extract n and d
    keyfile = open(privateKeyFileName, "r")
    n = int(keyfile.readline().strip(), 16)
    d = int(keyfile.readline().strip(), 16)

    M = decrypt(n, d, C)
    outfile.write(integerToString(M))
    infile.close()
    outfile.close()
    return


# main function to start off program
def main():
    # Calls RSA_encrypt and RSA_decrypt separately

    # Hard code the file names here
    # Test 1 with first key pair
    plaintextFileName = "final_project_deliverable_2/plaintext1.txt"
    publicKeyFileName = "final_project_deliverable_2/keyPub1.txt"
    ciphertextFileName = "final_project_deliverable_2/results/ciphertext.txt"
    # Encrypt the plaintext
    RSA_encrypt(plaintextFileName, publicKeyFileName, ciphertextFileName)

    privateKeyFileName = "final_project_deliverable_2/keyPri1.txt"
    plaintextFileName2 = "final_project_deliverable_2/results/plaintext2.txt"
    # Decrypt the ciphertext
    RSA_decrypt(ciphertextFileName, privateKeyFileName, plaintextFileName2)

    # Test 2 with second key pair
    plaintextFileName3 = "final_project_deliverable_2/plaintext3.txt"
    publicKeyFileName2 = "final_project_deliverable_2/keyPub2.txt"
    ciphertextFileName2 = "final_project_deliverable_2/results/ciphertext2.txt"
    # Encrypt the plaintext
    RSA_encrypt(plaintextFileName3, publicKeyFileName2, ciphertextFileName2)

    privateKeyFileName2 = "final_project_deliverable_2/keyPri2.txt"
    plaintextFileName4 = "final_project_deliverable_2/results/plaintext4.txt"
    # Decrypt the ciphertext
    RSA_decrypt(ciphertextFileName2, privateKeyFileName2, plaintextFileName4)

    # Now visually compare plaintextFileName and plaintextFileName2 to verify they are identical


if __name__ == "__main__":
    main()
