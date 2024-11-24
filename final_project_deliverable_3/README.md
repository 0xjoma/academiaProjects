# MMO Hash Function Implementation

This repository contains an implementation of the 128-bit Matyas-Meyer-Oseas (MMO) hash function. The implementation includes the core hash function along with two test cases to verify its functionality.

## Project Structure

```
academiaProjects/final_deliverable_3/
│
├── resources/
│   └── deliverableInstructions.docx   # Project instructions
│
├── results/                           # Hash output directory
│   ├── hash1.txt                      # Test case 1 output
│   └── hash2.txt                      # Test case 2 output
│
├── MMO.py                             # Main implementation file
├── README.md                          # Instructions
├── StringConversion.py                # Utility functions for string conversion
├── README.md                          # This documentation file
├── test1.txt                          # Test case 1 input file (simple string)
└── test2.txt                          # Test case 2 input file (multi-block test)
```

## Prerequisites

- Python 3.x
- No additional libraries required (uses only standard library)

## Running the Test Cases

### Test Case 1: Basic String Hash
This test case verifies the hash function's behavior with a simple text input.

1. Create a file named `test1.txt` with the following content:
   ```
   Hello, this is test case 1.
   ```

2. Run the test:
   ```bash
   cd academiaProjects/final_deliverable_3
   python MMO.py
   ```

3. Verify the results:
   - Check that `results/hash1.txt` has been created
   - The hash value should be a 128-bit value (represented as a string)
   - Given H0 = 12345, the output should be consistent

### Test Case 2: Multi-Block Input Hash
This test case verifies the hash function's behavior with a longer input that requires multiple 128-bit blocks, testing the block splitting and chaining functionality.

1. Create a file named `test2.txt` with the following content:
   ```
   This is a longer test case that will require multiple 128-bit blocks to test the block splitting and chaining functionality of the MMO hash function.
   ```

2. `test2.txt` contains a longer text input that spans multiple 128-bit blocks to test:
   - Block splitting functionality
   - Chaining between blocks
   - Proper padding of the final block

3. Run the test:
   ```bash
   python MMO.py
   ```

4. Verify the results:
   - Check that `results/hash2.txt` has been created
   - The hash value should be a 128-bit value (represented as a string)
   - Given H0 = 67890, the output should be consistent
   - Verify that changing any part of the input produces a different hash value

## Expected Test Results

For both test cases, verify the following:

1. Hash Length:
   - The binary representation of each hash should be exactly 128 bits
   - You can verify this using the provided function in the test output

2. Consistency:
   - Running the tests multiple times with the same H0 value should produce identical results
   - The hashes for test1.txt and test2.txt should be different

3. Block Processing:
   - Test case 2 specifically verifies that the implementation correctly handles:
     * Multiple block processing
     * Block chaining
     * Final block padding
     * Consistent results across multiple runs

## Troubleshooting

If the tests fail, check the following:

1. File Paths:
   - Ensure you're in the correct directory (`academiaProjects/final_deliverable_3`)
   - Verify that the results directory exists and is writable

2. File Encoding:
   - Ensure test files are saved with UTF-8 encoding
   - Verify line endings are consistent

3. Common Issues:
   - If hash values aren't consistent, verify H0 values are set correctly
   - If block processing seems incorrect, verify the padding implementation
   - Check that the g function is properly handling the last bit as specified

## Additional Notes

- The test cases use fixed H0 values (12345 and 67890) for reproducibility
- Test case 2 verifies proper handling of:
  * Block splitting
  * Block chaining
  * Final block padding
  * Proper state maintenance between blocks

## Extended Testing

To verify the implementation more thoroughly, you can:

1. Modify test case 2 by:
   - Adding more text to create additional blocks
   - Changing specific parts of the input to verify the avalanche effect
   - Testing with different block boundary conditions

2. Modify H0 values to test with different initial states

3. Compare hashes of similar inputs to verify the avalanche effect


## License
[MIT License](https://opensource.org/licenses/MIT)

## Contact
Jomael Ortiz Perez - jomael.ortizperez.cv@proton.me\
Project Link: https://github.com/0xjoma/academiaProjects/tree/main/final_project_deliverable_3