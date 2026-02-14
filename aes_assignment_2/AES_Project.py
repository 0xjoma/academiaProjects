"""
    In this project you will create a working AES crypto system.
    Wherever you see
        "Add code here"
    you need to fill in the code to perform the appropriate task.
    There are instructions commented throughout this file to help
    you complete the project.

    I recommend that you create a test method inside the AES class
    to test out each method (or function) as you go. This way it
    will be much easier to find any errors in your code.

    If you are having difficulty completing this project, email
    me at jtotushe@uwsuper.edu or stop into office hours.
"""

class AES:
    def __init__(self, key):
        self.key = key

    """
        AES does all its computations bitwise. That is the computations are done on binary
        strings. In most cases, we will use hexadecimal values to represent a binary string.
        Hexadecimal (hex) is a 16-digit number system. The digits are:
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a (10), b (11), c (12), d (13), e (14), and f (15).
        To convert a binary string to hexadecimal, one only needs to group the binary string
        into groups of 4 bits and convert each group of bits to decimal. 
        For example:
        10100110 ---> 1010 0110 ---> 8+2 4+2 ---> 10 8 ---> a8 (as 10 is represented by a).
        The conversion from hex to binary is to just apply the above process in reverse.

        In most cases we will do all operations on the integer value of the hexadecimal 
        number. There are a few cases where we will need to work with the actual binary string.

        sBox and invSBox are constructed from GF(2^8) (see below for the sBox and invSBox tables).
        The basic principle is that every element
        in GF(2^8) has an inverse. And so invSBox is the inverse of sBox.

        The table is read by row and column. For example, using the sBox table below, (3,5) would be the entry
        containing 0x96 (assuming we start counting at 0).

        Each entry is an integer (in hexadecimal).
        That is for 0x--, Python interprets this as an integer that has the same hex value
        as --. For example: 0x0b is the integer value 62. Or 0xab has integer value 171.
        If you are unfamiliar with this conversion process, look up an ASCII table online.
    """

    # Note that we will be using private methods (and variables) in the AES class.
    # Anything with a "__" in front of is private. That is it is only accessible from
    # within the class.
    __sBox = \
        [
            [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
            [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
            [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
            [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
            [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
            [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
            [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
            [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
            [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
            [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
            [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
            [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
            [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
            [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
            [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
            [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
        ]

    __invSBox = \
        [
            [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
            [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
            [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
            [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
            [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
            [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
            [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
            [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
            [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
            [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
            [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
            [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
            [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
            [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
            [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
            [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]
        ]

    """
        In GF(2^8), our elements are polynomials of degree 7 or less.
        Each coefficient is 0 or 1. There are two operations in GF(2^8).
        Addition (xor) and multiplication modulo an irreducible polynomial.
        The irreducible polynomial AES uses is:
            m(x) = x^8 + x^4 + x^3 + x + 1
        Note only the multiplication operation is modulo m(x). xor is not mod m(x).
        We represent a polynomial by a binary string. The index of the
        string represents the power on the coefficient.

        For example: x^7 + x^5 + x^2 + x + 1 is represented by 10100111.

        Multiplication of two polynomials should be thought of using
        the FOIL method. That way we only have to multiply a polynomial by x^p.
        Then add using the xor operation.

        The x_times method reads a polynomial (as a binary string) and
        multiplies it by x. Note that if the polynomial a has a 0 coefficient
        in degree 7, this is just a left shift of the binary digits. Note the
        left shift produces a 0 in the furthest right index.

        If there is a 1 in degree 7, then multiplying by x produces a degree
        8 polynomial (not in our space). The operation to produce a degree 7
        polynomial is then to xor the shifted binary string with 00011011 (or 1b in hex).
        See details of this process in the NIST-AES document.
    """

    # xTimes method should read in an int value and return an int value.
    # Remember the integer will be representing an ASCII value. And that
    # value has both a hexadecimal value and binary value.
    # This method should first convert the integer to an 8 bit binary string.
    # Then it should perform the x_times operation on the binary string
    # and return the (ASCII) integer value of the result.
    # The "^" symbol can be used to perform an xor operation (on ints).
    @staticmethod
    def __x_times(a):
        s = str(format(a, "08b"))  # Convert a to a binary string.

        # Add code here to perform the x_times operation.
        if s[0] == "1":
            return int(s[1:] + "0", 2) ^ 0x1B
        return int(s[1:] + "0", 2)

    """
        The following method multiplies two polynomials.
        The process works similarly to FOILing. That is multiply
        each term of polynomial p by every term of polynomial q.
        You can use the x_times method to help with this. For example:
        (x^7 + x^5 + x + 1)(x^3 + x^2 + 1)
        = x^7x^3 + x^7x^2 + x^7 + x^5x^3 + x^5x^2 + x^5 + xx^3 + xx^2 + x + x^3 + x^2 + 1
        Use the xor operation for any terms with the same degree.
        See the NIST-AES document for more details of this operation and a good example.
    """

    # This method should read in two integers (representing polynomials in GF(2^8)).
    # Then using the process described above, it should multiply the two polynomials
    # and return their result (as an integer).
    def __multiply_poly(self, p, q):
        pq = 0

        # Add code here to perform the multiply_poly operation.
        p = p & 0xFF
        q = q & 0xFF
        while q > 0:
            if q & 1:
                pq = pq ^ p
            p = self.__x_times(p)
            q = q >> 1

        return pq & 0xFF

    """
        The left_circular shift should read in a list and an integer n.
        Then it should apply a left shift by n indices to all 
        the entries. The value originally in degree 0 should be placed in the last
        index of the list. The shifted list should be returned.
        For example: [a, b, c, d] ---> [b, c, d, a] is a left shift of 1.
        Note AES will use a left shift with values 0, 1, 2, and 3.
    """

    def __left_circular_shift(self, a, n):
        shifted_list = []

        # Add code here for the left_circular_shift method.
        n = n % len(a)
        shifted_list = a[n:] + a[:n]
        for i in range(len(a)):
            a[i] = shifted_list[i]

        return shifted_list

    # The right_circular_shift method works like the left_circular_shift except
    # applies the shift to the right (instead of to the left).
    # For example: [a, b, c, d] ---> [d, a, b, c]
    def __right_circular_shift(self, a, n):
        shifted_list = []

        # Add code here for the right_circular_shift method.
        n = n % len(a)
        shifted_list = a[-n:] + a[:-n] if n != 0 else a[:]
        for i in range(len(a)):
            a[i] = shifted_list[i]

        return shifted_list

    """
        AES has a 2-dimensional state array (or list) that it performs
        all it's computation on. Think of this as a 4 x 4 matrix
        with hex entries.

        The shiftRows method applies a left circular shift
        to every row. Each row has a shift value of i where
        i is the index of the row. Note the index starts at
        0 and increases to 3. So the first row in the array
        has index 0 and gets a left shift by 0. The last row
        has index 3 and gets a left shift by 3.

        For example:
        [                           [
            [a, b, c, d]                [a, b, c, d]
            [e, f, g, h]    --->        [f, g, h, e]
            [i, j, k, l]                [k, l, i, j]
            [m, n, o, p]                [p, m, n, o]
        ]                           ]

        The method should read in a 2-dimensional list
        and return the 2-dimensional list (with the appropriate shift
        applied to each row).
    """

    def __shift_rows(self, m):
        for i in range(len(m)):
            self.__left_circular_shift(m[i], i)        
        return m

    """
        The inv_shift_rows method is essentially the same as shift_rows.
        Only difference is it will apply a right_circular_shift instead
        of a left_circular_shift.
    """

    def __inv_shift_rows(self, m):
        for i in range(len(m)):
            self.__right_circular_shift(m[i], i)        
        return m

    """
        table_lookup reads in an integer (from a hex value). Then it should
        convert this integer to a binary string. It then uses
        this binary string to look up a value in the sBox or invSBox.
        It then splits the binary string into two halves.
        Each half is converted to hexadecimal.
        The left half is used for the row and the right half
        is uses for the column. The method should return the
        hex value in table[row][column] (note this will be an int data type).
    """

    @staticmethod
    def __table_lookup(a, table):
        row = 0
        column = 0

        # Add code here for the table_lookup method.
        row = (a >> 4) & 0x0F
        column = a & 0x0F

        return table[int(row)][int(column)]

    """
        The subBytes method applies a transformation of the state
        (remember this is a 4 x 4 matrix or 2-d list).
        The method should transform the state by replacing the values
        in each index by sBox of that value.
        The transformed 2-d list should be returned.
    """

    def __sub_bytes(self, a):
        # Add code here for the sub_bytes method.
        for i in range(len(a)):
            for j in range(len(a[i])):
                a[i][j] = self.__table_lookup(a[i][j], self.__sBox)
        return a

    # This method is essentially the same as sub_bytes. Only it should
    # use the invSBox table instead of sBox.
    def __inv_sub_bytes(self, a):
        # Add code here for the inv_sub_bytes method.
        for i in range(len(a)):
            for j in range(len(a[i])):
                a[i][j] = self.__table_lookup(a[i][j], self.__invSBox)
        return a

    """
        The mix_columns method applies a transformation to each
        column in the state using the multiply_poly method.
        See section 5.1.3 of the NIST-AES document for details of how the mixing works.    
    """

    def __mix_columns(self, t):
        s = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]  # Define the 2-d list s and fill with 0's.

        # Add code here to perform the mix_columns method.
        for j in range(4):
            s[0][j] = self.__multiply_poly(0x02, t[0][j]) ^ self.__multiply_poly(0x03, t[1][j]) ^ t[2][j] ^ t[3][j]
            s[1][j] = t[0][j] ^ self.__multiply_poly(0x02, t[1][j]) ^ self.__multiply_poly(0x03, t[2][j]) ^ t[3][j]
            s[2][j] = t[0][j] ^ t[1][j] ^ self.__multiply_poly(0x02, t[2][j]) ^ self.__multiply_poly(0x03, t[3][j])
            s[3][j] = self.__multiply_poly(0x03, t[0][j]) ^ t[1][j] ^ t[2][j] ^ self.__multiply_poly(0x02, t[3][j])

        return s

    """
        The inv_mix_columns method is similar to the mix_columns.
        Each column gets an inverse transformation.
        See section 5.3.3 of the NIST-AES document for details of how the un-mixing works.
    """

    def __inv_mix_columns(self, t):
        s = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        # Add code here to perform the inv_mix_columns method.
        for j in range(4):
            s[0][j] = self.__multiply_poly(0x0E, t[0][j]) ^ self.__multiply_poly(0x0B, t[1][j]) ^ self.__multiply_poly(0x0D, t[2][j]) ^ self.__multiply_poly(0x09, t[3][j])
            s[1][j] = self.__multiply_poly(0x09, t[0][j]) ^ self.__multiply_poly(0x0E, t[1][j]) ^ self.__multiply_poly(0x0B, t[2][j]) ^ self.__multiply_poly(0x0D, t[3][j])
            s[2][j] = self.__multiply_poly(0x0D, t[0][j]) ^ self.__multiply_poly(0x09, t[1][j]) ^ self.__multiply_poly(0x0E, t[2][j]) ^ self.__multiply_poly(0x0B, t[3][j])
            s[3][j] = self.__multiply_poly(0x0B, t[0][j]) ^ self.__multiply_poly(0x0D, t[1][j]) ^ self.__multiply_poly(0x09, t[2][j]) ^ self.__multiply_poly(0x0E, t[3][j])

        return s

    """
        128 bit AES generates 10 round keys for the 10 rounds
        of the AES encryption (actually 11 keys, but the first
        key is copied from the input key). Each round key is
        again a 4 x 4 matrix (or 2-D list).

        The add_round_key method applies an xor operation between the
        state and the round key for each round of the AES algorithm.
        The xor operation is performed on each index of the matrices.
        See section 5.1.4 of the NIST-AES document for further details.
    """

    @staticmethod
    def __add_round_key(state, round_key):
        # Add code here for the add_round_key method.
        for i in range(4):
            for j in range(4):
                state[i][j] = state[i][j] ^ round_key[i][j]

        return state

    """
        The following methods are used to generate the round keys.
        We call this process the Key Expansion.

        The key expansion will produce the key schedule. With 128
        bit AES, this will be 11 round_keys. Our key_expansion method
        will create a 1-d list (with length 44) that we will break up into
        11 keys (each will be a 4 x 4 matrix or 2-d list).
        The key_expansion will use the methods rot_word and sub_word.

        The rot_word method is just a left circular shift of an array
        by 1 index.
    """

    @staticmethod
    def __rot_word(w):
        rotation = []

        # Add code here for the rot_word method.
        rotation = [w[1], w[2], w[3], w[0]]

        return rotation

    """
        The sub_word method does an sBox transformation
        applied to each 4 byte word. We will use a 1-d
        list to separate the 4 bytes in a word. Recall
        that a word is 32 bits (or 4 bytes where 1 byte
        is 8 bits).

        The method should read in a word (a 1-d list of length 4).
        In each index of the word, apply a sBox transformation 
        (using the table_lookup method). Store the result
        of the sBox transformations to output.
    """

    def __sub_word(self, w):
        output = []

        # Add code here for the sub_word method.
        for i in range(len(w)):
            output.append(self.__table_lookup(w[i], self.__sBox))

        return output

    """
        The following method reads in a string of hex digits
        and creates a list where each entry is an integer that
        represents a 2 digit hex number.
    """

    @staticmethod
    def __to_hex_list(s):
        key_table = []
        for i in range(0, len(s), 2):
            key_table.append(int(s[i:i + 2], 16))
        return key_table

    """
        The key_expansion generates 11 round keys where each round key is 4 words. Each word is 4 bytes
        or 4 2-digit hex numbers. To make things easier to organize, we will
        be treating each word as a 1-d list with 4 2 digit hexadecimal numbers.
        Each round key will contain 4 words. With 11 rounds this gives a total
        of 44 words. And so the expanded_key will be a 2-d list containing 44 words
        where each word is a 1-d list of 4 hex numbers.
        Please look in the NIST_AES document for additional details.

        The key_expansion uses the methods rot_word and sub_word. It also
        uses a list of values called r_con. Each value from r_con is a Hex string
        in which each element contains a 2-digit hex number followed by 6 zeros.
        Each value has r_con(i+1) = 2*r_con(i). Note this multiplication is done
        in GF(2^8). We will write r_con as a 2-d list where each entry is a list 
        of length 4 where each entry a 2-digit hex value. That is
            r_con(1) = [01, 00, 00, 00]
            r_con(2) = [02, 00, 00, 00]
            r_con(3) = [04, 00, 00, 00]
            r_con(4) = [08, 00, 00, 00]
            r_con(5) = [10, 00, 00, 00]
            r_con(6) = [20, 00, 00, 00]
            r_con(7) = [40, 00, 00, 00]
            r_con(8) = [80, 00, 00, 00]
            r_con(9) = [1b. 00, 00, 00]
            r_con(10)= [36, 00, 00, 00]

        Construction of the expanded_key is as follows:
        Let w_i denote the ith word (1-d list of 4 elements).
        In the code below, w_i will be the ith element of the expanded_key list.
        Step 1: Fill the first 4 elements of the expanded_key directly in from
                the inputted key.
        Step 2: Set i = 4.
        Step 3: Set r = rot_word(w_(i-1))
                    s = sub_word(r)
                    if i = 0 (mod 4), then temp = s xor r_con((i-4)/4)
                    else, then temp = w_(i-1)
        Step 4: Set w_i = w_(i-4) xor temp
        Step 5: Set i = i+1
        Step 6: repeat steps 3-5 nine more times for a total of 10 times.
    """

    # The following method should generate the expanded key.
    # The method should read in a key and generate
    # a 2-d list containing 44 1-d lists (these make up the 11 round keys).
    # The method should return the 2-d list.
    def __key_expansion(self, key):
        key_table = self.__to_hex_list(key)
        r_con = [[0x01, 0x00, 0x00, 0x00], [0x02, 0x00, 0x00, 0x00],
                 [0x04, 0x00, 0x00, 0x00], [0x08, 0x00, 0x00, 0x00],
                 [0x10, 0x00, 0x00, 0x00], [0x20, 0x00, 0x00, 0x00],
                 [0x40, 0x00, 0x00, 0x00], [0x80, 0x00, 0x00, 0x00],
                 [0x1B, 0x00, 0x00, 0x00], [0x36, 0x00, 0x00, 0x00]]
        
        # Setup the expanded_key list and fill the first 4 entries from the inputted key
        expanded_key = []
        for i in range(4):
            expanded_key.append([key_table[4*i], key_table[4*i + 1], key_table[4*i + 2], key_table[4*i + 3]])

        # Add code here to fill in the expanded_key list.
        for i in range(4, 44):
            temp = expanded_key[i - 1][:]
            if i % 4 == 0:
                temp = self.__sub_word(self.__rot_word(temp))
                for j in range(4):
                    temp[j] = temp[j] ^ r_con[int(i / 4) - 1][j]
            word = []
            for j in range(4):
                word.append(expanded_key[i - 4][j] ^ temp[j])
            expanded_key.append(word)

        return expanded_key

    """
        When AES first reads in a message, it first inputs the message
        into the state. We do this by separating the message into 16
        hex values 0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f and inputting them
        into a 4 x 4 matrix (or 2-d list) in the following form:
        0 4 8 c
        1 5 9 d
        2 6 a e
        3 7 b f
        As 2-d arrays usually treat each row as a 1-d array,
        we first write the message in as
        0 1 2 3
        4 5 6 7
        8 9 a b
        c d e f
        Then switch columns and rows.

        The method switch_columns_rows should do this operation.
        That is it should transform
        0 1 2 3                    0 4 8 c
        4 5 6 7        into        1 5 9 d
        8 9 a b        --->        2 6 a e
        c d e f                    3 7 b f
    """

    @staticmethod
    def __switch_columns_rows(table):
        # setup switch_table.
        switch_table = []
        for i in range(4):
            switch_table.append([])

        # fill in switch_table.
        for i in range(4):
            for j in range(4):
                switch_table[j].append(table[i][j])        

        return switch_table

    """
        This method makes a 3-d list
        that contains all roundKeys (each round_key
        is a 2-d list build from the 11 elements
        in the key_expansion). Each round key is a
        4 x 4 matrix. There is a total of 11 round keys.
    """

    def __get_round_keys(self, key):
        expanded_key = self.__key_expansion(key)

        # Set up 3-d list for round_keys and fill it with 0's
        round_keys = []
        for i in range(11):
            round_keys.append([])
            for j in range(4):
                round_keys[i].append([])
                for k in range(4):
                    round_keys[i][j].append(0)

        # Fill in the round_keys.
        for i in range(0, len(expanded_key), 4):
            for j in range(4):
                for k in range(4):
                    round_keys[int(i / 4)][j][k] = expanded_key[k + i][j]
        return round_keys

    """
        This method reads in a ASCII message,
        and sets the initial state.
    """

    def __initial_state(self, m):
        message_list = self.__to_hex_list(m)
        state = []
        for i in range(0, 16, 4):
            state.append([])
            state[int(i / 4)].append(message_list[i])
            state[int(i / 4)].append(message_list[i + 1])
            state[int(i / 4)].append(message_list[i + 2])
            state[int(i / 4)].append(message_list[i + 3])

        return self.__switch_columns_rows(state)

    """
        The to_hex_blocks method creates a list where each
        element is a 128 bit hex block. A message is read 
        into the method and broken up into 128 bit blocks 
        and stored in a list.
    """

    @staticmethod
    def __to_hex_blocks(message):
        while len(message) % 32 != 0:
            message = "0" + message

        message_blocks = []
        for i in range(0, len(message), 32):
            message_blocks.append(message[i:i + 32])
        return message_blocks

    """
        After encryption or decryption, this method
        converts the output state to a string
        of Hex values. Note that if a hex number has
        one digit, the method adds a 0 to the left of
        the digit so that the string has the correct
        length. Every output string should have 32
        hex digits.
    """

    def __table_to_string(self, m):
        s = ""
        m = self.__switch_columns_rows(m)
        for i in range(len(m)):
            for j in range(len(m[i])):
                t = "%x" % int(m[i][j])
                if len(t) == 1:
                    s = s + "0" + t
                else:
                    s = s + t
        return s

    """
        This method is where all the encryption is done.
        The cipher first needs to set the state.
        All operations are performed on the state to produce a new state.
        Step 1: add the initial round key to the state.
        Step 2: apply sub_bytes to state
        Step 3: shift_rows.
        Step 4: mix_columns.
        Step 5: add the round key.
        Step 6: repeat steps 2-5 8 more times.
                 (Steps 2-5 get done a total of 9 times).
        Step 7: apply sub_bytes to state.
        Step 8: shift_rows.
        Step 9: add the last round key.
        Step 10: return the state.
    """

    def __cipher(self, message):
        state = self.__initial_state(message)
        round_keys = self.__get_round_keys(self.key)

        # Add code here to perform the required steps for the cipher method.
        state = self.__add_round_key(state, round_keys[0])
        for i in range(1, 10):
            state = self.__sub_bytes(state)
            state = self.__shift_rows(state)
            state = self.__mix_columns(state)
            state = self.__add_round_key(state, round_keys[i])
        state = self.__sub_bytes(state)
        state = self.__shift_rows(state)
        state = self.__add_round_key(state, round_keys[10])

        return state

    """
        The invCipher is similar to the cipher method.
        It essentially runs the cipher in reverse.
        See the NIST-AES document for details.
    """

    def __inv_cipher(self, cipher_text):
        state = self.__initial_state(cipher_text)
        round_keys = self.__get_round_keys(self.key)

        # Add code here to perform the required steps for the inv_cipher method.
        state = self.__add_round_key(state, round_keys[10])
        for i in range(9, 0, -1):
            state = self.__inv_shift_rows(state)
            state = self.__inv_sub_bytes(state)
            state = self.__add_round_key(state, round_keys[i])
            state = self.__inv_mix_columns(state)
        state = self.__inv_shift_rows(state)
        state = self.__inv_sub_bytes(state)
        state = self.__add_round_key(state, round_keys[0])

        return state

    """
        This method reads in the message, breaks it into
        128 bit hex blocks, runs each hex block through cipher,
        and finally appends together the outputs to make a
        cipher_text string.
    """

    def encrypt(self, message):
        hex_message = ""
        for i in range(len(message)):
            hex_message = hex_message + format(ord(message[i]), "x")
        hex_blocks = self.__to_hex_blocks(hex_message)
        cipher_text = ""
        for i in range(len(hex_blocks)):
            cipher_text = cipher_text + self.__table_to_string(self.__cipher(hex_blocks[i]))
        return cipher_text

    """
        The method below is used in the decryption process to convert a 
        list of hex values back to ascii. It reads in a list
        of integers (each representing a hex value) and converts
        the list into a string of their ascii values. 
    """

    @staticmethod
    def __hex_list_to_text(hex_list):
        text = ""
        for i in range(len(hex_list)):
            text = text + chr(hex_list[i])
        return text

    """
        This method reads in a hex string, separates the string into
        128 bit hex blocks, sends each block through inv_cipher
        and finally appends the outputs into a ASCII string.
    """

    def decrypt(self, cipher_text):
        plain_text = ""
        hex_blocks = self.__to_hex_blocks(cipher_text)
        for i in range(len(hex_blocks)):
            decrypted_state = self.__switch_columns_rows(self.__inv_cipher(hex_blocks[i]))
            for j in range(len(decrypted_state)):
                plain_text = plain_text + self.__hex_list_to_text(decrypted_state[j])
        return plain_text


# Below is the main part of the program.
# Here we create an AES object (by inputting the key)
# and perform encryption and decryption on a test message

# The aes key from the NIST_AES.pdf document.
my_aes = AES("2b7e151628aed2a6abf7158809cf4f3c")

# another aes key.
# my_aes = AES("0f1571c947d9e8590cb7add6af7f6798")

cipher = my_aes.encrypt("This is a test message! This is a test message! This is a test message!")
print(cipher)
# The output from the above encryption should be
# 5c856c6cff2d6ce984e944fcdc2a4948da27a202bff253a3579480d2e86ffdb49732e781041c74f2f3600839e217e4a83450cbf6d1aeffbffa80472b866032a3da27a202bff253a3579480d2e86ffdb4

decrypted_message = my_aes.decrypt(cipher)
print(decrypted_message)
