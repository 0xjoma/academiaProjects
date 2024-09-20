import math


def linear_congruential_generator(seed, a, b, m, n):
    # Initialize variables
    s = seed
    binary_output = ""

    while len(binary_output) < n:
        # Generate next number in the sequence
        s = (a * s + b) % m

        # Convert to binary and remove '0b' prefix
        binary_s = bin(s)[2:]

       # Pad with zeros to ensure length consistency
        binary_s = binary_s.zfill(31)  # m is 2^31, so 31 bits are needed

        # ADD to the output
        binary_output += binary_s

    # Trim to exactly n digits
    return binary_output[:n]


# Setting textbook values
seed = 12345
a = 1103515245
b = 12345
m = 2**31
N = 1000

# Generate the sequence
output_sequence = linear_congruential_generator(seed, a, b, m, N)

# Save the output to a file
with open('output.txt', 'w') as f:
    f.write(output_sequence)

print(f"Generated {N} bits and saved to 'output.txt'")

# Analysis
ones_count = output_sequence.count('1')
zeros_count = output_sequence.count('0')
substring_count = output_sequence.count('01')

print(f"Number of 1s: {ones_count}")
print(f"Number of 0s: {zeros_count}")
print(f"Number of 01 substrings: {substring_count}")

expected_substring_count = (N - 1) / 4  # For truly random sequence

print(f"Expected number of '01' substrings in a truly random sequence: {
      expected_substring_count}")
