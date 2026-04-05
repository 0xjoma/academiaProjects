"""
    Part 1 - HashLib
"""
import hashlib

name = "Jomael Ortiz Perez"

print("Name:", name)
print("SHA-1:   ", hashlib.sha1(name.encode()).hexdigest())
print("SHA-256: ", hashlib.sha256(name.encode()).hexdigest())
print("SHA-512: ", hashlib.sha512(name.encode()).hexdigest())
print("SHA3-256:", hashlib.sha3_256(name.encode()).hexdigest())
